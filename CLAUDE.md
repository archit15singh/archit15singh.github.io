# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

- `hugo server -D` — Local dev server with drafts
- `hugo server` — Local dev server (production mode)
- `hugo --minify --cleanDestinationDir` — Production build to `public/`

## Local Development Server

**URL**: http://localhost:1313/

**Start**: `hugo server` (or `hugo server -D` to include drafts)

**When to use**: Before pushing changes to preview posts, test layouts, verify images, and catch issues locally. The server auto-reloads on file changes.

## Critical: buildFuture Configuration

**`buildFuture: false` is set in config.yml**

Posts with future dates will NOT be built. Always use past/current dates in frontmatter. If a post doesn't appear after build, check the date first.

## Debugging Missing Posts

1. Check date in frontmatter (must be past/current, not future)
2. Check for `draft: true` in frontmatter
3. Run `hugo --minify --cleanDestinationDir` and inspect `public/posts/`

## Playwright

Use `playwright screenshot --full-page --viewport-size="1280,3000" <url> <output.png>` for full-page screenshots. Run `playwright --help` for all commands.

## GitHub CLI

Use `gh` for GitHub operations (issues, PRs, runs, releases) instead of web scraping—it's faster and more reliable. Run `gh --help` for all commands.

## Architecture: Hugo + PaperMod

This site uses **Hugo with the PaperMod theme** as a git submodule (`themes/hugo-PaperMod/`). Customizations are minimal and isolated:

- **Custom partials** (`layouts/partials/`): Only `analytics.html`, `extend_footer.html`, `extend_head.html` — for GoatCounter analytics, footer mods, and head meta tags
- **Theme inheritance**: Layout files from the submodule are extended via Hugo's `extends` block, not replaced
- **No custom CSS/JS**: Styling is theme-provided (Tailwind-based); modifications go through config.yml parameters, not custom assets

**To modify the theme**: Edit `layouts/partials/` or `config.yml` params, not the submodule itself. The submodule is read-only from this repo's perspective.

## Post Creation Workflow

Posts live in `content/posts/` with filename pattern: `YYYY-MM-DD-slug.md`

**Required frontmatter fields**:
```yaml
title: "Post Title"
description: "Short description for SEO and feeds"
date: YYYY-MM-DDTHH:MM:SS+05:30  # Use +05:30 timezone; must be past/current (buildFuture: false)
tags: [Tag1, Tag2]
categories: [Category]
cover:
  image: "/images/uploads/image.jpg"
  alt: "Alt text"
  hidden: false
```

**Key behaviors**:
- Posts are auto-ordered by date descending on the homepage
- Archive page (`content/archives.md`) lists all posts
- Search functionality (`content/search.md`) queries full text
- Reading time is auto-calculated from word count

## Image Handling

Images are configured to auto-convert to **WebP** (`image_format: webp` in config.yml).

- Place images in `static/images/uploads/`
- Reference in frontmatter as `/images/uploads/filename.jpg` (Hugo handles WebP conversion at build time)
- Use Playwright to screenshot previews: `playwright screenshot --full-page http://localhost:1313/posts/slug/ preview.png`

## Text-to-Speech ("Listen to this post")

Client-side player using the Web Speech API — no audio files, no deps, no build changes.

