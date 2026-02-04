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
