---
title: "Building Luffy: a PR review agent you can audit"
description: "A comment-triggered PR review control plane. Hermes Agent, OpenRouter, Claude Opus 5, and a hub memory that actually grows. Built it on a real Odoo bug, captured the full agentic loop, and got a REQUEST CHANGES the code earned. Here is the system, the numbers, and a slice of the trace."
date: 2026-07-31T00:45:00+05:30
tags:
  - AI
  - Agents
  - Engineering
  - GitHub
categories:
  - Engineering
cover:
  hidden: false
  relative: false
  image: "/images/uploads/luffy-banner.jpeg"
  alt: "Luffy — a comment-triggered PR review agent with growing hub memory"
  caption: ""
editPost:
  URL: ""
  Text: ""
  appendFilePath: false
showToc: true
TocOpen: true
hidemeta: false
comments: true
disableHLJS: false
disableShare: false
hideSummary: false
searchHidden: false
ShowReadingTime: true
ShowBreadCrumbs: true
---

Most AI PR bots do the same thing. They read a diff, emit soft prose, and vanish. No memory of the last review on that repo. No package you can open later and see *which tools the model ran*. No honest score when the code is wrong.

I built **[Luffy](https://github.com/archit15singh/luffy-pr-review-agent)** for the opposite job: a comment-triggered review control plane. You type `@luffy review this pr`. GitHub Actions runs Hermes Agent through OpenRouter. The agent can shell into the workspace, repro failures, and post a structured Markdown review. Then it stores a redacted trace and grows hub memory so the next run on that repo is not starting from zero.

This post is how that system is put together, what broke on the way, and what a live run looked like when I pointed Claude Opus 5 at a real Odoo fix.

Proof, not vibe: Actions run `30574256524` on a fork's PR #3. Model `anthropic/claude-opus-5`. **REQUEST CHANGES**, score **42/100**. Ten API calls, nine tool-call turns, twenty-six session messages, about four minutes of Hermes wall time, roughly **$0.59**. The full trace package lives in the repo under `docs/showcase/`.

![Luffy captured Opus 5 agentic-loop trace on archit15singh/odoo PR #3 — REQUEST CHANGES, 42/100, 10 API calls, $0.59](/images/uploads/luffy-trace-demo.png)

---

## The problem is systems, not "better prompts"

PR review fails for boring reasons.

Humans skip things when the monorepo is huge. Consistency drifts. Institutional knowledge lives in Slack threads that die.

Stateless LLM review fails for different boring reasons. It has no durable notes for *this* codebase. It often cannot prove a claim with a local repro. When the run ends, you get a comment blob and nothing you can replay.

On something Odoo-sized, "clone the world and chat" is also an economics problem. Full checkouts burn minutes before the model even starts.

So the design question was never "which model writes nicer English?" It was:

1. How do we **bound** context (sparse paths, capped diffs)?
2. How do we **structure** the answer so CI and humans can parse it?
3. How do we **keep** what we learned (memory)?
4. How do we **export the loop** (tools, prompts, steps) so we can improve the system?

Luffy is an answer to those four.

---

## What Luffy is (and is not)

One line: comment-triggered PR reviews via Hermes + OpenRouter, with a fixed review contract, hub memory, and redacted run traces.

The user path is short:

```text
@luffy review this pr
  → GitHub Actions
  → Hermes (tools + model)
  → PR comment + ✅/❌
  → artifact trace + hub memory update
```

V1 is **not** a global bot that reviews every public repo with no install. The default model is paid on OpenRouter (`anthropic/claude-opus-5`); I would rather budget the cost deliberately via the trigger than pretend it is zero. It posts full PR comments, not inline review threads yet. Installation is per-repo, on purpose, so the trust boundary stays explicit.

If you need a rubber stamp, use a cheaper model and a shorter prompt. Luffy's showcase run failed the PR on purpose. That is the point.

---

## Principles I refused to drop

**Explicit trigger.** No auto-review on every push. Cost and consent stay with the commenter. The workflow also gates by GitHub `author_association` (default: owner / member / collaborator / contributor) so a random drive-by comment does not burn OpenRouter credits.

**PR text is untrusted.** Title, body, and diff can contain prompt-injection attempts. The SOUL and review prompt say so out loud. The model is a reviewer, not a servant of the PR description.

**Evidence over vibes.** Findings need a path, a symbol, and a concrete trigger when they claim a bug. On the Opus run, the agent did not only *assert* a codec problem. It ran Python against the workspace until `UnicodeDecodeError` showed up.

**Structured contract.** Free-form "LGTM" is useless in CI. The review is forced into a shape: verdict, confidence, score, review effort, walkthrough, blocking, a findings table, a security line, suggestions, optional code diffs, a tests & risk block, and "what was checked". A normalizer strips outer fences and caps size for GitHub comments.

**Durable state.** After each run, Luffy distills notes into local `MEMORY.md`, publishes a size-capped payload into the hub under `memory/repos/{owner}--{repo}/`, and preloads that hub memory on the next review for the same target. Without preload, "memory" is theater.

**Operability.** Sparse checkout of changed paths. Hermes install cache. Replace prior Luffy comments instead of stacking noise. Always post a failure stub if the agent dies. Eyes reaction while running; ✅ / ❌ when done.

---

## The pipeline (outer loop)

Roughly four boxes, statically:

```text
Developer ──comment──► Target repo (Actions + sparse PR head)
                              │
                              ▼
                     Luffy agent/ + scripts/
                     (SOUL, prompt, orchestrator)
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         Hermes Agent    OpenRouter      Hub repo
         (tools/loop)    (Opus 5…)     memory/ + ingest
              │
              ▼
     PR comment + Actions artifacts (trace)
```

The spine is a boring shell script on purpose. `scripts/run-luffy-review.sh` runs seven deterministic stages:

```text
1  preload_hub_memory   ──► Hub MEMORY.md → HERMES_HOME
2  assemble-context     ──► PR meta + diff + prompt fill
3  hermes -z            ──► install/run Hermes, capture loop
4  normalize-review     ──► contract repair + size cap
5  distill-memory       ──► append structured notes
6  save-trace           ──► redacted .luffy-out/traces/
7  publish-run-to-hub   ──► memory/repos/{owner}--{repo}/
```

Boring is good. Deterministic stages give you timings, retries, and a place to hang artifacts even when the model fails. The whole orchestrator for the showcase run took 253 seconds; 251 of those were Hermes, and the rest split across assemble, distill, and trace packaging.

| Stage | Seconds (real run) |
|-------|--------------------|
| preload_hub_memory | 0 |
| assemble | 2 |
| hermes | 251 |
| distill | 0 |

---

## The inner loop (Hermes + tools)

Here is the part most "PR bots" skip. The agent does not just emit a comment. It runs a multi-turn loop against the workspace, and I capture every turn.

```text
          ┌─ agentic loop (Hermes + OpenRouter) ──────┐
 prompt + │     prompt + memory + workspace           │
 memory   │            │                              │
 ────────►│            ▼                              │
          │     model reasoning ◄──► tools (read)     │
          │            │                              │
          │            ▼                              │
          │     draft Markdown review                 │
          └───────────────────────────────────────────┘
                              │
                              ▼
                   normalize -> distill -> trace -> comment
```

For the showcase run, the inner loop looks like this in trace:

```bash
hermes -z "$PROMPT" \
  --provider openrouter \
  --model anthropic/claude-opus-5 \
  -t terminal \
  --usage-file hermes-usage.json
```

Then `scripts/capture-hermes-loop.py` reads the usage JSON (tokens, cost, `session_id`, `api_calls`), the session `state.db` messages (roles, tool_calls, tool results), and a slice of `logs/agent.log`, and writes `agent-loop/agent-loop.md` + `agent-loop.json` into the trace.

Without that capture you only ship the last message. The last message is the advertisement, not the work.

---

## What the agent actually did (real, captured)

This is the run that made me trust the system. PR #3 was a real Odoo fix for [odoo/odoo#271153](https://github.com/odoo/odoo/issues/271153): `remove_control_characters` had encoded a Unicode character class and matched it against UTF-8 *bytes*, so `U+FFFE`/`U+FFFF` survived into lxml and crashed invoice generation. The PR fixed the `str` path. It changed the `bytes` path to `errors='surrogatepass'`. The comment claimed that round-tripped any byte sequence.

Opus 5 did not take that claim at face value. Condensed from the captured steps:

| Turn | Kind | What happened |
|------|------|---------------|
| 1 | user | Full Luffy review prompt + PR #3 metadata |
| 2 | tools | `cat pr.diff`, `cat context.md | head -200` |
| 3 | tools | Latin-1 `café` repro + `sed` of `xml_utils.py` |
| 4 | tools | `grep remove_control_characters` call sites |
| 5-8 | tools | More codec experiments; runs the PR's own new test |
| 9 | tools | Reads `cleanup_xml_node` boundary + checks the codec the comment promised |
| 10 | assistant | Structured review → REQUEST CHANGES (surrogatepass bug) |

The decisive moments, in the agent's own captured output:

Turn 5. The repro that broke the comment's claim:

```
b'caf\xe9'
RAISED: UnicodeDecodeError 'utf-8' codec can't decode byte 0xe9 in position 3
```

Turn 8. The agent ran the PR's own test class against the PR's own code:

```
--- test_non_utf8_bytes_do_not_raise ---
FAIL -> UnicodeDecodeError : 'utf-8' codec can't decode byte 0xe9 in position 3
```

So the PR shipped a test that its own implementation could not pass. The agent proved it instead of asserting it, then turned it into a blocking finding with a one-line codec fix (`surrogateescape`, not `surrogatepass`) and a code suggestion that preserved the surrogate range so `Société` did not silently become `Socit`. That is the product working. A soft APPROVE would have been a worse system outcome.

---

## The receipt

Numbers straight out of the trace package:

| Metric | Value |
|--------|-------|
| Actions run | `30574256524` |
| Session id | `20260730_191954_63f003` |
| Model | `anthropic/claude-opus-5` |
| Hermes stage | 251s (total orchestrator 253s) |
| API calls | 10 |
| Tool-call turns | 9 |
| Messages | 26 |
| Tokens total | ~195k (heavy cache read) |
| Est. cost | ~$0.59 |
| Verdict | REQUEST CHANGES |
| Score | 42/100 |
| Effort | 4/5 |

This is what got posted back on the PR (excerpt):

```markdown
## 🏴‍☠️ Luffy Review — PR #3
Verdict: REQUEST CHANGES
Confidence: high
Score: 42/100
Review effort: 4/5

### Blocking
- odoo/tools/xml_utils.py — errors='surrogatepass' cannot decode
  non-UTF-8 bytes and breaks cleanup_xml_node. surrogatepass only
  permits already-encoded lone surrogates; it does not tolerate
  arbitrary invalid bytes. Reproduced on this workspace:

  payload = '<?xml version="1.0" encoding="ISO-8859-1"?>…Société…'
           .encode('latin-1')
  OLD (base 19.0): b'<Inv>…Soci&#233;t&#233;…</Inv>'  # works
  NEW (this PR):   UnicodeDecodeError: 'utf-8' codec can't
                   decode byte 0xe9 in position 59
```

The findings table had four rows. One critical (the codec regression), one high (the self-failing test), one medium (the silent-accent-loss trap if you "fix" it naively), one low (a docstring/type promise mismatch). Each row carried a file, an issue, and a concrete trigger scenario. That is what a structured review looks like when the contract holds.

---

## If you cannot export the loop, you cannot improve the agent

Every run treats the trace as a small dataset:

```text
traces/pr{N}-run{RUN_ID}-a{ATTEMPT}/
  meta.json          # identity, status, timings pointer, file hashes
  prompt.md          # what the model was asked
  context.md         # the PR context block
  pr.json / pr.diff  # GitHub PR data + diff
  review.raw.md      # Hermes stdout, unnormalized
  review.md          # the normalized posted body
  hermes.stderr      # any errors
  timings.json       # stage durations
  agent-loop/
    agent-loop.md    # human-readable tool-by-turn walkthrough
    agent-loop.json  # messages + tool args (redacted)
    agent.log        # raw Hermes log slice
    usage.json       # cost + token shape
  memory-before.md   # MEMORY.md before the review
  memory-after.md    # MEMORY.md after the distill step
```

Traces are Actions artifacts (90 days for the trace bundle, 14 days for a debug bundle). You can pull one with `gh run download` and reconstruct exactly what the agent saw, what it said, and what it learned, for any review.

Secrets (`sk-or-…`, `OPENROUTER_API_KEY=…`) are stripped before anything is committed or uploaded. The hub is the source of truth, but it never holds credentials.

That package is why the agent is auditable instead of magical. *"This function has a null-deref bug"* is a strong claim. If an author disagrees, I should be able to point at a file in the trace and say "here is the prompt, here is the diff, here is the raw output, here is the memory delta." Long term these packages are the start of an eval set. Regression tests for agents look like golden traces, not only unit tests on pure functions.

---

## The memory hub (the part no stateless bot has)

Luffy treats memory as a first-class artifact in version control. There is a central hub repo. Every target repo that runs Luffy publishes its run into `memory/repos/{owner}--{repo}/` on the hub:

```text
memory/repos/
  {owner}--{repo}/
    MEMORY.md          # cumulative learned notes for that repo
    latest.json        # pointer to the most recent run
    runs/{trace_id}/
      meta.json        # run identity + hashes
      review.md        # the review body
      summary.md       # short distill block
```

Before a review, `scripts/preload-hub-memory.sh` pulls that repo's `MEMORY.md` from the hub into `HERMES_HOME`. The agent then reads prior notes ("this repo rejects inline CSS," "the auth module prefers vault refs," "PR #2 missed a null check in the serializer") and reviews with that context. After the review, a distill step appends a short summary back into memory. The next review is genuinely smarter because it is standing on what the previous one learned.

Why memory in git and not a database? Git is already where Luffy lives. The memory is reviewable, diffable, branchable. A bad ingest can be reverted. A human can edit `MEMORY.md` by hand and the next review picks it up. The cost of that simplicity is a serialized commit on the hub, handled with a concurrency group that does not cancel in-flight ingests and a retry loop for push races.

The publish path has two modes. **Direct** (the default): the target clones the hub, runs an ingest Python script, commits the new memory, and pushes `main`. This works with the target's own `GITHUB_TOKEN` when Luffy reviews itself, or with a PAT for cross-repo use. **Dispatch**: the target fires `repository_dispatch` (`luffy-run`) on the hub. Dispatch needs a classic PAT because `GITHUB_TOKEN` cannot call dispatch on another repo. That is a GitHub limitation, not a Luffy one.

---

## The ROI fixes that made it usable

Luffy v0 was correct but slow and noisy. A short sprint of ranked fixes turned it into something I would actually run. None of them are clever.

| ID | Fix | Why it mattered |
|----|-----|-----------------|
| F1 | PR head `fetch-depth: 1` + sparse-checkout of changed paths only | Cut minutes off monorepo checkouts |
| F2 | Cache the Hermes install tree (`~/.local` + `~/.hermes`) | Kills the cold-install cost on every run after the first |
| F3 | Preload the hub `MEMORY.md` into `HERMES_HOME` before review | The whole point. Reviews become memory-backed, not stateless |
| F4 | Drop the broken hermes-home Actions cache; let the hub be source of truth | Removes noise, simplifies the mental model |
| F5 | `+1` / `-1` reactions on the trigger comment | A clear done/fail signal to the author |
| F6 | Cap hub clone depth to 1 | Small, but the publish step is no longer slower than the review |
| F11 | `author_association` allowlist | Stops random comments from spending your OpenRouter budget |
| F12 | Replace prior Luffy comment instead of stacking | One review per PR, not a noise pile |

F3 is the one that separates Luffy from every stateless review bot, and it was not the first thing I shipped. It was the third. The first version had memory but did not *load* it. That gap was the whole product, and it took a real run to expose it. "Memory written but never preloaded" is a blog post, not a feature. Preload first.

---

## Things that hurt (so you do not repeat them)

**Private repos break naive shields.io GitHub badges.** Status APIs return "repo not found" for private repos. Static query badges that still deep-link to Actions were the fix.

**Sparse path counting.** `COUNT=$(grep -c . f || echo 0)` on an empty file becomes `0\n0` on some greps and forces a full monorepo clone. One character of shell, minutes of waste on a one-file PR.

**Cache keys with `run_id` every save** thrash the Actions cache. Stable key, save on miss.

**Missing OpenRouter key used to set `pipeline_rc=0`.** Users saw a green reaction on a config failure. Fixed: fail means fail.

**Expensive models without tools still guess.** Tools closed the loop on Opus. The score dropped because the code earned it, not because the model felt charitable.

---

## What this points at

Agentic CI is becoming a layer of the SDLC. Not chat in a sidebar. Jobs with permissions, artifacts, and budgets.

Review agents are also org learning systems when memory is real. The valuable output is not only the comment. It is the updated `MEMORY.md` and the trace you can re-read after the merge.

Open work I have not finished: pin Hermes install versions for bit-for-bit CI, a Docker image with Hermes preinstalled, inline review comments, a reusable `workflow_call` packaging for many target repos, and a tighter tool sandbox policy if you open the trigger to less trusted contributors.

---

## Close

Luffy is a bet that PR review agents should look like control planes: an explicit trigger, bounded context, a structured output, durable memory, and an exportable agentic loop.

The Odoo run is the receipt. The model spent ten calls and about sixty cents, used the shell nine times, and refused to rubber-stamp a broken codec path.

If you want to poke it: install the workflow on a default branch, set `OPENROUTER_API_KEY`, comment `@luffy review this pr`, then download the trace and open `agent-loop/agent-loop.md`.

Code: [archit15singh/luffy-pr-review-agent](https://github.com/archit15singh/luffy-pr-review-agent).

One comment. One review. Memory that grows.