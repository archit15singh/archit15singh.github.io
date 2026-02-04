# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site blog using the **PaperMod** theme, deployed to GitHub Pages. The site features technical writing on AI, systems thinking, cognitive science, and software engineering.

## Build Commands

### Local Development
- `hugo server -D` — Start local dev server with drafts enabled
- `hugo server` — Start local dev server without drafts (production mode)

### Production Build
- `hugo --minify --cleanDestinationDir` — Production build (outputs to `public/`)
- Always run production build locally before pushing to verify posts are included

### Testing
- After creating or modifying posts, run `hugo --minify --cleanDestinationDir` locally to verify the post appears in `public/`
- Check `public/index.html` and `public/posts/` to confirm post is built

## Critical Configuration: Future Dates

**IMPORTANT**: `buildFuture: false` is set in `config.yml`

- Posts with future dates will NOT be built in production
- Always use past or current dates in frontmatter to ensure posts are published
- If a post doesn't appear after build, check the date first

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

## Common Tasks

### Creating a New Post

1. Create file in `content/posts/` with naming convention: `YYYY-MM-DD-slug.md`
2. Add required frontmatter (see Content Conventions above)
3. Use a **past or current date** (not future)
4. Add banner image to `static/images/uploads/` if needed
5. Test locally: `hugo server`
6. Verify build: `hugo --minify --cleanDestinationDir`
7. Check `public/posts/` to confirm post is generated
8. Commit and push to auto-deploy

### Adding Images

1. Place image in `static/images/uploads/`
2. Reference in Markdown: `/images/uploads/filename.webp`
3. For cover images, use frontmatter `cover.image` field

### Modifying Site Configuration

- Edit `config.yml` for site-wide settings
- Test changes with `hugo server`
- Verify build before pushing

### Debugging Missing Posts

1. Check post date in frontmatter (must be past/current)
2. Check for `draft: true` in frontmatter
3. Run production build locally: `hugo --minify --cleanDestinationDir`
4. Inspect `public/posts/` and `public/index.html`
5. Check Hugo build output for errors

## Code Style

- **Configuration**: YAML (`.yml` extension)
- **Content**: Markdown with YAML frontmatter
- **Frontmatter**: Keep keys consistent with existing posts
- **Indentation**: 2 spaces for YAML

## Important Files to Reference

- `config.yml` — All site configuration, theme settings, menus
- `content/posts/2026-01-26-ai-augmented-developer-playbook.md` — Example of complete frontmatter
- `.github/workflows/gh-pages.yml` — Deployment workflow
- `layouts/partials/analytics.html` — Analytics implementation
