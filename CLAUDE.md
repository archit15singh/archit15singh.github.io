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

## Site Configuration Hotspots

Key settings in `config.yml` that affect behavior:

| Setting | Impact |
|---------|--------|
| `buildFuture: false` | Posts with future dates are invisible |
| `buildDrafts: false` | Posts with `draft: true` are invisible |
| `params.DateFormat` | How dates render in post headers |
| `params.goatcounter: "architsingh"` | Analytics; remove if not used |
| `languages.en.menu.main` | Navigation menu items (Archive, Search, Tags) |
