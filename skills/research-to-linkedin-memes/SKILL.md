---
name: research-to-linkedin-memes
description: End-to-end pipeline that SOURCES a research paper (via the openalex CLI or recursive online research), ANALYSES it by breaking the concept into a recursive taxonomy and searching each node, then CREATES ranked meme + LinkedIn-post options for you to pick in a browser UI that also teaches the paper's concept with a worked example. Use when the user says "make a meme post from research", "find a paper and meme it", "turn this concept/paper into a LinkedIn post", "research-to-meme", or hands over a topic, a paper, or an OpenAlex/arXiv link and wants LinkedIn content drafted. Nothing auto-posts.
---

# research-to-linkedin-memes

Go from a topic to publish-ready LinkedIn content in one loop: **source** a research paper, **analyse** it by decomposing the concept and searching each part, **create** several meme + post options, and **review** them in a browser UI that also explains the concept as a learning moment. Personal, single-user. **Nothing auto-posts** — you pick, edit, and paste.

Pipeline: **Source → Break down → Search each node → Explain → Meme → Review + select.**

## Voice: how everything gets written

Every piece of text this skill produces — your chat replies, the concept explainer, the meme captions, the LinkedIn copy, all of it — is written in one voice:

- **`/say-it-plain`**: plain words, spoken human-to-human, no jargon, but every fact/number/name exact. This is the default for the agent's own replies too, not just the artifacts.
- **`/deslop`**: run the deslop skill over any drafted prose (explainer, captions, post copy) before it reaches the UI. Strip AI tells, filler, and the Tier-1 banned words.
- **`WRITING-GUIDE.md`** (repo root) is the editorial bar: specific over vague, a real voice, one surprising sentence, direct not hedged. The explainer and the LinkedIn copy must pass it.

If you can swap the topic and the sentence still works, it's slop — rewrite it.

### Never reference the source paper in anything the user sees

The paper is *fuel*, not content. Do **not** name the paper, its authors, its title, or its branded technique name in the explainer, the meme captions, or the LinkedIn post. Teach the idea in your own plain framing and, where a name helps, a plain descriptive one you coin ("branch-and-backtrack reasoning"), never the paper's term. Keep the real citation only in the on-disk `explainer.json`/`selection.json` provenance (never posted, never rendered) so you can trace it later. A LinkedIn post that reads like a citation is a worse post.

### LinkedIn post craft (from what actually gets read)

Hold every `linkedin_post` to this, on top of the writing bar:

- **Hook in line one, under ~10 words**, and it must land before the "see more" fold (~140-210 chars in). The first two lines decide 80% of whether anyone reads on. Best hook types: contrarian claim, a specific number, a pain-point confession, or an unexpected comparison.
- **White space is the format.** Short paragraphs, 1-3 sentences each; single-line sentences; blank line between beats. Dense blocks get scrolled past no matter how good the idea.
- **Shape:** hook → the payoff in the next line or two → the substance (a short framework, contrast, or story, manual `→`/`-` bullets if listing) → a closing question that invites a reply.
- **Restraint:** at most one emoji and only if it earns its place; ALL CAPS almost never; no hashtag spam. Target a tight ~600-1,300 characters for a meme post (the meme carries the joke; the copy earns the click).

## Decisions this bakes in

- **Audience**: you, to ship LinkedIn content more often and actually understand what you post. Not a SaaS.
- **Human in the loop**: the agent drafts several options; you review and Select one. Never auto-post.
- **Source of truth is a real paper.** Ground the meme + post in an actual work found via `openalex` (or recursive online research), so the LinkedIn post can cite something real and the explainer teaches something true.
- **The UI teaches, not just picks.** The review page carries a plain-language explainer of the paper's concept + a worked example, above the meme options.
- **Rendering**: Imgflip `caption_image` API by default (auto-places text in any template); local Pillow is the no-account, watermark-free fallback.
- **Regeneration is a chat request**, not a UI control (see Interactive review UI).

## Prerequisites

Nothing required when a Claude agent drives it. Optional:

```bash
export OPENALEX_MAILTO=you@example.com   # optional: OpenAlex "polite pool" (faster). Nothing sent without it.
export IMGFLIP_USERNAME=...              # only for the Imgflip API render; free account at imgflip.com/signup
export IMGFLIP_PASSWORD=...              # NEVER paste this into a chat — set it in the shell
export ANTHROPIC_API_KEY=...             # only for the standalone (non-agent) scripts
```

`openalex` is at `~/.claude/bin/openalex` — free, no key, stdlib-only. Usage: `~/.claude/tools/openalex_usage.md`.

