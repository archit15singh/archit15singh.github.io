---
title: "Projects"
description: "Memori, Luffy, and other original systems. Code on GitHub, write-ups here."
url: "/projects/"
showToc: true
comments: false
hideMeta: true
tts: false
disableShare: true
ShowPostNavLinks: false
---

These projects explore how agents retain context, execute tools and expose enough information to investigate a failure. Each has source code and a longer account of its design.

## Memori — flagship

Memori stores memory for AI coding agents in a local SQLite database. Its Rust core combines full-text and vector search, with Python bindings and a CLI. Retrieval does not require a hosted API.

I built it around a recurring problem: useful context from one coding session is often unavailable in the next. Capturing notes is only part of the solution. The agent also needs to retrieve the right information while working.

The implementation combines search results with reciprocal rank fusion, reduces duplicate memories using cosine similarity, and adjusts ranking using access history. The [architecture article](/posts/2026-03-24-memori-architecture/) explains those choices and their trade-offs.

You can install the published packages or follow the repository instructions. Tests and benchmark code are included; retrieval quality still needs to be evaluated against the queries and expected answers of the workload you intend to use it for.

- [Source and setup](https://github.com/archit15singh/memori#readme)
- [Python package](https://pypi.org/project/py-memori/) · [Rust crate](https://crates.io/crates/memori-ai-core) · [API documentation](https://docs.rs/crate/memori-ai-core/latest)
- [Architecture decisions](/posts/2026-03-24-memori-architecture/) · [Retrieval design](/posts/2026-04-10-memori-recursive-design/)
- [Designing the CLI](/posts/2026-02-28-designing-cli-tools-for-ai-agents/) · [Enforcing constraints in code](/posts/2026-03-23-hard-constraints-belong-in-code/)
- [PyCon India talk](/speaking/)

## Luffy

Luffy is a GitHub PR review agent triggered by a comment. It can inspect code, run commands to reproduce a suspected bug, and post a structured review. It retains repository-specific memory and saves a redacted trace so the run can be examined later.

A GitHub Actions workflow runs Hermes Agent through OpenRouter. The model is selected explicitly. The [design article](/posts/2026-07-31-luffy-pr-review-agent/) follows the workflow from the initial comment through tool execution, review output and saved memory.

In one recorded Odoo review, Luffy returned REQUEST CHANGES with a score of 42/100. The run used ten API calls, took about four minutes and cost roughly $0.59. Those figures describe that run; they do not establish review accuracy across repositories. The saved trace lets you inspect how it reached the result.

- [Source and setup](https://github.com/archit15singh/luffy-pr-review-agent#readme)
- [Recorded run and traces](https://github.com/archit15singh/luffy-pr-review-agent/tree/main/docs/showcase)
- [Building Luffy](/posts/2026-07-31-luffy-pr-review-agent/)

## Other projects {#also-original}

These repositories cover evaluation, engineering knowledge and simulation.

**[Free Model Eval](https://github.com/archit15singh/free-model-eval).** Six free-tier coding models through OpenCode, eleven variants, ten tasks. Welch t-test, Bonferroni, Cohen's d. The grader is a different model from the one under test.

**[Chronicle](https://github.com/archit15singh/chronicle-engineering).** Reconstructs engineering decisions from repository history, PRs and incidents, aiming to preserve the reasoning behind changes.

**[Idea Generator](https://github.com/archit15singh/idea-generator).** An OpenCode workflow for exploring business ideas in a constrained market. It uses YC company data, staged comparisons and explicit checks to narrow candidates.

**[Sim Bangalore](https://github.com/archit15singh/sim-bangalore).** A simulation of Bengaluru across 243 BBMP wards, with synthetic residents and road/Metro routing. It compares scenarios such as remote work, fare changes and ORR closures. The foundation is a port of [Sim Francisco](https://github.com/tejasprabhune/simfrancisco). The Bangalore population, calibration, and policy core are the original work.

## Use or discuss the work

Start with the linked repository instructions and report reproducible issues there. For a technical collaboration or talk, [get in touch](/contact/).
