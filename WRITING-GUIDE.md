# Writing Guide: Anti-Slop & Editorial Standards

This file is the single source of truth for how blog posts in this repo get written and polished before they go live. Read it before writing, and run the checklist again before pushing to `main`.

> Applies to: **every blog post** in `content/posts/`. This is an editorial standard, not optional style advice.
> The original, full reference is `ANTI-SLOP.md` in [NousResearch/autonovel](https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md). This file distills it, adds the collated resource ranking, and locks in the workflow.

---

## 1. The bar: what "good prose" means here

Slop is text that reads like unedited LLM output: low information density, predictable structure, and vocabulary no human would reach for. The bar for every post is:

- **Specific over vague.** If you can swap the topic and the text still works, it is slop. Say the actual thing, with concrete details, numbers, and examples.
- **A voice.** It reads like a person wrote it, because a person did. Use "I" and "we" where honest. Contractions are fine.
- **One surprising sentence.** Human writing surprises. If a piece contains nothing that makes the reader stop, rewrite.
- **Direct, not hedged.** State it or say you don't know. No "may potentially" chains.

---

## 2. Banned words and phrases

### Kill on sight (Tier 1)

Rarely appear in casual human writing. Rewrite any sentence containing one:

| Slop word | Write instead |
|---|---|
| delve | dig into, look at, examine |
| utilize | use |
| leverage *(as a verb)* | use, take advantage of, depend on |
| facilitate | help, enable, make possible |
| elucidate | explain |
| embark | start, begin |
| endeavor | effort, try |
| encompass | include, cover |
| multifaceted | complex |
| tapestry | (describe the actual thing) |
| testament ("a testament to") | shows, proves |
| paradigm | model, approach |
| synergy / synergize | (delete, restart) |
| holistic | whole |
| catalyze / catalyst | trigger, cause |
| juxtapose | compare, contrast |
| nuanced (as filler) | (cut; show the nuance) |
| realm | area, field |
| landscape (metaphorical) | field, space, situation |
| myriad / plethora | many, lots |

### Suspicious in clusters (Tier 2)

Fine alone; three in one paragraph means rewrite. Use sparingly: robust, comprehensive, seamless, cutting-edge, innovative, streamline, empower, foster, enhance, elevate, optimize, scalable, pivotal, intricate, profound, resonate, underscore, harness, navigate (metaphorical), cultivate, bolster, galvanize, cornerstone.

### Filler phrases (Tier 3) — delete

