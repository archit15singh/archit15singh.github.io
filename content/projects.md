---
title: "Projects"
description: "Memori and Luffy — original systems for reliable AI agents. Code on GitHub, write-ups here."
url: "/projects/"
showToc: true
comments: false
---

These are the artifacts. Posts argue. These prove.

## Memori — flagship

Persistent memory for AI coding agents. Rust core, SQLite, FTS5, vector search. One file. No API dependency.

**Problem.** Every agent session starts from zero. Context you already paid for is gone the next time you open the repo.

**Thesis.** Memory is not a notes database. It is three jobs: capture useful state, preserve it cheaply, retrieve the right item at the right moment. If previously learned information cannot be recovered when needed, memory did not happen.

**Architecture.** Hybrid search with RRF, access decay scoring, cosine deduplication. Brute-force over an index until the collection size forces otherwise.

**Implementation.** Python bindings, a CLI designed for agents, Claude Code integration, a published package and crate.

**Results.** About 190 tests, benchmarks, and a retrieval loop that actually survives across sessions.

**Lessons.** Designing the CLI for agents made it better for humans. Hard constraints belong in code, not in the prompt.

**Code.** [github.com/archit15singh/memori](https://github.com/archit15singh/memori) · [py-memori on PyPI](https://pypi.org/project/py-memori/) · [memori-ai-core on crates.io](https://crates.io/crates/memori-ai-core) · [docs.rs](https://docs.rs/crate/memori-ai-core/latest)

**Research.**
- [Architecture decisions](/posts/2026-03-24-memori-architecture/)
- [Recursive design](/posts/2026-04-10-memori-recursive-design/)
- [CLI tools for AI agents](/posts/2026-02-28-designing-cli-tools-for-ai-agents/)
- [Hard constraints belong in code](/posts/2026-03-23-hard-constraints-belong-in-code/)

## Luffy

A comment-triggered PR review control plane. The agent can shell into the workspace, reproduce failures, post a structured review, store a redacted trace, and grow hub memory so the next run on that repo is not starting from zero.

**Problem.** Most PR bots read a diff, emit soft prose, and vanish. No memory of the last review. No package you can open later to see which tools ran. No honest score when the code is wrong.

**Thesis.** Agents need state, observability, and a control plane. Not a better prompt.

**Architecture.** GitHub comment → Actions → Hermes Agent through OpenRouter → tools in the workspace → structured Markdown review → redacted trace → hub memory.

**Implementation.** You type `@luffy review this pr`. Model choice is explicit. Memory is per-repo and accumulates.

**Results.** Live Odoo review on a real bug: REQUEST CHANGES, score 42/100, ten API calls, about four minutes, roughly $0.59. The trace package is in the repo under `docs/showcase/`.

**Lessons.** If you cannot audit the loop, you do not have a review agent. You have a comment generator.

**Code.** [github.com/archit15singh/luffy-pr-review-agent](https://github.com/archit15singh/luffy-pr-review-agent)

**Research.** [Building Luffy](/posts/2026-07-31-luffy-pr-review-agent/)
