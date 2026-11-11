---
title: "Projects"
description: "Lorevell, Luffy, FootagePilot and other original systems. Code and engineering notes by Archit Singh."
url: "/projects/"
showToc: true
comments: false
hideMeta: true
tts: false
disableShare: true
ShowPostNavLinks: false
---

These projects explore how agents retain context, execute tools and expose enough information to investigate a failure. Each has source code and a longer account of its design.

<span id="memori--flagship"></span>

## Lorevell (formerly Memori) {#lorevell}

Local knowledge for humans and agents. Lorevell keeps notes in plain Markdown files that you can read, edit and carry between tools. Markdown is the source of truth; SQLite is a rebuildable search index.

Its Rust core supports full-text and local vector search. The CLI connects the vault to existing coding agents, including Claude Code and Codex, for recall and bounded knowledge consolidation. The agent supplies the reasoning; Lorevell supplies the files, retrieval and validation around it.

The current repository documents the breaking 2.0 interface and installation from source. Older Memori packages and benchmarks describe earlier versions; they do not establish the behavior or performance of the current vault. Follow the current setup and migration instructions before switching an existing installation.

- [Source and current setup](https://github.com/archit15singh/lorevell#readme)
- [Memori → Lorevell rename guide](https://github.com/archit15singh/lorevell/blob/main/docs/rebrand.md)
- [Operational details and limits](https://github.com/archit15singh/lorevell/blob/main/docs/v2.md)
- Earlier Memori design: [Architecture decisions](/posts/2026-03-24-memori-architecture/) · [Retrieval design](/posts/2026-04-10-memori-recursive-design/) · [Designing the CLI](/posts/2026-02-28-designing-cli-tools-for-ai-agents/)
- [PyCon India talk](/speaking/)

## Luffy

Luffy is a GitHub PR review agent triggered by a comment. It can inspect code, run commands to reproduce a suspected bug, and post a structured review. It retains repository-specific memory and saves a redacted trace so the run can be examined later.

A GitHub Actions workflow runs Hermes Agent through OpenRouter. The model is selected explicitly. The [design article](/posts/2026-07-31-luffy-pr-review-agent/) follows the workflow from the initial comment through tool execution, review output and saved memory.

In one recorded Odoo review, Luffy returned REQUEST CHANGES with a score of 42/100. The run used ten API calls, took about four minutes and cost roughly $0.59. Those figures describe that run; they do not establish review accuracy across repositories. The saved trace lets you inspect how it reached the result.

- [Source and setup](https://github.com/archit15singh/luffy-pr-review-agent#readme)
- [Recorded run and traces](https://github.com/archit15singh/luffy-pr-review-agent/tree/main/docs/showcase)
- [Building Luffy](/posts/2026-07-31-luffy-pr-review-agent/)

<span id="spliceforge"></span>

## FootagePilot {#footagepilot}

An agent-driven video editor for real footage. The pipeline combines speech cleanup, local word alignment, Codex story planning, validated word-level cuts, captions and graphics, and HyperFrames or Remotion rendering with audio mixing.

The repository records a real-footage run and four generated variations, with export checks and documented limits. Listening quality and general storytelling performance are not established by those technical checks. Follow the current setup instructions and inspect the example outputs before choosing it for a workflow.

- [Source and setup](https://github.com/archit15singh/footagepilot)
- [Real-footage findings](https://github.com/archit15singh/footagepilot/blob/main/docs/REAL-E2E-RESULTS.md)
- [Naming and migration](https://github.com/archit15singh/footagepilot/blob/main/docs/NAMING.md)

## Other projects {#also-original}

These repositories cover evaluation, engineering knowledge and simulation.

**[Free Model Eval](https://github.com/archit15singh/free-model-eval).** Six free-tier coding models through OpenCode, eleven variants, ten tasks. Welch t-test, Bonferroni, Cohen's d. The grader is a different model from the one under test.

**[Chronicle](https://github.com/archit15singh/chronicle-engineering).** Reconstructs engineering decisions from repository history, PRs and incidents, aiming to preserve the reasoning behind changes.

**[Idea Generator](https://github.com/archit15singh/idea-generator).** An OpenCode workflow for exploring business ideas in a constrained market. It uses YC company data, staged comparisons and explicit checks to narrow candidates.

**[Sim Bangalore](https://github.com/archit15singh/sim-bangalore).** A simulation of Bengaluru across 243 BBMP wards, with synthetic residents and road/Metro routing. It compares scenarios such as remote work, fare changes and ORR closures. The foundation is a port of [Sim Francisco](https://github.com/tejasprabhune/simfrancisco). The Bangalore population, calibration, and policy core are the original work.

## Use or discuss the work

Start with the linked repository instructions and report reproducible issues there. For a technical collaboration or talk, [get in touch](/contact/).
