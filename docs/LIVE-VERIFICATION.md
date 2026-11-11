# Change, deploy and verify

Use this workflow for site content, layout, styling, scripts and deployment changes. Keep a coverage checklist in the PR: route/control, observed result, issue and verification status. An HTTP 200 is not visual verification.

## Before merging

1. Work on `archits/pr/<name>`. Read `CLAUDE.md` and inspect the current diff.
2. Build with `hugo --gc --minify -d /tmp/hugo-verify`; run `bash scripts/check-homepage.sh` and `python3 scripts/check-site.py /tmp/hugo-verify`.
3. Preview in Brave. Compare changed layouts, scroll to the bottom, click links, test keyboard focus and check narrow and wide views in both themes. For an interactive failure, inspect the browser console and reproduce the exact action before editing.
4. Open a PR with evidence and gaps. Merge only with current authorization. Confirm merged `main` builds locally.

## After deployment

1. Wait for both the main Hugo workflow and the `gh-pages` Pages deployment to succeed. Fetch production with a cache-busting query to confirm new content, then test ordinary URLs too.
2. Use computer use on **production**: home → each navigation item → project detail → article → related reading; Speaking → recording; Contact → its linked pages; Search → query → result; archive → post; pagination and footer. Scroll each affected page. Test speech controls on an article and theme/skip navigation. Inspect mailto destinations without sending mail; external login or blocked destinations remain explicitly unverified.
3. Check loaded CSS/JS/images, including stylesheet integrity. A working homepage does not prove inner pages work. Cached HTML can reference deleted fingerprinted assets after deployment; preserve published immutable assets and verify an older URL still loads.
4. Reproduce issues, make scoped fixes on a new branch, verify locally, PR/merge and repeat the failing production path. Stop when the checklist is clear; report untested paths rather than calling partial coverage complete.

Browser unavailable or concurrently controlled? Preserve the checklist/checkpoint and report that limit. Resume UI checks when available; source inspection and curl are complementary evidence, not substitutes for rendered interaction.

Deployment retains only fingerprinted CSS/JS using `scripts/retain-published-assets.py`. Its recent-history recovery restores previously deleted hashes; the latest published tree then carries them forward. Preserve this step when changing deployment tooling. Ordinary HTML and removed content are still replaced each deployment.
