---
title: "Projects"
description: "Memori, Luffy, Vital Few, and other original systems. Code on GitHub, write-ups here."
url: "/projects/"
showToc: true
comments: false
---

These are the artifacts. Posts argue. These prove. Memory, tools, deterministic constraints, evaluation, observability, security, human control.

## Memori — flagship

Persistent memory for AI coding agents. Rust core, SQLite, FTS5, vector search. One file. No API dependency.

**Problem.** Every agent session starts from zero. Context you already paid for is gone the next time you open the repo.

**Thesis.** Memory is not a notes database. It is three jobs: capture useful state, preserve it cheaply, retrieve the right item at the right moment. If previously learned information cannot be recovered when needed, memory did not happen.

**Architecture.** Hybrid search with RRF, access decay scoring, cosine deduplication. Brute-force over an index until the collection size forces otherwise.

**Implementation.** Python bindings, a CLI designed for agents, Claude Code integration, a published package with prebuilt wheels for Linux (manylinux), macOS, and Windows, and a Rust crate.

**Results.** About 190 tests, benchmarks, and a retrieval loop that actually survives across sessions.

**Lessons.** Designing the CLI for agents made it better for humans. Hard constraints belong in code, not in the prompt.

**Code.** [github.com/archit15singh/memori](https://github.com/archit15singh/memori) · [py-memori on PyPI](https://pypi.org/project/py-memori/) · [memori-ai-core on crates.io](https://crates.io/crates/memori-ai-core) · [docs.rs](https://docs.rs/crate/memori-ai-core/latest)

**Talk.** [Memory is the Agent](/speaking/), PyCon India 2025.

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

## Vital Few

An agent skill that compresses a field. Name an object, compete, commit, stop. Two files, no runtime.

**Problem.** Give an agent a terse pointer and it tours the field. Stars get ranked. The tail expands. You still do not know what you would work tomorrow.

**Thesis.** Ordering is the product. The list is not. Stop is a four-check (frame names the ontology, k is from the front, item-1 witness is yes, no further search), not a feeling.

**Architecture.** `name → instance → siblings → rank → ontology → frame → explode → cca → hypothesis-rank → top-k → extract loop`. Each move derives from one property of a trustworthy cut: Zwicky/Wohlin completeness, Juran's cut, cross-consistency, Chamberlin/Platt/Pugh disagreement, Simon's stop. Recursion is bounded.

**Implementation.** [SKILL.md](https://github.com/archit15singh/vital-few/blob/main/SKILL.md) is the runbook. [LOOP.md](https://github.com/archit15singh/vital-few/blob/main/LOOP.md) is the spec. Copy both into the agent's skills directory.

**Results.** One worked pass in-repo: `anthropic autonomous vulnerability patcher` → closed-loop CRS, witness as proof object as item 1.

**Lessons.** Implementing the top-k inside the ranking loop is a fail. Running the candidates is the next loop.

**Code.** [github.com/archit15singh/vital-few](https://github.com/archit15singh/vital-few)

**Research.** [Vital Few: compress a field, then stop](/posts/2026-09-20-vital-few/)

## Also original

GitHub only. No post yet.

**[Free Model Eval](https://github.com/archit15singh/free-model-eval).** Six free-tier coding models through OpenCode, eleven variants, ten tasks. Welch t-test, Bonferroni, Cohen's d. The grader is a different model from the one under test.

**[Chronicle](https://github.com/archit15singh/chronicle-engineering).** Engineering knowledge dies when people leave. Chronicle rebuilds the decision graph from the repo: PRs, architecture, incidents. Document search is the wrong product.

**[Idea Generator](https://github.com/archit15singh/idea-generator).** An OpenCode skill that is a DAG. Ingest YC companies in a constrained market, descend, cut a wedge, score founder-fit. Gates and typed receipts live in `idea_factory/`. The prompts do not.

**[Sim Bangalore](https://github.com/archit15singh/sim-bangalore).** 243 BBMP wards, one synthetic agent per resident, A* on road plus Metro, a scorecard for WFH / fare / ORR-closure experiments. The foundation is a port of [Sim Francisco](https://github.com/tejasprabhune/simfrancisco). The Bangalore population, calibration, and policy core are the original work.
