#!/usr/bin/env python3
"""
linli - throwaway local LinkedIn post scheduler.

Talks straight to LinkedIn's official REST API. No Docker, no third-party
service, no dependencies beyond the Python standard library. All state lives
under this file's directory (~/linli by default) so `linli nuke` wipes
everything in one shot.

Commands:
  auth              One-time OAuth login (opens a browser).
  whoami            Show the logged-in member (verifies the stored token).
  post              Post text (+ optional local images) right now.
  schedule          Queue a post for a future date/time.
  list              List queued posts.
  cancel <id>       Remove a queued post.
  run               Foreground scheduler loop: posts due jobs, Ctrl-C to stop.
  nuke              Delete ALL local state (tokens + queued posts).

Auth setup (once): create a LinkedIn developer app, add the products
"Sign In with LinkedIn using OpenID Connect" and "Share on LinkedIn", set the
redirect URL to http://localhost:8765/callback, then export:
  export LINKEDIN_CLIENT_ID=...      export LINKEDIN_CLIENT_SECRET=...
"""

import argparse
import http.server
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timezone
from typing import NoReturn

# --- Layout -----------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(BASE_DIR, "state")
TOKEN_PATH = os.path.join(STATE_DIR, "token.json")
JOBS_DIR = os.path.join(STATE_DIR, "jobs")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# --- LinkedIn endpoints -----------------------------------------------------
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
IMAGES_URL = "https://api.linkedin.com/rest/images"
POSTS_URL = "https://api.linkedin.com/rest/posts"
SCOPES = "openid profile w_member_social"
REDIRECT_URI = "http://localhost:8765/callback"
CALLBACK_PORT = 8765
# LinkedIn requires a dated API version header (YYYYMM). Override with
# LINKEDIN_API_VERSION if this one is retired.
API_VERSION = os.environ.get("LINKEDIN_API_VERSION", "202401")
MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 20 MB safety cap


# --- Small helpers ----------------------------------------------------------
def die(msg, hint=None, code=2) -> NoReturn:
    print(f"Error: {msg}", file=sys.stderr)
    if hint:
        print(f"Hint: {hint}", file=sys.stderr)
    sys.exit(code)


def ensure_state_dirs():
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(JOBS_DIR, exist_ok=True)
    os.chmod(STATE_DIR, 0o700)


def _require_https(url, what):
    if urllib.parse.urlparse(url).scheme != "https":
        die(f"refusing non-HTTPS {what}: {url}")


def load_config():
    """Client id/secret from env first, then config.json (which must be 0600)."""
    cid = os.environ.get("LINKEDIN_CLIENT_ID")
    csec = os.environ.get("LINKEDIN_CLIENT_SECRET")
    if cid and csec:
        return cid, csec
    if os.path.exists(CONFIG_PATH):
        mode = os.stat(CONFIG_PATH).st_mode & 0o077
        if mode:
            die(f"{CONFIG_PATH} is group/world accessible",
                hint="chmod 600 it — it holds your client secret")
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        cid = cid or cfg.get("client_id")
        csec = csec or cfg.get("client_secret")
    if not (cid and csec):
        die("no LinkedIn client credentials found",
            hint="export LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET, "
                 "or put them in config.json (chmod 600)")
    return cid, csec


def save_token(data):
    ensure_state_dirs()
    data["obtained_at"] = int(time.time())
    # Write 0600 from the start: create with restrictive mode, then write.
    fd = os.open(TOKEN_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(TOKEN_PATH, 0o600)


def load_token():
    if not os.path.exists(TOKEN_PATH):
        die("not authenticated", hint="run: linli auth")
    with open(TOKEN_PATH) as f:
        tok = json.load(f)
    expires_at = tok.get("obtained_at", 0) + tok.get("expires_in", 0)
    if expires_at and time.time() > expires_at:
        die("access token expired", hint="run: linli auth")
    return tok


def _http_json(url, headers, data=None, method=None):
    """Do an HTTPS request, parse JSON. Raises with the server body on error."""
    _require_https(url, "request")
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}, dict(resp.headers)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        die(f"LinkedIn API {e.code} on {urllib.parse.urlparse(url).path}: {detail}")
    except urllib.error.URLError as e:
        die(f"network error reaching LinkedIn: {e.reason}")


