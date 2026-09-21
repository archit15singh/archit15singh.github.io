# linli — throwaway local LinkedIn scheduler

Post text + local images to LinkedIn, now or on a schedule, straight through
LinkedIn's official API. No Docker, no third-party service, no dependencies
beyond the Python standard library. Everything lives in this one directory, so
tearing it down is `rm -rf ~/linli`.

## One-time setup

1. Create a LinkedIn developer app: https://www.linkedin.com/developers/apps
2. On the **Products** tab add both:
   - *Sign In with LinkedIn using OpenID Connect*
   - *Share on LinkedIn*
3. On the **Auth** tab set an authorized redirect URL to exactly:
   `http://localhost:8765/callback`
4. Copy the app's Client ID and Client Secret, then either:
   ```bash
   export LINKEDIN_CLIENT_ID=xxxx
   export LINKEDIN_CLIENT_SECRET=yyyy
   ```
   or `cp config.example.json config.json`, fill it in, and `chmod 600 config.json`.

## Use

```bash
cd ~/linli

./linli auth                       # opens a browser, logs you in once
./linli whoami                     # confirms the token works

# post right now
./linli post --text "Shipped a thing today." --image ~/Pictures/ship.png

# schedule for later (local time); repeat --image for a multi-image post
./linli schedule --at "2026-09-23 10:00" --text-file ~/notes/post.md \
    --image ~/Pictures/a.png --image ~/Pictures/b.png

./linli list                       # see the queue
./linli cancel 20260923-100000-abc123

# run the scheduler in the foreground — it posts due jobs, Ctrl-C to stop.
# nothing is installed to cron/launchd; close the terminal and it's gone.
./linli run

# wipe everything
./linli nuke --yes                 # deletes token + queue
rm -rf ~/linli                     # removes the tool itself
```

`--json` before the subcommand gives machine-readable output where it applies.

## How scheduling works

LinkedIn's API has no server-side scheduling for personal profiles, so the
schedule is local: `schedule` writes a small JSON job under `state/jobs/`, and
`run` is a foreground loop that posts any job whose time has passed, then
deletes it. A failed post stays queued and is retried on the next tick. There
is **no** system cron or launchd entry — the schedule only fires while `run` is
active, by design (ephemeral, nothing left behind).

## Security notes (audited)

- **Local only.** The only network hosts contacted are `www.linkedin.com` and
  `api.linkedin.com`. Every request is asserted HTTPS; the image upload target
  is additionally checked to be a `*.linkedin.com` host before any bytes go out.
- **Secrets at rest.** The OAuth token is written `0600` (created with a
  restrictive mode, not chmod-after-write). `state/` is `0700`. If you use
  `config.json`, the tool refuses to run unless it's `0600`.
- **No secret ever hits stdout/stderr or logs.** `whoami`/`list` print name and
  URN only; the access token and client secret are never echoed.
- **OAuth CSRF.** A random `state` is generated and verified on the callback.
  The callback server binds to `127.0.0.1` only, handles exactly one request,
  and times out after 5 minutes.
- **No stored input prompts.** All inputs are CLI flags; the tool never calls
  `input()`/`getpass()`. Post text can come from `--text-file` to keep content
  out of shell history.
- **Bounded uploads.** Images must be regular files under 20 MB.
- **No telemetry, no analytics, no auto-refresh tokens.** When the ~60-day
  token expires the tool tells you to re-run `auth` rather than silently
  hoarding a refresh token.

## Uninstall

```bash
./linli nuke --yes && rm -rf ~/linli
```

That's the whole footprint. (If you also want back the Docker VM RAM bumped
during earlier exploration: `colima stop && colima start --cpu 2 --memory 2`.)