## Pipeline

### 1. Source the paper

Start from whatever the user gives — a topic, a concept, a paper id, or an arXiv/OpenAlex link.

```bash
# Rank papers on a topic by a blend of impact + recency + relevance. NOTE: -o is GLOBAL (before the subcommand).
~/.claude/bin/openalex -o json search "self-improving language model agents" -n 15

# All-time most-cited works for a concept
~/.claude/bin/openalex -o json top "artificial intelligence" -n 10

# Full quality report for one work id (W... from search/top output)
~/.claude/bin/openalex -o json score W4323655724
```

`search` returns `id, title, year, cited_by_count, relevance_score, blended_score, authors, doi`. Pick a strong, real paper (high blended score, on-topic, ideally open-access so you can read it). If the user gave a link, resolve it and read the abstract/paper.

**Recursive online research (also valid):** when OpenAlex is thin or the concept is practitioner-canon (blog-shaped, not paper-shaped), use `WebSearch`/`WebFetch` instead — search the concept, read the best primary sources, and treat those as the "paper." The rest of the pipeline is identical; the explainer just cites the source you actually used.

### 2. Break the concept into a taxonomy, search each node

Decompose the paper's core idea into a small **recursive tree** of sub-concepts (the ontology of the idea), then search each node to collate meme/LinkedIn angles from across the tree — not just the top-line claim.

- Write the tree: the concept → its 3-5 child sub-concepts → (optionally) one more level on the richest child. **Cap depth at 2 and ~3-5 nodes per level.** Stop expanding a branch as soon as new nodes stop adding a *distinct* angle (same saturation rule as any recursive research loop — consecutive dry nodes = done).
- For each node, do a quick `openalex search` and/or `WebSearch` to find the sharpest framing, contrast, or surprising result at that node.
- **Collate + rank angles**: across all nodes, list candidate meme/post angles and rank by (a) how surprising/clickable and (b) how faithful to the source. The top 3 distinct angles become your 3 options in step 5.

Keep the tree in the run dir as `taxonomy.json` if useful; the node names also feed the explainer's "how we searched it" chips.

### 3. Write the concept explainer (the learning panel)

Draft a rich, plain-language explainer so the reader *gets it intuitively* — this is what makes the UI a learning tool, not just a picker. Write it in the skill's voice (say-it-plain + deslop + WRITING-GUIDE), and give it an analogy, the mechanism as steps, several examples, and a small visual. **Do not put the paper's name/authors in the rendered fields** — keep `paper` only as private provenance (the UI never renders it):

```json
{
  "paper": {"title": "...", "authors": "...", "year": 2023, "url": "...", "doi": "..."},
  "concept": "Plain descriptive name of the idea (NOT the paper's branded term)",
  "hook": "One line that makes the idea click.",
  "plain": "2-4 sentences: what the idea is, in plain words, exact but jargon-free.",
  "analogy": "One everyday analogy a non-expert can picture.",
  "how_it_works": ["step 1", "step 2", "step 3", "step 4"],
  "examples": ["concrete example 1", "example 2 from a different domain", "example 3"],
  "visual": "A small ASCII diagram (rendered in a monospace block) that shows the shape of the idea.",
  "taxonomy": ["node1", "node2", "node3"]
}
```

The server renders `hook`, `plain`, `analogy`, `how_it_works` (numbered), `visual` (monospace), `examples` (list), and `taxonomy` (chips). `paper` is intentionally not rendered.

### 4. Seed the meme template bank (one time)

```bash
mkdir -p bank/images
curl -s "https://api.imgflip.com/get_memes" \
  | python3 -c "import sys,json; json.dump(json.load(sys.stdin)['data']['memes'], open('bank/templates.json','w'), indent=2)"
```

