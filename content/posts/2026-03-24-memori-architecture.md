---
title: "Building Persistent Memory for AI Agents: Architecture Decisions in Memori"
description: "A deep dive into the engineering decisions behind Memori -- a persistent memory system for AI coding agents built on Rust, SQLite, and fastembed. Covers hybrid search with RRF, access decay scoring, cosine deduplication, and why I deliberately chose brute-force over indexing."
date: 2026-03-24T10:00:00+05:30
tags:
  - AI
  - Agents
  - Engineering
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/memori-architecture-banner.jpeg"
  alt: "Abstract circuit nodes interconnected -- persistent memory architecture for AI agents"
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

# Building Persistent Memory for AI Agents

Every AI coding agent session starts from zero. The agent doesn't remember that you spent three hours last Tuesday debugging a SQLite WAL-mode deadlock, or that you decided against a particular abstraction pattern after trying it twice, or that your project has a non-obvious deployment constraint that every new session will trip over unless you paste it into the prompt again.

That tax -- re-establishing context at the start of every session -- compounds invisibly. You stop noticing it the same way you stop noticing a slow network: individually small, collectively enormous.

[Memori](https://github.com/archit15singh/memori) is my attempt to fix this. It's a persistent memory system for AI coding agents -- specifically Claude Code, though the architecture is general. Agents store what they learn, retrieve what's relevant, and accumulate knowledge across sessions instead of resetting each time.

Building it surfaced a set of engineering decisions I didn't anticipate. This post is about those decisions: what the naive approach was, why it failed, what I chose instead, and the tradeoff I accepted.

---

## The Architecture in One View

Before the decisions, the shape of the system:

```
Agent (Claude Code)
      |
      v
memori CLI  (Python, argparse, 18 subcommands)
      |
      v
PyMemori    (PyO3 bindings, Mutex<Memori>, GIL management)
      |
      v
Rust Core
  +-- storage.rs   CRUD, dedup, metadata merge, prefix resolution
  +-- search.rs    hybrid search, RRF fusion, decay scoring
  +-- embed.rs     fastembed AllMiniLM-L6-V2, lazy OnceLock singleton
  +-- schema.rs    DDL, FTS5 virtual table, migrations v0-v3
  +-- types.rs     Memory struct, SearchQuery, InsertResult
      |
      v
Single SQLite file  (~/.memori/memories.db)
```

Two crates: `memori-core` (pure Rust data layer) and `memori-python` (PyO3 bindings plus CLI). The CLI is what agents actually call. The Rust core is what makes it fast enough to call on every session without the agent noticing.

The design principle that shapes every decision below: **simplicity and portability over maximum scale**. Memori is purpose-built for AI agent memory across development sessions. It is not a general-purpose vector database.

---

## Decision 1: One SQLite File, No Vector Database

The first instinct when building a system that stores and retrieves embeddings is to reach for a proper vector database -- Qdrant, Weaviate, Chroma, pgvector. They exist for this. They have HNSW indexes, they scale to billions of vectors, they have rich filtering.

I chose SQLite instead. One `.db` file. No server. No daemon. No configuration.

The reason is operational simplicity at agent scale. A developer running Claude Code doesn't want to manage a database server to get persistent memory. The expected scale -- a working memory for a single developer across their projects -- tops out around 10,000-50,000 memories. At that scale, a vector database is infrastructure overhead for a problem SQLite handles in microseconds.

The full memory for a working developer fits in roughly 200MB. That file is copyable, backupable, and deletable with a single command. If something goes wrong, `rm ~/.memori/memories.db` and start over.

SQLite in WAL mode also gives acceptable write throughput: around 5,700 writes per second at 500K memories, dropping to about 4,200 at 1M. For an agent that stores a few memories per session, that headroom is irrelevant.

The tradeoff I accepted is vector search scaling. At 100K memories, brute-force cosine similarity takes 162ms. At 500K, it's 904ms. That's fine for the intended use case. If you're building something that needs sub-10ms retrieval at a million vectors, SQLite is the wrong choice. Memori knows what it is.

---

## Decision 2: Hybrid Search via Reciprocal Rank Fusion

Most retrieval systems make you choose: keyword search or semantic search. Keyword search (BM25) is fast and exact -- it finds the word you typed. Semantic search finds things conceptually related even if the exact words don't match. Both have failure modes you don't want.

Memori runs both and combines the results. The non-obvious part is *how* to combine them.

The naive approach is score normalization: scale BM25 scores and cosine similarities to the same range, then average. This fails in practice because BM25 and cosine don't have comparable distributions. A BM25 score of 0.8 and a cosine similarity of 0.8 don't mean the same thing. Any weighted combination is numerically unprincipled.

The solution is [Reciprocal Rank Fusion](https://github.com/archit15singh/memori/blob/main/memori-core/src/search.rs), which combines *ranks* instead of scores:

```rust
fn reciprocal_rank_fusion(
    fts_results: &[(String, f32)],
    vec_results: &[(String, f32)],
    k: f32,
) -> Vec<(String, f32)> {
    let mut scores: HashMap<String, f32> = HashMap::new();

    for (rank, (id, _)) in fts_results.iter().enumerate() {
        *scores.entry(id.clone()).or_insert(0.0) += 1.0 / (k + rank as f32 + 1.0);
    }
    for (rank, (id, _)) in vec_results.iter().enumerate() {
        *scores.entry(id.clone()).or_insert(0.0) += 1.0 / (k + rank as f32 + 1.0);
    }

    let mut fused: Vec<(String, f32)> = scores.into_iter().collect();
    fused.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(Equal));
    fused
}
```

The constant `k=60` is the standard RRF default -- it controls how much the top ranks dominate. A result that ranks first in both lists gets a combined score of `1/61 + 1/61 ≈ 0.033`. A result that ranks 60th in both gets `1/121 + 1/121 ≈ 0.017`. The gap shrinks logarithmically, which is exactly what you want: strong agreement on top results, graceful degradation elsewhere.

The search pipeline over-fetches 3x the requested limit from each source, fuses, then truncates to the final limit. This ensures the fusion has enough candidates to work with before cutting.

---

## Decision 3: Brute-Force Vector Search, on Purpose

Given the SQLite choice, vector search has to happen somewhere. The obvious path is a purpose-built index -- HNSW (Hierarchical Navigable Small World) gives approximate nearest-neighbor search in O(log N) instead of O(N). Qdrant, Faiss, and hnswlib all implement it.

I chose brute-force. Every search scans all vectors, computes cosine similarity, and returns the top-k.

This was a deliberate decision, not an oversight. The reasons:

**Scale doesn't justify the complexity.** At 10,000 memories, brute-force takes 14ms. At 100,000, it takes 162ms. A developer's working memory across all their projects is unlikely to exceed 50,000 memories. At that scale, brute-force is fast enough that no one would notice the difference.

**HNSW adds maintenance complexity.** An HNSW index needs to be rebuilt when memories are deleted, updated, or re-embedded. It introduces eventual consistency windows. The brute-force approach is always consistent because it just reads the table.

**The isolation makes replacement easy.** All vector search lives in [`search.rs::vector_search()`](https://github.com/archit15singh/memori/blob/main/memori-core/src/search.rs) -- a single function that takes a query vector and returns scored IDs. If Memori ever needs HNSW, it's a drop-in replacement for one function. Nothing else changes.

```rust
fn vector_search(
    conn: &Connection,
    query_vec: &[f32],
    limit: usize,
    filter: Option<&str>,
    before: Option<f64>,
    after: Option<f64>,
) -> Result<Vec<(String, f32)>> {
    // O(N) cosine similarity scan
    // isolated here specifically for future HNSW replacement
    ...
}
```

The benchmark numbers at 500K memories (904ms) are the signal that tells me when the replacement is warranted. That number hasn't become a problem yet.

---

## Decision 4: Access Decay Scoring

Raw retrieval scores don't capture everything that makes a memory useful. A memory you've accessed 50 times probably contains something important. A memory you stored eight months ago and never touched since is probably stale. Neither of these signals comes from the content alone.

Memori applies a scoring adjustment to every retrieved memory:

```rust
let boost = 1.0 + 0.1 * (1.0 + access_count as f32).ln();
let decay = if last_accessed == 0.0 {
    1.0  // never accessed -- no penalty
} else {
    let days = (now - last_accessed) / 86400.0;
    (-0.01 * days).exp()
};
let final_score = base_score * boost * decay;
```

Two terms, each with a specific mathematical property chosen deliberately.

**Boost is logarithmic.** The 10th access contributes less than the 1st. The 100th contributes less than the 10th. This prevents a single heavily-accessed memory from dominating all searches regardless of relevance. The boost asymptotes: it can never be infinite no matter how many times a memory is accessed.

**Decay is exponential with a 69-day half-life.** A memory last accessed 69 days ago has its score halved. At 138 days, quartered. This matches the intuition that information has a "freshness" component -- a debugging decision from two years ago is probably less useful than one from last week, even if the content is similar.

**New memories are never penalised.** The `last_accessed == 0.0` guard means a memory that has never been retrieved gets `decay = 1.0`. Without this guard, every newly stored memory would immediately start decaying from the moment it was written, which would penalise new knowledge unfairly.

The combined effect: frequently accessed memories surface reliably, recently stored memories surface without penalty, and old memories that nobody touches gradually fade to the bottom of results rather than disappearing abruptly.

---

## Decision 5: Cosine Deduplication on Insert

Without deduplication, a memory system accumulates redundancy rapidly. An agent that runs 100 sessions might store "Use parameterised queries to prevent SQL injection" 40 times in slightly different phrasings. The memory grows without becoming more useful.

Memori deduplicates at write time. When a new memory is inserted, it's compared against existing memories of the same type using cosine similarity:

```rust
fn find_duplicate(
    conn: &Connection,
    content: &str,
    vector: &[f32],
    metadata_type: Option<&str>,
    threshold: f32,
) -> Result<Option<String>> {
    // fetch all memories of the same type
    // compute cosine similarity against each
    // return first ID above threshold (default 0.92)
    ...
}
```

If the similarity exceeds 0.92, the system updates the existing memory instead of creating a new one -- merging metadata, bumping `updated_at`, preserving the existing ID.

The threshold matters. At 0.92, semantically equivalent content with slightly different phrasing deduplicates. At 0.99, only near-identical text deduplicates. I landed on 0.92 as the default after testing -- it catches rephrasing of the same concept without being aggressive enough to merge genuinely distinct memories.

**The edge case to know about.** When you tag a memory with `memori tag <id> topic=kafka`, the system re-embeds the memory using `content + metadata scalar values` as the embedding input. This shifts the vector. If you store an identical memory later, its embedding is computed from content alone -- and the similarity check compares against the shifted vector. The two vectors are no longer the same, so deduplication can miss.

This is a known tradeoff. Tagging semantically enriches the vector (making a memory findable by its topic as well as its content), but it introduces drift. The FTS5 full-text index still catches both texts in keyword search, so you won't lose retrieval -- but the dedup guard may not fire.

---

## Decision 6: FTS5 External-Content Table

SQLite has a full-text search extension called FTS5. The naive way to use it is a separate table that stores a copy of the text you want to search. This duplicates your data.

Memori uses an external-content table instead:

```sql
CREATE VIRTUAL TABLE memories_fts USING fts5(
    content,
    content=memories,
    content_rowid=rowid
);
```

The `content=memories` directive tells FTS5 that the authoritative content lives in the `memories` table. The FTS5 virtual table stores only its index, not the text itself. Disk usage stays roughly half of what a duplicated approach would use.

The tradeoff is that the index has to be kept in sync manually. SQLite doesn't do this automatically for external-content tables. Memori uses triggers:

```sql
CREATE TRIGGER memories_fts_insert AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, content)
    VALUES (new.rowid, new.content || ' ' || COALESCE(new.metadata, ''));
END;

CREATE TRIGGER memories_fts_delete AFTER DELETE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content)
    VALUES ('delete', old.rowid, old.content || ' ' || COALESCE(old.metadata, ''));
END;
```

Notice that both `content` and `metadata` are indexed by FTS5. This means a keyword search for "kafka" finds memories that mention kafka in their content *and* memories tagged with `topic=kafka` in their metadata. The FTS5 index covers the full text of the JSON metadata blob. That's a concrete UX benefit: searching for a topic finds tagged memories even when the tag word doesn't appear in the content.

The schema uses three versions of progressive migration:
- v0 -> v1: FTS5 index + metadata-aware triggers
- v1 -> v2: `last_accessed` and `access_count` columns (enables decay scoring)
- v2 -> v3: expression index on `json_extract(metadata, '$.type')` for fast type-filtered queries

Each migration runs idempotently via `PRAGMA user_version`. Adding a column to an existing database without breaking it is straightforward in SQLite; the migration just checks the version integer and runs the missing DDL.

---

## What the Architecture Optimises For

Every design decision above reflects the same underlying choice: **simplicity and portability over scale**.

One file means the entire memory system is copyable, backupable, and versionable. No infra means zero operational overhead -- no daemon to restart, no port to forward, no credentials to manage. Brute-force vector search means the code is auditable and replaceable without touching anything else. RRF means you get hybrid search without numerically dubious score normalization.

The things Memori explicitly does not try to do: sub-10ms vector search at a million records, distributed writes across multiple machines, real-time index updates on a hot write path. Those require different architecture choices. Memori is not that system.

What it is: a memory system that a developer can install in one command, that an agent can call in one CLI invocation, that stores in one file, and that accumulates knowledge across every session without any ongoing maintenance.

```bash
# install
pip install memori-python

# agent stores a lesson at end of session
memori store "WAL mode deadlock in SQLite requires explicit BEGIN IMMEDIATE" \
  --meta '{"type": "debugging", "project": "api-service"}'

# agent retrieves relevant context at start of next session
memori context --compact --project api-service
```

The architecture exists to make that loop reliable and fast. Nothing more.

---

## The Code

Memori is open source at [github.com/archit15singh/memori](https://github.com/archit15singh/memori). The core decision points discussed above all live in `memori-core/src/` -- specifically `search.rs` for the RRF and decay logic, `storage.rs` for deduplication, and `schema.rs` for the FTS5 setup and migrations.

If you're building something that needs persistent context across agent sessions, I'd be interested in what you find.
