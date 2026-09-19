#!/usr/bin/env python3
"""Scan a Hugo-built site for broken links and missing anchors.

Usage:
  python3 check-links.py [--dir public] [--external]

Exit 0 = clean. Exit 1 = issues found. Exit 2 = scan error.
"""
import argparse
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "blob:", "sms:", "callto:")
IGNORED_FRAGMENTS = {"", "top", "comments"}


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for key, val in attrs:
            if not val:
                continue
            key = key.lower()
            if key in ("href", "src", "poster", "data-src", "data-lazy-src"):
                self.refs.append((tag, key, val.strip()))
            elif key == "srcset":
                for bit in val.split(","):
                    parts = bit.strip().split()
                    if parts:
                        self.refs.append((tag, key, parts[0]))


def collect_pages(root):
    pages = []
    for p in root.rglob("*.html"):
        if p.is_file():
            pages.append(p)
    return pages


def resolve_target(root, page, path):
    if path.startswith("/"):
        joined = path.lstrip("/")
    else:
        base = page.parent.relative_to(root).as_posix()
        joined = os.path.normpath(os.path.join(base, path))
    if joined in (".", ""):
        joined = "index.html"
    elif joined.endswith("/"):
        joined = joined + "index.html"
    cand = root / joined
    if cand.is_file():
        return cand
    if cand.is_dir():
        idx = cand / "index.html"
        return idx if idx.is_file() else None
    if not Path(joined).suffix:
        idx = root / joined / "index.html"
        return idx if idx.is_file() else None
    return None


def has_anchor(target, frag):
    try:
        text = target.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    pat = r"\b(?:id|name)=[\"']?"
    if re.search(pat + re.escape(frag) + r"[\"'\s>]", text):
        return True
    return False


def check_external(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        pass
    req2 = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-1024"})
    try:
        with urllib.request.urlopen(req2, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="Broken-link scanner for a built Hugo site")
    ap.add_argument("--dir", default="public", help="built site dir (default: public)")
    ap.add_argument("--external", action="store_true", help="verify external URLs too")
    ap.add_argument("--base", default="", help="own site base URL; matching absolute links are checked locally (e.g. https://example.github.io/)")
    args = ap.parse_args()

    base = args.base.rstrip("/")
    base_host = urlparse(base).netloc if base else ""

    root = Path(args.dir).resolve()
    if not root.is_dir() or not (root / "index.html").is_file():
        print(f"error: {root} is not a built site (no index.html)", file=sys.stderr)
        return 2

    pages = collect_pages(root)
    issues = []
    externals = []
    skipped_external = 0

    for page in pages:
        try:
            parser = LinkExtractor()
            parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        except OSError as e:
            print(f"warn: unreadable {page}: {e}", file=sys.stderr)
            continue
        rel_page = page.relative_to(root).as_posix()
        for tag, attr, val in parser.refs:
            if not val:
                continue
            low = val.lower()
            if val.startswith("//"):
                if args.external:
                    externals.append((rel_page, "https:" + val))
                else:
                    skipped_external += 1
                continue
            if low.startswith(SKIP_SCHEMES):
                continue
            p = urlparse(val)
            if p.scheme in ("http", "https"):
                if p.netloc == base_host:
                    path = p.path
                    frag = p.fragment
                    path = os.path.normpath(path.lstrip("/"))
                    target = resolve_target(root, page, "/" + path)
                    label = f"{rel_page} -> {val}"
                    if target is None:
                        issues.append(f"404  {label}")
                    elif frag and frag not in IGNORED_FRAGMENTS and not has_anchor(target, frag):
                        issues.append(f"anchor {label}  (missing #{frag})")
                elif args.external:
                    externals.append((rel_page, val))
                else:
                    skipped_external += 1
                continue
            frag = p.fragment
            if val == "#" or frag in IGNORED_FRAGMENTS:
                continue
            if not p.path and frag:
                target = page
                label = f"{rel_page}#{frag}"
            else:
                target = resolve_target(root, page, p.path)
                label = f"{rel_page} -> {val}"
            if target is None:
                issues.append(f"404  {label}")
            elif frag and not has_anchor(target, frag):
                issues.append(f"anchor {label}  (missing #{frag})")

    if args.external:
        unique = {}
        for rel_page, url in externals:
            if url not in unique:
                unique[url] = rel_page
        items = list(unique.items())
        print(f"checking {len(items)} unique external URLs (concurrency 8)...", file=sys.stderr)
        done = 0
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(check_external, url): url for url, _ in items}
            for fut in futures:
                url = futures[fut]
                code = fut.result()
                done += 1
                if done % 50 == 0:
                    print(f"... {done}/{len(items)}", file=sys.stderr)
                if code is None or code >= 400:
                    issues.append(f"external {code}  {unique[url]} -> {url}")
    else:
        pass

    seen = []
    for line in issues:
        if line not in seen:
            seen.append(line)

    print(f"scanned {len(pages)} html pages, {skipped_external} external links skipped (use --external)")
    for line in seen:
        print(line)
    if seen:
        print(f"{len(seen)} unique issues")
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())