Each entry: `{"id","name","box_count",...}`. `box_count` = number of text slots (Drake=2, Two Buttons=3, Gru's Plan=4). **Emit exactly `box_count` captions.** Optionally write a one-line "use when…" fit-note per template so matching is by meaning, not name.

### 5. Generate the meme + post options

As the driving agent (no API key needed), turn the top 3 ranked angles into 3 options. For each: pick a template whose rhetorical move fits the angle, write exactly `box_count` captions, and write the `linkedin_post` copy following **LinkedIn post craft** above (scroll-stopping hook, white space, closing question) and the **no source-paper reference** rule. Run `/deslop` over every caption and post before rendering.

Each option: `{"id","template","template_id","captions":[...],"post"}`.

### 6. Render

**Default — Imgflip API** (auto-places text into any template's boxes; needs env creds; Free tier watermarks + 500×500):

```bash
python3 - <<'PY'
import json, os, urllib.parse, urllib.request
data = json.load(open("options.json")); opts = data["options"] if isinstance(data,dict) else data
for o in opts:
    boxes = {f"boxes[{j}][text]":c for j,c in enumerate(o["captions"])}
    payload = {"template_id":o["template_id"],"username":os.environ["IMGFLIP_USERNAME"],
               "password":os.environ["IMGFLIP_PASSWORD"], **boxes}
    req = urllib.request.Request("https://api.imgflip.com/caption_image",
        data=urllib.parse.urlencode(payload).encode(), headers={"User-Agent":"Mozilla/5.0"})  # UA required (see gotchas)
    r = json.loads(urllib.request.urlopen(req).read())
    o["meme_url"] = r["data"]["url"] if r["success"] else None
    print(o["id"], o.get("meme_url") or r.get("error_message"))
json.dump(data, open("options.json","w"), indent=2)
PY
```

**Fallback — local Pillow** (no account, watermark-free, 1200×1200) needs a per-template text-region map, so it only covers templates you've mapped. Use for Drake-style two-panel layouts; see Gotchas.

### 7. Build options.json (v2), launch the UI, review

Write the v2 payload to a scratch run dir (e.g. `/tmp/meme-run/`), **never the repo**:

```json
{ "explainer": { ...from step 3... }, "options": [ ...rendered options with meme_url... ] }
```

Launch and watch (looping monitor, so you catch every click):

```bash
cd /tmp/meme-run && python3 /path/to/skills/research-to-linkedin-memes/scripts/review_server.py 8765
open http://localhost:8765/
# watch for the select:
cd /tmp/meme-run; while true; do until [ -f action.json ]; do sleep 1; done; echo "$(cat action.json)"; rm -f action.json; done
```

The page shows the **explainer panel** (paper, concept, plain explanation, example, taxonomy chips) above the meme grid. On `{"type":"select","id":"B","post":"..."}` the server saves the meme + `post.txt` + `selection.json` + `explainer.json` into `output/<timestamp>/`; tell the user the path. Done.

**Regeneration is a chat request.** No button. The user says "regenerate" (optionally with a steer); the agent writes a fresh `options.json` and the open page auto-refreshes (it polls `options.json`). A bare "regenerate" → the agent picks its own short creative steer. The human drives each round, so there's no runaway loop.

**Files (run dir, all gitignored):** `options.json` (v2 batch), `taxonomy.json` (optional), `action.json` (the select), `output/<ts>/` (final meme + `post.txt` + `selection.json` + `explainer.json`).

## Gotchas

- **`openalex -o json` — `-o` is a GLOBAL flag before the subcommand** (`openalex -o json search ...`), not after. `search ... -o json` errors with "unrecognized arguments".
- **Cap the taxonomy recursion**: depth 2, ~3-5 nodes/level, stop a branch when it stops adding a distinct angle. Unbounded concept-tree search burns time and tokens for diminishing returns.
- `box_count` mismatch is the #1 render failure — Imgflip silently mis-renders a wrong count. `box_count` is the *default* slot count; emit exactly that many and validate before rendering.
- Free Imgflip accounts keep a minimal watermark and downsize to 500×500; `no_watermark` is Premium. Local Pillow avoids both.
- **Imgflip `caption_image` returns HTTP 403 to Python `urllib`'s default user-agent.** Set `headers={"User-Agent":"Mozilla/5.0"}` on the render POST *and* when downloading `meme_url`. A 403 here is the UA, not bad creds.
- **Text placement is per-template** for the local Pillow render (Drake = right half of each panel). The Imgflip API sidesteps this by auto-placing into default boxes.
- **Never paste an Imgflip password into a chat.** Env var only; rotate if it leaks.
- **Run the UI in a scratch dir, never the repo.** The shipped `.gitignore` covers the runtime files, but keeping the run dir outside the repo avoids ever committing generated images to a public repo.
- Meme taste and paper faithfulness are what's most likely to be wrong — that's why this generates options, grounds them in a real source, and gates on a human.

## When you build a fuller standalone version

To run without an agent watching, add a backend that calls the `openalex` CLI + Claude (needs `ANTHROPIC_API_KEY`) to source, decompose, explain, and generate — and keep the same `review_server.py` page (it already renders the v2 `{explainer, options}` schema). Keep it local; nothing here needs hosting or auth.
