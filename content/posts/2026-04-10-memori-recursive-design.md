---
title: "Memori: The Recursive Design of Agent Memory"
description: "Agent memory is not a storage problem. It is a retrieval problem -- and the architecture of Memori follows directly from that shift in framing. This post walks through the conceptual core: why memory is really three problems, what each design decision reduces to, and why the system stores rules about how to use itself."
date: 2026-04-09T10:00:00+05:30
tags:
  - AI
  - Agents
  - Engineering
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/memori-recursive-design-banner.jpeg"
  alt: "A lone figure ascending an infinite staircase through darkness toward light -- recursive layers of agent memory"
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
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: false
UseHugoToc: true
---

# Memori: The Recursive Design of Agent Memory

[Memori](https://github.com/archit15singh/memori) is not primarily a database for notes. It is an attempt to turn agent memory into an engineered retrieval system.

The thesis is simple. An agent fails across sessions because state is lost. Lost state only matters if previously learned information cannot be recovered when needed. So "memory" is really three problems:

1. Capture useful state.
2. Preserve it cheaply and portably.
3. Retrieve the right item at the right moment.

Everything in the code follows from that split. This post is about the concepts underneath the system -- what each design decision reduces to, and why the project is recursive at its core.

---

## Memory as Retrieval, Not Storage

Storing everything is easy. Finding the one relevant thing later is hard.

This distinction shifts the system's center of gravity. Most memory systems are designed around insert: how quickly can we write, how much can we hold, how flexibly can we structure it. Memori is designed around search and ranking. The CRUD path is thin. The retrieval path is where the design effort went.

That is why `search.rs` is the most complex file in the codebase, and `storage.rs` is mostly plumbing. The architecture encodes the thesis directly.

---

## Hybrid Search: Neither Keyword Nor Vector Alone

Exact words matter sometimes. Meaning similarity matters sometimes. Neither keyword search nor vector search dominates all cases.

Keyword search (BM25 via SQLite FTS5) finds the word you typed, precisely. Vector search finds conceptually related memories even when the exact words don't match. Both have failure modes: keyword search misses synonyms and paraphrases; vector search misses specific technical terms and identifiers.

Memori runs both and fuses the results using Reciprocal Rank Fusion. The key insight in RRF is that it combines *ranks* instead of *scores*. BM25 scores and cosine similarities live on different scales with different distributions -- averaging them is numerically unprincipled. Rank-based fusion sidesteps the problem entirely.

A result that ranks first in both keyword and vector lists gets the highest combined score. A result that ranks highly in one but not the other still surfaces. The fusion is robust to the score-scale incompatibility because it throws the scores away and only uses the ordering.

---

## Ranking Under Uncertainty

Relevance is not directly observable. The system uses proxies: text match rank, vector similarity, recency, prior access frequency. Since these signals are heterogeneous, combining them heuristically is the honest choice.

Memori applies two adjustments on top of the hybrid rank:

**Logarithmic boost from access count.** The tenth access contributes less than the first. The hundredth contributes less than the tenth. This prevents a single heavily-accessed memory from dominating all searches regardless of content. Boost asymptotes; it never becomes infinite.

**Exponential decay from last access time.** A memory accessed 69 days ago has its score halved. At 138 days, quartered. This matches the intuition that information has a freshness component -- a debugging decision from two years ago is probably less useful than one from last week, even if the content is similar.

New memories are never penalised. A memory that has never been retrieved gets a decay multiplier of 1.0. Without this guard, every newly stored memory would decay immediately from the moment it was written, penalising new knowledge before it has had a chance to prove its usefulness.

The combined effect: frequently accessed memories surface reliably, recently stored memories surface without penalty, and old memories that nobody touches gradually fade to the bottom rather than disappearing abruptly.

---

## Vectors as Lossy Semantic Sketches

Embeddings map text into a numeric space where semantic closeness becomes geometric closeness. That lets "similar idea" become cosine similarity over 384 floats.

The vector is not truth. It is a lossy sketch. Two sentences can be semantically similar and have low cosine similarity if they use different vocabulary. Two sentences can have high cosine similarity and mean different things in context. The embedding captures a projection of meaning -- useful, imperfect, irreplaceable for fuzzy retrieval.

Memori uses AllMiniLM-L6-V2 via fastembed. It is fast enough to embed at insert time without making the CLI feel slow, and accurate enough for the retrieval task. The singleton is lazily initialized -- the model loads once per process and is reused for all operations.

---

## Metadata as Controllable Semantics

Raw text is expressive but sloppy. Metadata adds explicit dimensions: `type`, `topic`, `project`, `verified`. These give the system symbolic filtering in addition to semantic search.

The design choice that makes this interesting: Memori re-embeds the full memory after metadata updates, using `content + metadata scalar values` as the input. Adding a tag to a memory shifts its vector. A memory tagged `topic=kafka` becomes retrievable by vector search for Kafka-related queries even if the word "kafka" doesn't appear in the content.

This is both a feature and a known tradeoff. The enriched vector is more useful for retrieval. But it drifts from the embedding of the raw content, which means deduplication on a later insert of identical content may not recognise the match. The FTS5 index still catches both texts in keyword search, so retrieval quality doesn't suffer -- but the dedup guard may silently miss.

---

## Deduplication as Memory Hygiene

Agents over-store. An agent that runs 100 sessions might store "use parameterised queries to prevent SQL injection" 40 times in slightly different phrasings. The memory grows without becoming more useful.

Memori deduplicates at write time. When a new memory is inserted, it is compared against existing memories of the same type using cosine similarity. If the similarity exceeds the threshold (default 0.92), the system updates the existing memory instead of creating a new one -- merging metadata, bumping `updated_at`, preserving the ID.

Memory quality is not just adding information. It is resisting redundant information. Deduplication operationalises that as a semantic check at the insert boundary.

The threshold is a judgment call. At 0.92, semantically equivalent content with different phrasing deduplicates. At 0.99, only near-identical text deduplicates. Anything lower and distinct memories start colliding. 0.92 catches rephrasing without being aggressive enough to merge genuinely different things.

---

## Portability Over Infrastructure

More infrastructure increases operational burden. Agent memory only works if it is easier to keep than to ignore.

This is a product philosophy encoded as architecture. The design chooses SQLite, one file, local embeddings, no cloud dependency, no server, no daemon. The full working memory for a developer across all their projects fits in roughly 200MB. That file is copyable, backupable, and deletable with a single command.

The scale argument supports the choice. A developer's working memory tops out around 10,000-50,000 memories. Brute-force cosine similarity at that scale is 14ms to 100ms -- fast enough that no one notices. The moment when HNSW indexing becomes worth the complexity overhead is above 500K memories. That threshold is unlikely to be crossed by a single developer's session history.

Vector search is isolated in a single function specifically to make the upgrade path clear. If the scale assumption ever proves wrong, the replacement is a drop-in for one function. Nothing else changes.

---

## Agent Ergonomics as Correctness

A tool for agents is not just an API. It is a behavioral interface.

The CLI design reflects this. Short ID prefixes instead of full UUIDs. `--json` and `--raw` flags for machine-readable output. Compact context views that fit in a token budget. A single `context` subcommand that retrieves the most relevant memories for the current session without requiring the agent to compose a multi-step query.

The system assumes the caller is another reasoning process with token limits and imperfect discipline. So ergonomics is not decoration. An agent that cannot efficiently query memory will stop using it. An agent that gets back verbose, poorly structured output will stop trusting it. The CLI is part of the correctness surface.

---

## Self-Maintenance: Teaching the Agent to Curate

Memory systems decay if no one curates them. Humans will not reliably curate agent memory. So the agent must be taught to do it.

Memori ships with a behavioral protocol embedded in `claude_snippet.md` -- a structured prompt fragment that instructs the agent on when to search memory, when to store, when to clean, and when to distrust. Installing Memori means installing both the software and the behavioral loop that makes the software useful.

The project is not just a library. It is a library plus a protocol.

---

## The Recursive Core

Here is the part that took the longest to articulate clearly.

Memori does not just store facts. It stores the conditions under which remembering becomes useful.

A memory can describe a debugging technique. A memory can also describe when to search for debugging techniques, how to phrase the query, how to evaluate the result, and how to store the lesson so it surfaces again next time. Memory content can include rules for producing better future memory content.

That is the self-recursive structure of the project. The agent uses memory to improve its own memory use. The system stores abstractions -- and some of those abstractions are about how the system itself should be used. When the agent follows the behavioral protocol, reads its own lessons, and updates its memory rules based on what worked and what didn't, it is running a feedback loop that improves retrieval quality over time without any human intervention.

---

## The One-Sentence Summary

Useful memory emerges from the interaction of persistence, representation, retrieval, ranking, hygiene, and agent behavior.

Each concept in that list is a separate engineering problem. Memori is an attempt to solve all six, in the smallest possible system, with the clearest possible tradeoffs.

The code is at [github.com/archit15singh/memori](https://github.com/archit15singh/memori). The architectural decisions are all in `memori-core/src/` -- `search.rs` for RRF and decay, `storage.rs` for deduplication, `schema.rs` for FTS5 and migrations, and `embed.rs` for the embedding singleton. The behavioral protocol lives in `memori-python/python/memori_cli/data/claude_snippet.md`.

If you are building something that needs persistent context across agent sessions, start there.
