#!/usr/bin/env python3
"""Check built-site navigation, social previews and utility-page behavior."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys
import base64
import hashlib


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.meta = {}
        self.assets = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "link" and "stylesheet" in attrs.get("rel", ""):
            self.assets.append((attrs.get("href", ""), attrs.get("integrity")))
        if tag in ("img", "script") and attrs.get("src"):
            self.assets.append((attrs["src"], attrs.get("integrity")))
        if tag == "meta":
            self.meta[attrs.get("name", attrs.get("property", ""))] = attrs.get("content", "")


root = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
pages = {path: Page(path.read_text()) for path in root.rglob("*.html")}
errors = []
for path, page in pages.items():
    # Hugo's redirect aliases have no page chrome or social metadata.
    if "main" not in page.ids:
        continue
    if page.meta.get("twitter:site") != "@archit_singh15":
        errors.append(f"{path}: invalid social handle")
    if "papermod-cover.png" in page.meta.get("og:image", ""):
        errors.append(f"{path}: stock theme social image")
    for url, integrity in page.assets:
        asset = urlparse(url)
        if asset.netloc and asset.netloc != "archit15singh.github.io":
            continue
        target = root / asset.path.lstrip("/")
        if not target.is_file():
            errors.append(f"{path}: missing asset {url}")
        elif integrity and integrity.startswith("sha256-"):
            actual = "sha256-" + base64.b64encode(hashlib.sha256(target.read_bytes()).digest()).decode()
            if actual != integrity:
                errors.append(f"{path}: asset integrity mismatch {url}")
    for href in page.links:
        url = urlparse(href)
        if url.scheme or url.netloc or (url.path and not url.path.startswith("/")):
            continue
        target = root / url.path.lstrip("/") if url.path else path
        if target.is_dir():
            target /= "index.html"
        if not target.exists():
            errors.append(f"{path}: missing target {href}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{path}: missing heading {href}")

for name in ("about", "contact", "projects", "research", "speaking"):
    path = root / name / "index.html"
    text = path.read_text()
    if 'class=lp-play' in text or 'class="lp-play"' in text or 'class=post-meta' in text:
        errors.append(f"{path}: article controls on utility page")

for error in errors:
    print(error, file=sys.stderr)
if errors:
    sys.exit(1)
print(f"PASS: navigation, heading links, social metadata and utility layouts ({len(pages)} HTML files)")