"It's worth noting that...", "It's important to note that...", "Importantly, ...", "Notably, ...", "Interestingly, ...", "Let's dive into...", "In this section, we will...", "As we can see...", "As mentioned earlier...", "In conclusion, ...", "To summarize, ...", "Furthermore, ...", "Moreover, ...", "Additionally, ...", "In today's [fast-paced] world...", "At the end of the day...", "When it comes to...", "In the realm of...", "Not just X, but Y" *(the #1 LLM rhetorical crutch — restructure)*.

---

## 3. Structural slop patterns

- **The topic-sentence machine.** Don't run every paragraph through *topic sentence → elaboration → example → wrap-up*. Vary the rhythm. Sometimes the point lands last; sometimes a paragraph is one line.
- **List abuse.** Bullets are not a substitute for explaining. Watch for every item starting with the same verb, lists of exactly 3 or 5, and lists nested 3+ deep.
- **Symmetry addiction.** Real writing is lumpy. Some sections are long because the topic is complex. Some are two sentences. Don't force equal-length sections or 3-pros/3-cons balance.
- **The hedge parade.** "can", "may", "might", "could potentially". Human experts state things.
- **Transition-word addiction.** If every paragraph opens with "However / Furthermore / Additionally / Moreover / Consequently", rewrite so paragraphs start with the actual subject.
- **Em dash overload.** More than ~2 per page is a tell. Use commas, periods, or parentheses instead.
- **Empty openings / closings.** No throat-clearing ("In today's world..."). End on your actual last point, not a generic call to action.

---

## 4. The anti-slop checklist (run before every push)

**Word-level**
- [ ] No Tier 1 words. Replace or delete every one.
- [ ] No Tier 2 clusters (3+ in a paragraph → rewrite).
- [ ] No Tier 3 filler phrases.
- [ ] Em dashes: ≤2 per page.
- [ ] No "not just X, but Y" constructions.
- [ ] No "leverage" as a verb.

**Sentence-level**
- [ ] Paragraphs don't all start with transitions.
- [ ] Sentence lengths vary (mix short and long).
- [ ] No hedging chains ("may potentially", "could possibly").

**Paragraph/structure-level**
- [ ] Not every paragraph follows the same template.
- [ ] Sections aren't suspiciously balanced in length.
- [ ] It has a voice; you could tell who wrote it.
- [ ] Opens with the point, not throat-clearing. Ends on the last point, not a formula.

**Smell test**
- [ ] Read it aloud. Does it sound like a person talking, not a press release?
- [ ] Would you be embarrassed if someone asked "did AI write this?"
- [ ] Does it say something specific? Could you swap the topic and it still work?
- [ ] Is there a single surprising sentence?

**Repo-specific additions for this site**
- [ ] No names of the post's sources used as a personal "I mined these people" brag; attribute only where attribution is the content, and even then prefer work titles over profiling the authors.
- [ ] Build with `hugo --minify --cleanDestinationDir` and confirm `public/posts/<slug>/` exists (watch the `buildFuture: false` date trap: a future-dated post silently vanishes).
- [ ] Cover image present in `static/images/uploads/`.

---

## 5. Collated & ranked anti-slop resources

The canonical reference plus a curated set of alternatives/supplements, ranked by how useful they are for absorbing the patterns.

### The baseline

1. **Anti-Slop Reference** — [NousResearch/autonovel `ANTI-SLOP.md`](https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md). The field guide this file is distilled from: banned words, structural patterns, tone-by-context, detection signals, and the checklist. Start here.

### Best complementary reads, in order

2. **[blader/humanizer](https://github.com/blader/humanizer)** — Catalogs 33 concrete AI-writing patterns across content, language, style, and communication, with before/after examples, an explicit final audit pass, and a no-fabrication rule. Best complementary taxonomy.
3. **[milock/humanizer](https://github.com/milock/humanizer)** — 16 structural patterns plus a 3-tier vocabulary system with severity levels (CRITICAL → HIGH → MEDIUM → LOW) and before/after examples with a self-audit pipeline. Best structural analysis.
4. **[Aaron-Bushnell/humanizer](https://github.com/Aaron-Bushnell/humanizer)** — Runs anti-slop as an auditable lint system: 43 editorial patterns, density scoring, voice profiles, and an integrity gate that preserves numbers, citations, URLs, and code. Best if you want rules turned into a linting methodology.
5. **[rcawston/no-ai-slop](https://github.com/rcawston/no-ai-slop)** — 24 anti-slop rules, banned-word lists, structural tells, and a self-check pass. Core rule: replace vague claims with concrete, checkable details. Best concise version.

### Worth skimming for breadth

6. **[spuvr/humanizer](https://github.com/spuvr/humanizer)** — Compact before/after table covering "worth noting", rule-of-three, "it's not X, it's Y", vague attribution, and em-dash abuse.
7. **[harshaneel/humanize](https://github.com/harshaneel/humanize)** — Nine humanization levers (structural flattening, specificity insertion, voice/register, removing softening language) grounded in 50+ cited sources.
8. **[kjmagnan1s/anti-slop](https://github.com/kjmagnan1s/anti-slop)** — A maintained consolidation of avoid-ai-writing / humanizer / stop-slop, with a protect-list so it doesn't flatten your own voice.
9. **[miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop)** — Broader, but its copywriting skill covers headlines, CTAs, tone, fake statistics, AI-writing patterns, and markdown hygiene.
10. **[mrshibly/Humanizer](https://github.com/mrshibly/Humanizer)** — 45+ patterns and perplexity/burstiness engineering; more detector-oriented than actionable for prose itself.

### The recurring high-signal patterns across all of them

Cross-project consensus on what marks AI-generated prose. Watch for these everywhere:

- Significance inflation and generic praise
- Vague attribution ("experts say")
- Fake specificity
- Rule-of-three abuse
- "It's not X, it's Y"
- Manufactured punchlines
- Overuse of em dashes
- "It's worth noting…" / "It's important to…"
- Hollow intensifiers
- Abstract claims without evidence
- Over-structured prose / excessive headings and lists
- AI vocabulary clusters
- Copula avoidance ("serves as", "features", "boasts" instead of "is", "has")
- Restating the obvious
- Performative conclusions
- Generic "actionable" advice
- Claims without concrete examples

---

## 6. Writing workflow (lock this in)

1. **Write it like a person first.** Draft the post with a voice, specific details, and one surprising sentence. Don't auto-hedge.
2. **Run the checklist in §4.** Kill every banned word, filler phrase, and structural tell.
3. **Build locally** with `hugo server` and `hugo --minify --cleanDestinationDir`. Confirm the post appears in `public/posts/` (date must be past/current or it silently drops).
4. **Add the cover image** to `static/images/uploads/`.
5. **Push to `main`** — the GitHub Actions workflow deploys to Pages.
6. **Verify live** with `curl` on the published URL, then open it.

---

*Last updated: 2026-08-30. Source-distilled from the ranked list in §5; the load-bearing standard is the checklist in §4 and the baseline in §5(1).*
