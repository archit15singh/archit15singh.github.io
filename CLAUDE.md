# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hugo static site using the **PaperMod** theme, deployed to GitHub Pages via GitHub Actions.

## Build Commands

- `hugo server -D` — Local dev server with drafts
- `hugo server` — Local dev server (production mode)
- `hugo --minify --cleanDestinationDir` — Production build to `public/`

## Critical: buildFuture Configuration

**`buildFuture: false` is set in config.yml**

Posts with future dates will NOT be built. Always use past/current dates in frontmatter. If a post doesn't appear after build, check the date first.

## Architecture

```
.
├── config.yml              # Main site configuration
├── configTaxo.yml          # Taxonomy and privacy settings (legacy, mostly duplicated in config.yml)
├── content/
│   ├── posts/              # Blog posts (Markdown with YAML frontmatter)
│   │   └── YYYY-MM-DD-slug.md
│   ├── archives.md         # Archive page
│   └── search.md           # Search page
├── static/
│   ├── images/uploads/     # Blog post images (prefer webp format)
│   └── [favicons, etc.]    # Root-level static assets
├── layouts/partials/       # Custom template overrides
│   ├── analytics.html      # GoatCounter analytics
│   ├── extend_footer.html  # Footer customizations
│   └── extend_head.html    # Head customizations
├── themes/hugo-PaperMod/   # Theme (do not modify directly)
├── public/                 # Build output (git-ignored, generated)
└── .github/workflows/
    └── gh-pages.yml        # Auto-deployment to GitHub Pages
```

### Key Concepts

- **Hugo**: Static site generator that converts Markdown + templates → HTML
- **PaperMod Theme**: Pre-built theme providing layouts, styles, and components
- **Frontmatter**: YAML metadata at the top of each Markdown file
- **Taxonomies**: Categories, tags, and series for content organization
- **Layouts override**: Files in `layouts/` override theme templates

## Content Conventions

### Post Frontmatter

All posts in `content/posts/` require YAML frontmatter with these fields:

```yaml
---
title: "Post Title"
description: "SEO-friendly description"
date: 2026-01-26T10:00:00.000Z  # ISO 8601 format, USE PAST DATES
tags:
  - AI
  - Development
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/post-banner.webp"  # Prefer webp format
  alt: "Alt text for accessibility"
  caption: "Optional caption"
showToc: true
TocOpen: true
---
```

### File Naming

- Posts: `YYYY-MM-DD-slug.md` (e.g., `2026-01-26-ai-augmented-developer-playbook.md`)
- Images: `descriptive-name.webp` in `static/images/uploads/`

### Image Paths

- Cover images: `/images/uploads/filename.webp` (leading slash = root of `static/`)
- Prefer `webp` format for performance
- Images are copied as-is from `static/` to `public/` during build

## Deployment

- **Auto-deploys** on push to `main` via GitHub Actions (`.github/workflows/gh-pages.yml`)
- No manual deployment step needed
- Workflow runs: Checkout → Setup Hugo → Build → Deploy to `gh-pages` branch
- Use `draft: true` in frontmatter for unpublished posts
  - `hugo server -D` shows drafts locally
  - Production build ignores drafts

## Site Configuration

### Primary Config (`config.yml`)

- `baseURL`: Site URL (required for proper link generation)
- `theme`: Must be `hugo-PaperMod`
- `buildFuture: false`: Critical setting affecting publication
- `params.goatcounter`: Analytics identifier
- `params.homeInfoParams`: Homepage content
- `menu.main`: Navigation links (Archive, Search, Tags)
- `outputs.home`: Enables HTML, RSS, JSON (JSON required for search)

### Theme Customization

- Override theme templates by placing files in `layouts/` with same path structure
- Custom partials in `layouts/partials/`:
  - `analytics.html`: GoatCounter tracking
  - `extend_footer.html`: Footer additions
  - `extend_head.html`: Head additions

## Creating a New Post

1. Create `content/posts/YYYY-MM-DD-slug.md`
2. Add required frontmatter (see Content Conventions above) with **past/current date**
3. Add images to `static/images/uploads/` (reference as `/images/uploads/filename.webp`)
4. Test with `hugo server` then verify with production build
5. Push to `main` to auto-deploy

## Debugging Missing Posts

1. Check date in frontmatter (must be past/current, not future)
2. Check for `draft: true` in frontmatter
3. Run `hugo --minify --cleanDestinationDir` and inspect `public/posts/`
