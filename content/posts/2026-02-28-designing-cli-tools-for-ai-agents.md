---
title: "Designing CLI Tools for AI Agents: Lessons from Building Memori"
description: "A practitioner's guide to designing command-line tools that AI coding agents can use effectively -- covering output modes, error design, behavioral snippets, and the subtle art of making machines help themselves."
date: 2026-02-28T00:00:00+05:30
tags:
  - AI
  - Development
categories:
  - AI
cover:
  hidden: true
  relative: false
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

# Designing CLI Tools for AI Agents

Most CLI tools are designed for humans who can google error messages, read man pages, and ask Stack Overflow. AI agents can't do any of that. They get one shot at parsing your output, one chance to recover from an error, and they pay per token for everything you print.

I built [Memori](https://github.com/archit15singh/memori) -- a persistent memory system for Claude Code -- and discovered that designing for agents forced me to make a better tool for everyone. Here are the principles I extracted, grounded in exact code from the repository.

---

## The Core Insight

AI agents interact with CLI tools the same way a junior developer does on their first day: they read help text, try commands, parse output, and recover from errors. The difference is that agents do this thousands of times, never learn from frustration, and can't ask a coworker for help.

This means every design decision that reduces ambiguity, eliminates guesswork, or enables self-recovery compounds across thousands of invocations. A CLI designed for agents isn't a different tool -- it's a better tool for everyone.

---

## Principle 1: Dual-Mode Output -- Humans and Machines from the Same Command

Every command should produce both human-readable and machine-readable output, controlled by a flag. The human output is the default. The machine output is structured JSON.

```bash
# Human-readable (default)
$ memori search --text "database"
a1b2c3d4 [0.85] Chose SQLite over Postgres for portability [decision]

# Machine-readable
$ memori --json search --text "database"
[{"id": "a1b2c3d4-...", "content": "Chose SQLite...", "score": 0.85, ...}]

# Compact machine-readable (saves tokens)
$ memori --raw search --text "database"
[{"id":"a1b2c3d4-...","content":"Chose SQLite...","score":0.85}]
```

The entire output formatting strategy hinges on a [three-line helper function](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L82-L84):

```python
def _json_indent(args):
  """Return indent level for JSON output: None for --raw, 2 otherwise."""
  return None if getattr(args, "raw", False) else 2
```

Every subcommand calls `_json_indent(args)` when serializing output. `None` produces compact single-line JSON for `--raw`; `2` produces pretty-printed JSON for `--json`. One function, consistent formatting everywhere.

The human output path in [`cmd_search()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L179-L188) shows how to design scannable output -- truncated IDs, bracketed scores, and access frequency only surfaced when it's significant (above 5 hits):

```python
for r in results:
  score = f"[{r['score']:.4f}]" if r.get("score") is not None else ""
  meta = json.dumps(r.get("metadata") or {})
  access = r.get("access_count", 0)
  access_str = f" ({access} hits)" if access > 5 else ""
  print(f"{r['id'][:8]} {score} {r['content']}  meta={meta}{access_str}")
```

**The token budget problem**: LLM agents pay per token. The `--raw` flag strips whitespace and indentation, cutting output size by ~40%. The `--compact` flag on the `context` command goes further -- truncating IDs to 8 characters and content to 100 characters. These aren't cosmetic choices -- they directly determine how much context an agent can work with in a single session.

---

## Principle 2: Errors That Teach

Most CLI tools treat errors as stop signs. For AI agents, errors should be road signs -- they need to say what went wrong, why, and what to do instead.

The foundation is the [`_err()` helper](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L55-L64):

```python
def _err(error_type, message, exit_code=1, use_json=False, input_id=None):
  """Print an error and exit. When use_json is True, emit structured JSON to stderr."""
  if use_json:
    obj = {"error": error_type, "message": message}
    if input_id is not None:
      obj["id"] = input_id
    print(json.dumps(obj), file=sys.stderr)
  else:
    print(f"{message}", file=sys.stderr)
  sys.exit(exit_code)
```

Every error goes through this function. In human mode, you get a readable message. In JSON mode, you get a structured object with a machine-parseable `error` type and the original input `id`, all on stderr. The exit code is always explicit.

This enables different error recovery strategies at the call site. Look at how [`cmd_related()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L607-L623) parses upstream Rust errors and translates them into agent-actionable hints:

```python
def cmd_related(args):
  db = _get_db(args.db)
  try:
    results = db.related(args.id, limit=args.limit)
  except RuntimeError as e:
    err_msg = str(e)
    if "no embedding" in err_msg:
      error_type = "no_embedding"
      hint = " (run 'memori embed' to generate embeddings)"
    elif "ambiguous" in err_msg:
      error_type = "ambiguous_prefix"
      hint = " (use a longer prefix to disambiguate)"
    else:
      error_type = "not_found"
      hint = " (try 'memori list' to see available memories)"
    _err(error_type, err_msg + hint, exit_code=1, use_json=args.json, input_id=args.id)
```

Three different failure modes, three different recovery hints. An agent receiving `"no_embedding"` knows to run `memori embed`. An agent receiving `"ambiguous_prefix"` knows to retry with a longer ID. No documentation lookup needed -- the error itself is the documentation.

**Exit codes as signal**: `0` = success, `1` = not found (possibly transient), `2` = user input error (deterministic, don't retry). An agent that gets exit code 2 from [`_parse_json()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L67-L72) knows not to retry with the same malformed JSON.

---

## Principle 3: Progressive Disclosure in Help Text

Agents read `--help` before they read documentation. Your help text is your most important documentation surface.

**Bad**: Showing only syntax.

```
usage: tool store [-h] [--meta META] content
```

**Good**: Showing syntax, then examples that demonstrate the *intent*. Memori uses argparse's `epilog` field with `RawDescriptionHelpFormatter` on every subcommand. The store command's help shows exact, copy-pasteable examples:

```
Examples:
  memori store "FTS5 hyphens crash MATCH" --meta '{"type": "debugging"}'
  memori store "prefer dark mode" --meta '{"type": "preference"}' --json
```

**Warnings over rejections**: The [`_warn_unknown_type()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L108-L114) function demonstrates progression before blocking:

```python
def _warn_unknown_type(meta):
  """Warn if metadata has an unrecognized type value (never reject)."""
  if meta and isinstance(meta, dict) and "type" in meta:
    t = meta["type"]
    if isinstance(t, str) and t not in KNOWN_TYPES:
      known = ", ".join(sorted(KNOWN_TYPES))
      print(f"Warning: unknown type '{t}'. Known types: {known}", file=sys.stderr)
```

The operation succeeds. The warning teaches. The agent learns what types are valid without losing its work. This is critical -- agents often experiment with parameters, and rejecting valid-but-unexpected inputs forces unnecessary retries.

---

## Principle 4: One Command for Session Start

AI agents start fresh every session. They need to reconstruct context quickly. A single "catch me up" command is worth more than five individual queries.

Memori's [`cmd_context()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L326-L441) aggregates four queries into one call:

```python
def cmd_context(args):
  db = _get_db(args.db)
  topic = args.topic

  total = db.count()

  # Relevant matches (always hybrid search)
  matches = db.search(text=topic, filter=search_filter, limit=limit)
  # Recent memories (by last update, not creation)
  recent = db.list(sort="updated", limit=5)
  # Frequently accessed (only show if any have been accessed)
  frequent = db.list(sort="count", limit=3)
  frequent = [r for r in frequent if r.get("access_count", 0) > 0]
  # Stale memories (created 30+ days ago, never accessed)
  thirty_days_ago = time.time() - 30 * 86400
  stale_candidates = db.list(sort="created", limit=20, before=thirty_days_ago)
  stale = [r for r in stale_candidates if r.get("access_count", 0) == 0][:5]
  # Type distribution
  type_dist = db.type_distribution()
```

The output is a single Markdown document with sections:

```
## Relevant Memories: "kafka architecture"
- a1b2c3d4 [0.85] Chose event sourcing over CQRS because...

## Recent Memories (by last update)
- e5f6a7b8 [decision] Switched from Avro to Protobuf...

## Frequently Accessed
- c9d0e1f2 (12 hits) Kafka partition key strategy...

## Stale Memories (30+ days, never accessed)
- g3h4i5j6 WAL mode enables concurrent reads...

## Stats
Total: 47 memories | Types: debugging: 12, decision: 15, ...
```

**Why one command beats five**: Latency. Token budget. Cognitive load. An agent calling `search`, then `list --sort access_count`, then `list --sort updated_at`, then `stats` separately wastes four round-trips and produces four separate outputs to parse.

The [compact mode](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L356-L374) goes further -- truncating IDs to 8 chars, content to 100 chars, and emitting flat JSON optimized for agent parsing:

```python
def _compact_entry(r):
  entry = {"id": r["id"][:8], "content": r["content"]}
  if r.get("score") is not None:
    entry["score"] = round(r["score"], 4)
  meta = r.get("metadata")
  if meta and isinstance(meta, dict) and "type" in meta:
    entry["type"] = meta["type"]
  return entry
```

---

## Principle 5: Smart Defaults, Explicit Overrides

The default behavior should be the right behavior 90% of the time. Flags exist for the other 10%.

**Deduplication**: Look at how [`cmd_store()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L117-L145) handles the default:

```python
def cmd_store(args):
  db = _get_db(args.db)
  meta = _parse_json(args.meta, "--meta", use_json=args.json) if args.meta else None
  _warn_unknown_type(meta)

  # Determine dedup threshold
  dedup_threshold = None
  if not args.no_dedup:
    dedup_threshold = args.dedup_threshold  # defaults to 0.92

  result = db.insert(args.content, vector=vector, metadata=meta,
                     dedup_threshold=dedup_threshold, no_embed=args.no_embed)

  mid = result["id"]
  action = result["action"]

  if action == "deduplicated":
    print(f"Deduplicated: {mid} (updated existing memory)")
  else:
    print(f"Stored: {mid}")
```

The agent doesn't need to check for duplicates first. The Rust core's [`insert()`](https://github.com/archit15singh/memori/blob/main/memori-core/src/storage.rs#L78-L121) does the heavy lifting -- auto-embedding the content, finding duplicates by cosine similarity within the same memory type, and either updating the existing record or creating a new one:

```rust
pub fn insert(conn: &Connection, content: &str, vector: Option<&[f32]>,
              metadata: Option<Value>, dedup_threshold: Option<f32>,
              no_embed: bool) -> Result<InsertResult> {
    let id = uuid::Uuid::new_v4().to_string();

    // Auto-embed if no explicit vector and not suppressed
    let auto_vec = if no_embed { None } else { auto_embed(content, vector) };
    let effective_vec = vector.or(auto_vec.as_deref());

    // Dedup check: if we have a vector and dedup is enabled, look for duplicates
    if let (Some(threshold), Some(vec)) = (dedup_threshold, effective_vec) {
        let type_filter = metadata.as_ref()
            .and_then(|m| m.get("type"))
            .and_then(|t| t.as_str());

        if let Some(dup_id) = find_duplicate(conn, vec, type_filter, threshold)? {
            update(conn, &dup_id, Some(content), Some(vec), metadata, false)?;
            return Ok(InsertResult::Deduplicated(dup_id));
        }
    }

    conn.execute("INSERT INTO memories ...", params![id, content, ...])?;
    Ok(InsertResult::Created(id))
}
```

**The asymmetry principle**: The CLI defaults to dedup at 0.92 threshold ([`DEFAULT_DEDUP_THRESHOLD`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L38)). But the Python API defaults to `None` (no dedup). Same underlying function, different ergonomics -- agents accumulate memories and need dedup protection, while library callers may have their own dedup logic.

**Search mode selection**: When an agent passes `--text "query"`, the Rust [`search()`](https://github.com/archit15singh/memori/blob/main/memori-core/src/search.rs#L19-L72) function automatically embeds the text and runs hybrid search. The dispatch is clean:

```rust
let results = match (&query.vector, &query.text) {
    (Some(vec), Some(text)) => hybrid_search(conn, vec, text, ...),
    (Some(vec), None)       => vector_search(conn, vec, ...),
    (None, Some(text)) => {
        if query.text_only {
            text_search(conn, text, ...)         // FTS5 only (agent's explicit choice)
        } else {
            let query_vec = embed_text(text);    // auto-embed
            hybrid_search(conn, &query_vec, text, ...)  // then hybrid
        }
    }
    (None, None) => recent_search(conn, ...),    // fallback to recency
};
```

No flags needed for the common case. `--text-only` exists for when the agent knows lexical matching is sufficient.

---

## Principle 6: Short IDs with Collision Detection

UUIDs are 36 characters. Agents work with tokens. Every character costs something.

The Rust [`resolve_prefix()`](https://github.com/archit15singh/memori/blob/main/memori-core/src/storage.rs#L491-L525) function handles this transparently:

```rust
pub fn resolve_prefix(conn: &Connection, prefix: &str) -> Result<String> {
    if prefix.len() >= 36 {
        return Ok(prefix.to_string());  // full UUID passthrough
    }

    let mut stmt = conn.prepare(
        "SELECT id FROM memories WHERE id LIKE ?1 || '%' LIMIT 2"
    )?;
    let mut rows = stmt.query(params![prefix])?;

    let first = match rows.next()? {
        Some(row) => row.get::<_, String>(0)?,
        None => return Err(MemoriError::NotFound(prefix.to_string())),
    };

    // Check if there's a second match
    if rows.next()?.is_some() {
        let count: i64 = conn.query_row(
            "SELECT COUNT(*) FROM memories WHERE id LIKE ?1 || '%'",
            params![prefix], |row| row.get(0),
        )?;
        return Err(MemoriError::AmbiguousPrefix(prefix.to_string(), count as usize));
    }

    Ok(first)
}
```

Three key design decisions:
1. **LIMIT 2 optimization**: Only fetch two rows. If there's a second match, we know there's ambiguity without scanning the full table.
2. **B-tree range scan**: `LIKE prefix%` on a UUID primary key uses the index. No table scan.
3. **Collision detection, not silent resolution**: The error includes the total match count, giving the agent enough information to retry with a longer prefix.

Every mutation in the [`Memori` facade](https://github.com/archit15singh/memori/blob/main/memori-core/src/lib.rs#L55-L79) calls `resolve_prefix()` automatically -- `get()`, `update()`, `delete()`, `touch()`, `related()`. The agent never manages full UUIDs.

---

## Principle 7: The Behavioral Snippet -- Teaching an Agent *When*, Not Just *How*

This is the most unconventional principle and possibly the most important one. A CLI tool can inject a behavioral guide directly into the agent's system prompt.

Memori's [`cmd_setup()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L753-L832) writes a [106-line snippet](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/data/claude_snippet.md) into `~/.claude/CLAUDE.md`. The snippet doesn't document commands -- `--help` does that. It documents *behavior*:

**When to store** (from the snippet):
- "After fixing a bug where the root cause was not obvious from the error message -- store the root cause chain, not the fix itself"
- "After choosing between alternatives -- store what was chosen and what was rejected with reasoning"
- "When user explicitly states a preference about tools, style, or workflow"

**When NOT to store**:
- "Facts already in CLAUDE.md, README, or inline code comments (don't duplicate)"
- "Session-specific context (current file paths, variable names, temp state)"
- "Anything you're uncertain about -- verify first, store after"

**Content quality guidance**:
- "Each memory should be 1-3 sentences: the insight, the context, and optionally the evidence. If you need more, you're storing a document, not a memory -- use a file instead."

This turns the CLI from a passive tool into an active participant in the agent's decision-making.

**Version-tagged markers** enable the setup command to auto-upgrade stale snippets:

```python
SNIPPET_START = f"<!-- memori:start v{__version__} -->"
SNIPPET_END = f"<!-- memori:end v{__version__} -->"
```

The [upgrade logic](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L808-L824) detects version mismatches and replaces the old snippet:

```python
markers = _find_markers(content)
if markers is not None:
  _, _, old_version = markers
  if old_version == __version__:
    print(f"Memori snippet already present in {target}")
    return
  # Stale version -- re-inject
  start_idx, end_idx, _ = markers
  content = content[:start_idx] + content[end_idx:]
  content += separator + snippet
  print(f"Updated memori snippet in {target} (v{old_v} -> v{__version__})")
```

The tool manages its own documentation lifecycle. No manual intervention needed.

---

## Principle 8: Metadata as Structured Context

Free-text content is searchable but not filterable. Metadata bridges the gap.

```bash
# Store with typed metadata
memori store "Chose SQLite over Postgres" --meta '{"type": "decision", "project": "memori"}'

# Filter by metadata
memori search --filter '{"type": "decision", "project": "memori"}'
```

**Tag coercion**: The [`_parse_tag_value()`](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L230-L244) function auto-types values:

```python
def _parse_tag_value(v):
  """Parse a tag value string into its natural type (bool, int, float, or str)."""
  if v.lower() == "true":
    return True
  if v.lower() == "false":
    return False
  try:
    return int(v)
  except ValueError:
    pass
  try:
    return float(v)
  except ValueError:
    pass
  return v
```

`memori tag a1b2c3d4 count=42 verified=true score=3.14` stores typed values that round-trip correctly through store, tag, and filter.

**Safe filtering in Rust**: The [`build_filter_clause()`](https://github.com/archit15singh/memori/blob/main/memori-core/src/search.rs#L316-L345) function converts JSON filters into `json_extract()` WHERE clauses with key validation against `[a-zA-Z_][a-zA-Z0-9_]*` to prevent SQL injection:

```rust
fn build_filter_clause(filter: &Value) -> Result<String> {
    match filter {
        Value::Object(map) => {
            let mut conditions = Vec::with_capacity(map.len());
            for (key, val) in map {
                if !is_valid_filter_key(key) {
                    return Err(MemoriError::InvalidFilter(...));
                }
                let json_val = match val {
                    Value::String(s) => format!("'{}'", s.replace('\'', "''")),
                    Value::Number(n) => n.to_string(),
                    Value::Bool(b) => if *b { "1".into() } else { "0".into() },
                    _ => format!("'{}'", val.to_string().replace('\'', "''")),
                };
                conditions.push(format!(
                    "json_extract(metadata, '$.{}') = {}", key, json_val
                ));
            }
            Ok(conditions.join(" AND "))
        }
        _ => Ok("1=1".to_string()),
    }
}
```

**Flat equality only**: No nested paths, no operators. This is intentional -- simpler API surface, no injection risk, sufficient for 95% of agent filtering needs. The constraint is documented so agents don't waste tokens trying `{"count": {">": 5}}`.

---

## Principle 9: Stderr for Errors, Stdout for Data

This sounds obvious. It isn't. Getting it wrong creates a class of bugs that are invisible during development and catastrophic in production.

Consider what happens when an agent pipes search results into a file:

```bash
memori search --text "kafka" --json > results.json
```

If the search fails and the error goes to stdout, `results.json` now contains `{"error": "no_embedding", "message": "..."}`. The agent reads this file, tries to parse it as search results, and hallucinates downstream behavior based on an error object it interpreted as data. No crash. No exception. Just silently wrong.

Look at the `_err()` function from Principle 2 again -- both the human-readable and JSON error paths write to `file=sys.stderr`. Success output goes to stdout via `print()`. The separation is absolute, and it's enforced by routing *all* errors through a single function rather than trusting each command to remember.

**The full contract**: Stdout gets data. Stderr gets errors. Exit code `0` means stdout is trustworthy. Non-zero means stderr explains why. An agent that checks `$?` before parsing stdout never misinterprets an error as data.

---

## Principle 10: Idempotent Setup and Graceful Degradation

Agents may run setup commands multiple times. Configuration should be idempotent -- running it twice produces the same result as running it once.

The setup command's [marker detection](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L808-L813) makes this safe:

```python
markers = _find_markers(content)
if markers is not None:
  _, _, old_version = markers
  if old_version == __version__:
    print(f"Memori snippet already present in {target}")
    return  # idempotent -- no changes
```

**Graceful degradation on empty state**: When an agent runs `memori context "topic"` on a fresh database with zero memories, the [output path](https://github.com/archit15singh/memori/blob/main/memori-python/python/memori_cli/__init__.py#L400-L441) returns clean sections with `(no matches)` and `(empty)` -- not errors:

```
## Relevant Memories: "topic"
  (no matches)

## Recent Memories (by last update)
  (empty)

## Stats
Total: 0 memories
```

The agent reads this, understands the database is empty, and moves on. No error handling needed. No special case code. The tool works correctly at every scale, from zero to thousands.

---

## Bonus: Hybrid Search with Reciprocal Rank Fusion

This isn't a CLI design principle per se, but it's a design decision that directly affects agent experience. When an agent searches, should it get lexical matches or semantic matches? The answer is both.

Memori's [`hybrid_search()`](https://github.com/archit15singh/memori/blob/main/memori-core/src/search.rs#L207-L262) runs FTS5 and vector search in parallel, then fuses results using Reciprocal Rank Fusion:

```rust
fn hybrid_search(conn: &Connection, query_vec: &[f32], query_text: &str,
                 filter: Option<&str>, limit: usize, now: f64) -> Result<Vec<Memory>> {
    let candidate_limit = limit * 3;  // over-fetch for better fusion

    let vec_results = vector_search(conn, query_vec, filter, candidate_limit, now)?;
    let text_results = text_search(conn, query_text, filter, candidate_limit, now)?;

    // Build rank maps, collect unique candidates...

    // Compute RRF scores
    let mut scored: Vec<(Memory, f32)> = all_memories.into_values().map(|m| {
        let vec_rank = vec_ranks.get(&m.id).copied().unwrap_or(candidate_limit + 1);
        let text_rank = text_ranks.get(&m.id).copied().unwrap_or(candidate_limit + 1);
        let rrf = 1.0 / (RRF_K + vec_rank as f32) + 1.0 / (RRF_K + text_rank as f32);
        (m, rrf)
    }).collect();

    scored.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    scored.truncate(limit);
    // ...
}
```

RRF uses ranks, not scores, because cosine similarity and BM25 are on incompatible scales. `K=60` is a [tunable constant](https://github.com/archit15singh/memori/blob/main/memori-core/src/search.rs#L10) that controls how much weight goes to top-ranked results. Results are also boosted by access frequency with [exponential time decay](https://github.com/archit15singh/memori/blob/main/memori-core/src/search.rs#L74-L87) (~69 day half-life), so agents naturally get relevant *and* fresh results.

The agent doesn't need to know any of this. It just calls `memori search --text "query"` and gets good results. But the `--text-only` escape hatch exists for when lexical precision matters more than semantic recall.

---

## Putting It All Together

These ten principles converge on a single design philosophy: **make the common workflow transparent and the error path self-correcting.**

An AI agent using a well-designed CLI tool should be able to:

1. Read `--help` and understand what to do
2. Run the command and parse the output
3. Hit an error and know how to recover
4. Never need external documentation

The agent's interaction with your tool is a conversation. The tool's output is its side of that conversation. Design it like you're pair programming with someone who's brilliant but has no context -- because that's exactly what's happening.

| Principle | One-Liner |
|-----------|-----------|
| Dual-mode output | `--json` and `--raw` on every command |
| Errors that teach | What failed, why, and how to fix it |
| Progressive disclosure | Examples in `--help`, warnings over rejections |
| Session start command | One call aggregates multiple queries |
| Smart defaults | Right behavior without flags, overrides when needed |
| Short IDs | Prefix resolution with collision detection |
| Behavioral snippet | Teach *when* to use, not just *how* |
| Structured metadata | Flat JSON, auto-typed tags, equality filtering |
| Stderr/stdout separation | Errors to stderr, data to stdout, always |
| Idempotent setup | Safe to run twice, graceful on empty state |

The best CLI tools for AI agents aren't AI-specific tools. They're well-designed tools that happen to work exceptionally well when the user is a machine. Every principle here -- structured output, teaching errors, smart defaults, graceful degradation -- makes the tool better for human developers too.

The difference is that humans forgive bad design. Agents don't. Design for agents, and humans benefit for free.

The full source is at [github.com/archit15singh/memori](https://github.com/archit15singh/memori).
