# AGENTS.md

## Build Commands
- `hugo server -D` — Local dev server with drafts
- `hugo --minify --cleanDestinationDir` — Production build (outputs to `public/`)
- Always run production build locally before pushing to verify posts are included

## Important: Future Dates
- `buildFuture: false` is set in config.yml — posts with future dates will NOT be built
- Always use past or current dates in frontmatter to ensure posts are published

## Architecture
This is a Hugo static site using the **PaperMod** theme, deployed to GitHub Pages via `.github/workflows/gh-pages.yml`.

- `content/posts/` — Blog posts in Markdown with YAML frontmatter (format: `YYYY-MM-DD-slug.md`)
- `config.yml` — Site configuration (theme, params, menus, taxonomies)
- `static/` — Static assets (copied as-is to `public/`)
- `layouts/` — Custom template overrides
- `themes/hugo-PaperMod/` — Theme (do not modify directly)

## Content Conventions
- Posts require frontmatter: `title`, `description`, `date`, `tags`, `categories`
- Use `cover.image` for post banners; prefer `/images/uploads/` path and `webp` format
- Date format in frontmatter: ISO 8601 (`2026-01-26T10:00:00.000Z`)

## Code Style
- YAML for config; Markdown for content
- Keep frontmatter keys consistent with existing posts (see `content/posts/` examples)

## Deployment
- Auto-deploys on push to `main` via GitHub Actions (no manual step needed)
- Use `draft: true` in frontmatter for unpublished posts (`hugo server -D` shows drafts; production build won't)
