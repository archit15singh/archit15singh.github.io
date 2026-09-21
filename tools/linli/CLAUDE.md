# linli — agent guide (when / how / why)

`linli` is a self-contained, zero-dependency CLI that posts to LinkedIn through
LinkedIn's official REST API — either immediately or on a local schedule. It is
deliberately throwaway: everything (token, queued posts) lives under the tool's
own directory, so uninstalling is one `rm -rf`.

## When to use it

Reach for `linli` when the user wants to:
- **Post to LinkedIn from the command line** with text and/or local image files.
- **Schedule a LinkedIn post** for a specific date/time without a paid tool
  (Buffer, Hootsuite, MagicPost, etc.).
- Automate posting from a script (`--json` output, non-interactive flags).

Do **not** use it for: reading the feed, analytics, commenting, company-page
posting to a page you don't administer, or anything needing a LinkedIn product
the app hasn't been granted.

## Why it exists (design intent)

- **Free + local.** No SaaS, no Docker, no server. Stdlib-only Python 3.
- **Official API, so no account-ban risk** — unlike browser-automation tools
  that log in as the user and click.
- **Ephemeral by design.** Scheduling is a foreground loop (`run`), not a cron
  or launchd entry, so nothing persists after the terminal closes. This is a
  feature, not a limitation: a scheduled post only fires while `run` is active.

## How to use it

Prereq (one time, done by the human): a LinkedIn developer app with the
products *Sign In with LinkedIn using OpenID Connect* and *Share on LinkedIn*,
redirect URL `http://localhost:8765/callback`, and env vars
`LINKEDIN_CLIENT_ID` / `LINKEDIN_CLIENT_SECRET` (or a `0600` `config.json`).
Full setup is in `README.md`.

```bash
cd <this-dir>            # or wherever the user keeps their copy (e.g. ~/linli)
./linli auth             # opens a browser once; stores a 0600 token
./linli whoami           # verify the token resolves a member

./linli post --text "..." --image ~/a.png            # post now
./linli schedule --at "2026-09-23 10:00" \
    --text-file post.md --image a.png --image b.png  # queue for later
./linli list                                         # show the queue
./linli cancel <job-id>                              # drop one
./linli run                                          # foreground scheduler
./linli nuke --yes                                   # wipe token + queue
```

Notes for agents:
- Prefer `--text-file` over `--text` for multi-line or sensitive copy (keeps it
  out of shell history).
- `--image` is repeatable; one image → single-image post, many → multi-image.
- `--json` (before the subcommand) gives machine-readable output for `whoami`,
  `post`, `schedule`, `list`.
- The scheduler only posts while `./linli run` is in the foreground. If the user
  wants "set and forget," tell them that explicitly — do not silently install a
  cron entry (the tool intentionally never does).
- Times are parsed as **local** time (`YYYY-MM-DD HH:MM`).

## Safety invariants (do not regress these when editing)

- Only ever contacts `api.linkedin.com` / `www.linkedin.com`; all requests are
  asserted HTTPS and the image-upload host is checked to be `*.linkedin.com`.
- Token file is `0600`, `state/` is `0700`, `config.json` must be `0600`.
- No secret is ever printed; no `input()`/`getpass()`/`eval`/`exec`/`subprocess`.
- OAuth uses a random `state` (CSRF) and a one-shot `127.0.0.1`-only callback.
- `config.json` and `state/` are gitignored — never commit them.
