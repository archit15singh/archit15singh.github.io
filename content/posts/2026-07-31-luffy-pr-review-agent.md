---
title: "Luffy: A PR Review Agent That Actually Remembers"
description: "Most AI PR bots are stateless chat on a diff. Luffy is a review control plane: explicit trigger, bounded context, one Hermes review via OpenRouter, and a central memory hub that grows smarter with every run. Here is how I built it and why each design decision is where it is."
date: 2026-07-31T00:45:00+05:30
tags:
  - AI
  - Agents
  - Engineering
  - GitHub
categories:
  - Engineering
cover:
  hidden: true
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

Every few months a new "AI reviews your pull requests" product launches.
They all follow roughly the same recipe: throw a diff at a model, post
the prose back to the PR thread, move on. It works, sort of. The reviews
are okay. They forget everything the moment the job ends. Two weeks later
the same author opens another PR and the bot makes the exact same
suggestions, the same missed bugs, the same tone — because it has no
memory of having reviewed this repository before.

I wanted something different, so I built **[Luffy](https://github.com/archit15singh/luffy-pr-review-agent)**.

Luffy is not a better version of stateless chat-on-a-diff. It is a small
**review control plane** with five deliberate stages:

1. An explicit human trigger (no spam on every push)
2. Bounded context via sparse checkout and a capped diff
3. One Hermes review through OpenRouter
4. A durable memory bank on a central hub so the next review on the
   same repo is smarter
5. Redacted run traces stored as Actions artifacts for audit

One comment. One review. Memory that grows.

```
  @luffy review this pr
            │
            ▼
┌───────────────────────────┐
│  Target repo Actions      │
│  · sparse PR checkout     │
│  · preload hub MEMORY     │
│  · Hermes + OpenRouter    │
│  · normalize Markdown     │
│  · comment on PR          │
│  · upload trace artifact  │
└─────────────┬─────────────┘
              │ publish
              ▼
┌───────────────────────────┐
│  This hub                 │
│  memory/repos/{owner}--…  │
│  runs/{trace_id}/…        │
└───────────────────────────┘
```

## Why the trigger is a comment, not a push

The first design decision is the one people push back on hardest. Why
not review every push? Because the cost is wrong.

A model call costs money and tokens every time it runs. Most pushes are
noise — a rebuild, a typo fix, a merge of main. Auto-reviewing every
push means the agent spends its budget restating the obvious ten times
for every one time it catches something real. The author also learns to
ignore the bot, because the bot has cried wolf.

So Luffy only runs when a human types `@luffy review this pr` on the PR.
The trigger is cheap, explicit, and starts a feedback loop: people
invoke the review precisely when they want eyes on the change. There is
also a manual dispatch (Actions → Luffy PR Review → Run workflow) for
the same reason — the human is in control of when compute happens.

The cost control scales. With a record of *why* a review was requested,
the memory bank can later learn which kinds of triggers led to useful
reviews and which didn't. That signal never exists in a push-on-everything
bot.

## Bounded context, not "fetch everything"

The second decision is about how much of the repository you hand the
model. The naive answer is "clone the repo, feed the diff, done." On a
monorepo that is not a small amount of time.

Before any of the Luffy pipeline runs, a single `gh pr view` call lists
the changed files through the API — no clone needed. If the change
touches a sane number of files (capped at 200), Luffy builds a
sparse-checkout pattern and asks `actions/checkout` for exactly those
paths with `fetch-depth: 1`. The runner never downloads the rest of the
monorepo.

On a one-file PR against a large monorepo, the checkout step went from
roughly three and a half minutes to seconds. That is the difference
between "the review lands while the author is still at the keyboard"
and "the author has gone home."

The diff itself is also capped. `MAX_DIFF_BYTES` (default 400000)
prevents a model context window from being filled by a generated lockfile
or a vendored dump. The agent sees the signal, not the noise, and the
cost per review is predictable.

## Hermes as the reviewer

I run the review itself through [Hermes Agent](https://github.com/nousresearch/hermes-agent)
on top of OpenRouter, with `openai/gpt-5-mini` as the default model
(overridable via a `LUFFY_MODEL` Actions variable).

Hermes brings one thing I care about: a memory file it reads at the
start of every run. That is the seam I hang the rest of the system on.
Before the review I copy the hub's cumulative `MEMORY.md` for this
repository into Hermes's memory directory; the agent then reads prior
notes — "this repo rejects inline CSS," "the auth module prefers vault
references over env vars," "PR #2 missed a null check in the serializer" —
and reviews with that context.

After the review, a distill step appends a short summary of what this
run found back into memory. The next review is genuinely smarter,
because it is standing on what the previous review learned.

## The memory hub

This is the part that I think matters most, and it is the part no
stateless bot has.

Luffy treats memory as a first-class artifact in version control. There
is a central *hub* repository (the Luffy repo itself). Every target repo
that runs Luffy publishes its run to `memory/repos/{owner}--{repo}/` on
the hub:

```
memory/repos/
  {owner}--{repo}/
    MEMORY.md          # cumulative learned notes for that repo
    latest.json        # pointer to the most recent run
    runs/{trace_id}/
      meta.json        # run identity + hashes
      review.md        # the review body
      summary.md       # short distill block
```

The publish path has two modes. **Direct** (the default): the target
clones the hub, runs an ingest Python script, commits the new memory,
and pushes main. This works with the target's own `GITHUB_TOKEN` when
Luffy reviews itself, or with a PAT for cross-repo use. **Dispatch**:
the target fires `repository_dispatch` (`luffy-run`) on the hub, which
triggers the *Ingest Luffy Run* workflow. Dispatch needs a classic PAT
because `GITHUB_TOKEN` cannot call dispatch on another repo — that is a
GitHub limitation, not a Luffy one.

Why memory in git and not a database? Because git is already the place
where Luffy lives. The memory is reviewable, diffable, branchable. A bad
ingest can be reverted. A human can edit `MEMORY.md` by hand and the
next review picks it up. There is no extra service to run, no database
to back up, no migration to write. The cost of that simplicity is a
serialized commit on the hub — handled with a concurrency group that
does not cancel in-flight ingests and a retry loop for push races.

The memory is also redacted. Before anything is committed, secrets
(`sk-or-…`, `OPENROUTER_API_KEY=…`) are stripped from the trace. The
hub is the source of truth, but it never holds credentials.

## Traces as artifacts, not logs

Every run produces a structured per-run trace stored as a GitHub
Actions artifact:

```
traces/pr{N}-run{RUN_ID}-a{ATTEMPT}/
  meta.json          # identity, status, timings pointer, file hashes
  prompt.md          # the agent prompt
  context.md         # the PR context block
  pr.json / pr.diff  # the GitHub PR data
  review.raw.md      # Hermes stdout, unnormalized
  review.md          # the normalized posted body
  hermes.stderr      # any errors
  timings.json       # stage durations
  memory-before.md   # MEMORY.md as it was before the review
  memory-after.md    # MEMORY.md after the distill step
```

Traces live 90 days (a debug bundle lives 14). I can pull one with
`gh run download` and reconstruct exactly what the agent saw, what it
said, and what it learned — for any review, ever.

This matters because Luffy is an agent making claims on PRs. *"This
function has a null-deref bug"* is a strong claim. If an author
disagrees, or if I want to know why a review was strange, I shouldn't
have to trust the bot. I should be able to point at a file and say
"here is the prompt, here is the diff, here is the raw output, here is
the memory delta." The trace is the audit trail that makes the bot
accountable to its own history.

## The ROI fixes that made it usable

Luffy v0 was correct but slow and noisy. A short sprint of six ranked
fixes turned it into something I'd actually run:

| ID | Fix | Why it mattered |
|----|-----|-----------------|
| F1 | PR head `fetch-depth: 1` + sparse-checkout of changed paths only | Cut minutes off monorepo checkouts |
| F2 | Cache the Hermes install tree (`~/.local` + `~/.hermes`) | Cuts the cold-install cost on every run after the first |
| F3 | Preload the hub `MEMORY.md` into `HERMES_HOME` before review | The whole point — reviews become *memory-backed*, not stateless |
| F4 | Drop the broken hermes-home Actions cache; let the hub be source of truth | Removes noise, simplifies the mental model |
| F5 | `+1` / `-1` reactions on the trigger comment | A clear done/fail signal to the author |
| F6 | Cap hub clone depth to 1 | Small, but the publish step is no longer slower than the review |

The interesting thing about this list is that none of these fixes are
clever. They are the boring, ranked, "do the high-ROI thing first"
backlog that comes from actually running the bot and measuring where
the time goes. F3, in particular, is what separates Luffy from every
stateless review bot — and it was not the first thing I shipped, it was
the third. The first version had memory but did not *load* it. That gap
was the whole product, and it took a real run to expose it.

## What Luffy does *not* do

Honest limits matter, because half the posts in this space sell a vision
and ship a demo.

- **Comments only.** Luffy posts a review as a single PR comment. Inline
  review threads (the kind GitHub renders next to the line) are on the
  list (F9) but not shipped.
- **Installation is per-repo.** Luffy is not a global bot that races in
  on arbitrary public repos. You install the workflow on a repo you own,
  add the secrets, and that repo gets reviews. This is a feature, not a
  limitation — it keeps the trust boundary explicit.
- **The default model is paid.** `openai/gpt-5-mini` on OpenRouter is
  not free. I'd rather budget the cost deliberately via the trigger
  than pretend it is zero.
- **Hermes is installed on the runner.** A pinned Docker image with
  Hermes preinstalled (F8) is on the backlog. For now, the install is
  cached, which is good enough.

## Why I built it

I review a lot of PRs. I also write a lot of PRs that other people
review. The bottleneck in both directions is the same: the reviewer has
to rebuild the context the author already had, and the author has to
re-explain it. A stateless bot makes the second problem slightly better
and the first problem worse, because now there is a third party in the
thread who is confidently wrong in a way that takes longer to correct
than it would have to just read the diff.

Memory is the load-bearing wall. If the review agent remembers what it
has already learned about this repo — what the conventions are, what
the recurring mistakes are, what was flagged last time — then every
review costs a little less money and a little less energy than the one
before it. The slope matters more than the starting point.

Luffy is a small thing with that one opinion baked in. You can read
every line of it, run it locally, point it at your own repos, and watch
the memory grow. The code is
[here](https://github.com/archit15singh/luffy-pr-review-agent).

One comment. One review. Memory that grows.