---
name: check-website-links
description: Scan the whole Hugo site for broken links (internal pages, images, anchors, external URLs) after a build, fix what is broken, and push. Use when the user asks to check or fix broken links on the site, validate a post's links before publishing, or hunt 404s and missing anchors across the website.
---

# Check Website Links

1. Build the site: `hugo --minify --cleanDestinationDir`
2. Run the scanner: `python3 .claude/skills/check-website-links/scripts/check-links.py --dir public --base "https://archit15singh.github.io/"`
3. Read the report. Each line is one broken thing:
   - `404` — an internal page, image, or file does not exist.
   - `anchor` — the page exists but the `#fragment` is not on it.
   - `external` — an external URL failed (only shown with `--external`).
4. For each broken link, fix the source of truth:
   - Wrong URL in a post/page: edit `content/**` frontmatter or body.
   - File renamed/moved: point the link at the new slug, or keep the old slug.
   - Anchor changed: update the link to the real heading id.
5. Rebuild and rerun until the report is clean.
6. For external failures, double-check by hand (Cloudflare/bot-blocking causes false positives) before touching anything.
7. Commit the fixes and push.

## Gotchas

- Bare `#` and `#top` are ignored (theme scroll-to-top). `#comments` is ignored for pages with `comments: false`.
- Hugo minifies HTML, so heading ids render unquoted (`id=the-problem-is-search`). The scanner matches both quoted and unquoted forms.
- Posts link to `public/posts/slug/index.html` via clean URLs; the scanner resolves both `/slug/` and `/slug`.
- **`--base` is required**: absolute links to the site's own domain (e.g. `/apple-touch-icon.png`) resolve locally against `public/`; without it they are treated as live-site requests and 404 until the push deploys.
- External links are only verified with `--external`; run that as a separate pass and eyeball each failure, since many sites block scripted requests. Known bot-blocking noise to ignore: GitHub `429` (rate limit), LinkedIn `999`/`405`, Twitter/X share intents `403`, Facebook sharer `400`, and `crates.io` HEAD `404` (real browsers get `200`).