- **Toggle**: `params.tts.enabled` in config.yml (global); set `tts: false` in a post's frontmatter to hide it on that post.
- **Files**: `layouts/_default/single.html` (override of the theme's, byte-identical except the injected `partial "listen.html"` above `.post-content`), `layouts/partials/listen.html` (player markup + scoped inline CSS), `static/js/listen.js` (speech logic, deferred, loaded only on post pages).
- **Behavior**: text is read from `.post-content`, split into ≤220-char sentence chunks (Chrome/Safari cut long utterances after ~15s), code blocks/pre/footnotes skipped, active paragraph highlighted + auto-scrolled into view, **click any paragraph to start reading from there**, **voice picker** (persisted in `localStorage`, with a 250ms poll fallback because Safari sometimes never fires `voiceschanged`), **progress %** in the status bar, rate toggle 1x–2x, `<`/`>` sanitized to full-width on iOS 26 (a leading `<` bricks all speech until browser restart), watchdog restarts a stalled chunk on flaky mobile synthesizers, pause is cancel+resume (Android `pause()` cancels), `speechSynthesis.cancel()` on unload. **Only state changes announce to screen readers** (sr-only `lp-announce` live region); the visible `lp-status` updates every chunk without touching `aria-live`. A GoatCounter event (`tts listen`) fires on first play.
- **Verify**: `hugo server` then `node /var/folders/3d/y46y2yvs7pz05l35lp_1wjzc0000gn/T/opencode/tts-test.js` (asserts state machine + no console errors). Player appears on `public/posts/*/index.html`, never on the homepage.

## Hugo Gotchas

- **`default` treats `false` as empty**: `(.Param "tts") | default true` returns `true` even when frontmatter sets `tts: false`. Use `and .Site.Params.tts.enabled (ne (.Param "tts") false)` for a per-post opt-out.
- When overriding a theme template, keep it a byte-identical copy + injection, so upstream `git diff` against the submodule stays a one-liner.
- **`gh` resolves to the submodule's repo**: with `themes/hugo-PaperMod` present, `gh run list` / `gh repo view` target `adityatelange/hugo-PaperMod`. Always pass `-R archit15singh/archit15singh.github.io`.

## Site Configuration Hotspots

Key settings in `config.yml` that affect behavior:

| Setting | Impact |
|---------|--------|
| `buildFuture: false` | Posts with future dates are invisible |
| `buildDrafts: false` | Posts with `draft: true` are invisible |
| `params.DateFormat` | How dates render in post headers |
| `params.goatcounter: "architsingh"` | Analytics; remove if not used |
| `languages.en.menu.main` | Navigation menu items (Archive, Search, Tags) |

## Content Enrichment Loop (Staff+ post workflow)

A repeatable loop was used to recursively enrich the Staff+ operating-model post (content/posts/2026-08-30-the-staff-plus-operating-model.md) from primary sources. It ran 4 rounds in one session (reaching the then-dry point), then a later session ran a further 10 productive rounds (312→358 lines) plus one dry confirm pass. Patterns that worked:

- **Round pattern**: websearch on genuinely-thin sub-areas → find primary sources (staffeng.com, lethain.com, leaddev.com, noidea.dog/glue, blog4ems, greatcircle.com IC piece) → weave only *additive* (non-redundant) insight into existing sections (no new headings) → run anti-slop check → hugo build → commit + push main.
- **Loop artifacts**: `.enrich-loop/ledger.tsv` (round/queries/new_sources/areas/dry) tracks saturation. The in-memory ledger survives across my session but isn't committed; keep it updated if resuming.
- **Anti-slop for edits**: after each edit run `rg --pcre2` for Tier-1 banned words + check em-dash count per new paragraph (target ≤2). The post's existing voice uses em dashes heavily; keep *newly added* blocks lean.

### Gotchas
- **Semantic Scholar keyless rate limit**: `lit_search.py search` returned `HTTP 429` with no S2_API_KEY (1 req/s limits). For this kind of practitioner-topic research, plain `websearch`/`webfetch` was the right tool anyway — the canon is blog posts/books, not papers.
- **Saturation is qualitative here**: "100% coverage" ended up meaning "every operating capability the primary canon surfaces is developed somewhere in the post," not "every possible source cited." 4 rounds hit the point where further searches stopped adding distinct capabilities (measure: fresh rounds adding 0 new capabilities → dry).
- **Banned-word check nuance**: "leverage" as noun/adjective (e.g. "highest-leverage", "reads as leverage") is fine; only *verb* usage is banned. The regex `\bleverage\b(?!s)(?=\s+(the|this|to|a)...)` catches the verb form — and also false-positives on adjective "high-leverage", so eyeball any hit before "fixing" it.
- **Anti-slop regex false positives**: the `rg "not just .* but "` pattern over-matches legitimate contrasts where "but" simply appears later in the sentence with no crutch structure (e.g. "map who holds influence, not just the org chart, and notice..." — no "but Y"). Also `rg "—"` counting em dashes across a multi-line `sed` window can catch a *pre-existing* adjacent line; restrict the window to exactly the new paragraph before judging the count.
- **Lit_search is single-token under zsh**: don't store `python3 .../lit_search.py` in a variable; call the executable path directly.
- **Prior "convergence" is session-local and fragile**: the R35 ledger entry declared the post saturated, yet a fresh continuation session (R36-42) surfaced six genuinely-distinct operating capabilities (design-review ritual, error-budget contract, kill-criteria, calibration seat, external visibility, situational leadership) from re-searching thin sub-areas. A "confirmed convergence" from an earlier round is NOT proof of saturation — each rerun must probe genuinely-thin, canonical areas (reliability/decision/people-development seams) rather than trusting the ledger. True convergence only holds after THIS session produces consecutive dry rounds.
- **Second-wave thin seams that paid off** (from the R36-42 continuation): decision/reliability mechanics (error budgets, kill-criteria), running-ritual mechanics (design/architecture reviews), and people-development frameworks (situational leadership, calibration seat, external visibility), all classic-but-previously-skipped canon. Keep newly added blocks at zero em-dashes and zero Tier-1 words to stay lean against a post that's now ~20.5k words.

## Reading-List Enrichment Loop (content/posts/2023-01-01-my-reading-list.md)

Same recursive loop applied to the decade-long reading list (~80 flat books → 107 annotated entries across 15 domains). Ledger lives in `.enrich-loop/reading-list-ledger.tsv`. Saturation was reached after 9 productive rounds + 1 dry confirm. Notes that differ from the Staff+ loop:

- **Books, not papers**: plain `websearch` on "best/canonical X books" is the right tool; no lit-search needed. Good sources: goodreads (for community-vetted canonical status + author bios), publisher catalogs (MIT Press, O'Reilly, Cambridge, Springer), and best-of lists.
- **Confirm passes repeatedly uncovered real gaps** — the "dry" signal is unreliable on a first pass. Rounds that looked dry (agentic UX, cybernetics, causal ML) each found at least one genuinely missing canonical book. Only consecutive all-dry rounds confirm convergence, same lesson as Staff+ R35→R36.
- **Goodreads `webfetch` returns a huge review dump** (hundreds of lines) — useful for identifying a book + canon status, wasteful to read fully. Fetch to identify title/author/year, then write the annotation from the description, not the reviews.
- **One em-dash per annotation max, zero Tier-1 words** — annotations are one sentence each, so keep them lean; the `rg --pcre2 'not just .* but'|tapestry|paradigm|holistic|...` check runs clean before each commit.
- **`(Additions)` was a meta-label in the original post** (internal provenance leak) that should be removed at publication — never leak internal methodology; rename to the plain domain name.
- **User-sourced additions (e.g. Rishit's recs) are high value**: Logicomix, Jaynes' *Probability Theory*, Feynman Lectures, Drexler's *Nanosystems* came from a friend, not search, and filled real gaps (including a whole new "Foundations: probability/physics/molecular machinery" domain). When the owner routes in human recommendations, add them with proper annotations rather than treating search as the only source.