# --- OAuth ------------------------------------------------------------------
class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    code = None
    state = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return
        qs = urllib.parse.parse_qs(parsed.query)
        _CallbackHandler.code = qs.get("code", [None])[0]
        _CallbackHandler.state = qs.get("state", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        msg = b"<h2>linli: authorization received. You can close this tab.</h2>"
        self.wfile.write(msg)

    def log_message(self, format, *args):
        pass  # keep the terminal quiet


def cmd_auth(args):
    client_id, client_secret = load_config()
    state = secrets.token_urlsafe(24)
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    # One-shot loopback server, bound to localhost only.
    server = http.server.HTTPServer(("127.0.0.1", CALLBACK_PORT), _CallbackHandler)
    server.timeout = 300
    print("Opening browser to authorize with LinkedIn...")
    print(f"If it doesn't open, visit:\n  {url}\n")
    webbrowser.open(url)
    server.handle_request()  # blocks until the redirect hits, or timeout

    if _CallbackHandler.code is None:
        die("no authorization code received (timed out or denied)")
    if _CallbackHandler.state != state:
        die("OAuth state mismatch — possible CSRF, aborting")

    token_data = {
        "grant_type": "authorization_code",
        "code": _CallbackHandler.code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    _require_https(TOKEN_URL, "token exchange")
    body = urllib.parse.urlencode(token_data).encode()
    req = urllib.request.Request(
        TOKEN_URL, data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            tok = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        die(f"token exchange failed {e.code}: {e.read().decode(errors='replace')[:300]}")

    # Resolve the member URN so posting doesn't need another round-trip.
    info, _ = _http_json(USERINFO_URL, {"Authorization": f"Bearer {tok['access_token']}"})
    tok["sub"] = info.get("sub")
    tok["name"] = info.get("name")
    save_token(tok)
    print(f"Authenticated as {info.get('name')} (urn:li:person:{info.get('sub')}).")
    print(f"Token saved to {TOKEN_PATH} (0600). Expires in ~{tok.get('expires_in', 0)//86400} days.")


def cmd_whoami(args):
    tok = load_token()
    info, _ = _http_json(USERINFO_URL, {"Authorization": f"Bearer {tok['access_token']}"})
    out = {"name": info.get("name"), "urn": f"urn:li:person:{info.get('sub')}"}
    print(json.dumps(out, indent=2) if args.json else f"{out['name']}  ({out['urn']})")


# --- Posting ----------------------------------------------------------------
def _auth_headers(tok):
    return {
        "Authorization": f"Bearer {tok['access_token']}",
        "LinkedIn-Version": API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def _upload_image(tok, path):
    """Register + upload one image, return its urn:li:image:... id."""
    if not os.path.isfile(path):
        die(f"image not found: {path}")
    size = os.path.getsize(path)
    if size > MAX_IMAGE_BYTES:
        die(f"image too large ({size} bytes > {MAX_IMAGE_BYTES})")
    owner = f"urn:li:person:{tok['sub']}"
    init, _ = _http_json(
        IMAGES_URL + "?action=initializeUpload",
        _auth_headers(tok),
        data={"initializeUploadRequest": {"owner": owner}},
    )
    value = init.get("value", {})
    upload_url = value.get("uploadUrl")
    image_urn = value.get("image")
    if not upload_url or not image_urn:
        die(f"unexpected initializeUpload response: {init}")
    # Defense-in-depth: only ever PUT bytes to a linkedin.com host.
    host = urllib.parse.urlparse(upload_url).hostname or ""
    if not (host == "linkedin.com" or host.endswith(".linkedin.com")):
        die(f"refusing to upload to non-LinkedIn host: {host}")
    _require_https(upload_url, "image upload")
    with open(path, "rb") as f:
        img_bytes = f.read()
    req = urllib.request.Request(
        upload_url, data=img_bytes, method="PUT",
        headers={"Authorization": f"Bearer {tok['access_token']}"},
    )
    try:
        urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        die(f"image upload failed {e.code}: {e.read().decode(errors='replace')[:300]}")
    return image_urn


def _publish(tok, text, image_paths):
    author = f"urn:li:person:{tok['sub']}"
    image_urns = [_upload_image(tok, p) for p in image_paths]
    payload = {
        "author": author,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if len(image_urns) == 1:
        payload["content"] = {"media": {"id": image_urns[0]}}
    elif len(image_urns) > 1:
        payload["content"] = {
            "multiImage": {"images": [{"id": u} for u in image_urns]}
        }
    _, headers = _http_json(POSTS_URL, _auth_headers(tok), data=payload)
    return headers.get("x-restli-id") or headers.get("X-RestLi-Id") or "(posted)"


def _resolve_text(args):
    if args.text_file:
        with open(args.text_file) as f:
            return f.read().strip()
    if args.text:
        return args.text
    die("no post text", hint="use --text '...' or --text-file path")


def cmd_post(args):
    tok = load_token()
    text = _resolve_text(args)
    post_id = _publish(tok, text, args.image or [])
    print(json.dumps({"status": "posted", "post_id": post_id}, indent=2)
          if args.json else f"Posted. id={post_id}")


# --- Scheduling -------------------------------------------------------------
def _parse_when(s):
    """Accept 'YYYY-MM-DD HH:MM' or ISO 8601. Naive = local time."""
    s = s.strip().replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.astimezone()  # attach local tz
        except ValueError:
            continue
    die(f"could not parse time: {s!r}", hint="use 'YYYY-MM-DD HH:MM' (local time)")


def cmd_schedule(args):
    load_token()  # fail fast if not authed
    text = _resolve_text(args)
    when = _parse_when(args.at)
    for p in args.image or []:
        if not os.path.isfile(p):
            die(f"image not found: {p}")
    ensure_state_dirs()
    job_id = datetime.now().strftime("%Y%m%d-%H%M%S-") + secrets.token_hex(3)
    job = {
        "id": job_id,
        "run_at": when.isoformat(),
        "text": text,
        "images": [os.path.abspath(p) for p in (args.image or [])],
        "created_at": datetime.now().astimezone().isoformat(),
    }
    path = os.path.join(JOBS_DIR, job_id + ".json")
    with open(path, "w") as f:
        json.dump(job, f, indent=2)
    print(json.dumps({"status": "scheduled", "id": job_id, "run_at": job["run_at"]}, indent=2)
          if args.json else f"Scheduled {job_id} for {job['run_at']}")


def _load_jobs():
    if not os.path.isdir(JOBS_DIR):
        return []
    jobs = []
    for name in sorted(os.listdir(JOBS_DIR)):
        if name.endswith(".json"):
            with open(os.path.join(JOBS_DIR, name)) as f:
                jobs.append(json.load(f))
    return jobs


def cmd_list(args):
    jobs = _load_jobs()
    if args.json:
        print(json.dumps(jobs, indent=2))
        return
    if not jobs:
        print("No scheduled posts.")
        return
    for j in jobs:
        imgs = f" [{len(j['images'])} img]" if j["images"] else ""
        preview = j["text"].replace("\n", " ")[:50]
        print(f"{j['id']}  {j['run_at']}{imgs}  {preview}")


def cmd_cancel(args):
    path = os.path.join(JOBS_DIR, args.id + ".json")
    if not os.path.exists(path):
        die(f"no such job: {args.id}", hint="linli list")
    os.remove(path)
    print(f"Cancelled {args.id}")


def cmd_run(args):
    tok = load_token()
    print(f"Scheduler running (checking every {args.interval}s). Ctrl-C to stop.")
    try:
        while True:
            now = datetime.now(timezone.utc)
            for job in _load_jobs():
                run_at = datetime.fromisoformat(job["run_at"])
                if run_at.astimezone(timezone.utc) <= now:
                    print(f"[{datetime.now().astimezone().isoformat()}] posting {job['id']}...")
                    try:
                        tok = load_token()  # re-read in case it was refreshed
                        pid = _publish(tok, job["text"], job.get("images", []))
                        print(f"  posted id={pid}")
                        os.remove(os.path.join(JOBS_DIR, job["id"] + ".json"))
                    except SystemExit:
                        # _publish/die called sys.exit; keep the loop alive so one
                        # bad job doesn't kill the scheduler.
                        print(f"  FAILED {job['id']} — leaving it queued for retry")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def cmd_nuke(args):
    import shutil
    if not args.yes:
        die("refusing to nuke without --yes",
            hint="linli nuke --yes  (deletes token + all queued posts)")
    if os.path.isdir(STATE_DIR):
        shutil.rmtree(STATE_DIR)
    print("Wiped all local state (token + queued posts).")
    print(f"To remove the tool entirely: rm -rf {BASE_DIR}")


# --- CLI --------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(prog="linli", description="Throwaway local LinkedIn scheduler.")
    p.add_argument("--json", action="store_true", help="JSON output where applicable")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("auth", help="OAuth login (opens browser)").set_defaults(func=cmd_auth)
    sub.add_parser("whoami", help="Show logged-in member").set_defaults(func=cmd_whoami)

    sp = sub.add_parser("post", help="Post now")
    sp.add_argument("--text")
    sp.add_argument("--text-file")
    sp.add_argument("--image", action="append", help="Local image path (repeatable)")
    sp.set_defaults(func=cmd_post)

    ss = sub.add_parser("schedule", help="Queue a post for later")
    ss.add_argument("--at", required=True, help="'YYYY-MM-DD HH:MM' local time")
    ss.add_argument("--text")
    ss.add_argument("--text-file")
    ss.add_argument("--image", action="append", help="Local image path (repeatable)")
    ss.set_defaults(func=cmd_schedule)

    sub.add_parser("list", help="List queued posts").set_defaults(func=cmd_list)

    sc = sub.add_parser("cancel", help="Remove a queued post")
    sc.add_argument("id")
    sc.set_defaults(func=cmd_cancel)

    sr = sub.add_parser("run", help="Foreground scheduler loop")
    sr.add_argument("--interval", type=int, default=30, help="Poll seconds (default 30)")
    sr.set_defaults(func=cmd_run)

    sn = sub.add_parser("nuke", help="Delete all local state")
    sn.add_argument("--yes", action="store_true")
    sn.set_defaults(func=cmd_nuke)
    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
