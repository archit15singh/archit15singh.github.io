# Staff+ enrichment loop prompt (canonical)

Copy this whole prompt into a fresh session to resume or rerun the recursive content-enrichment loop on the Staff+ post. It is version-controlled here so it survives across sessions and stays the single source of truth for how the loop behaves.

---

You are continuing a recursive content-enrichment task on one blog post in this repo. You have NO prior context, so everything you need is below. Work in an autonomous loop until you reach the convergence signal, then stop and summarize.

## The artifact
`content/posts/2026-08-30-the-staff-plus-operating-model.md` — a dense, already-comprehensive synthesis of the Staff+ engineering career track (Senior → Tech Lead → Staff/Principal). It is a finished field guide, not a draft: leadership without authority, the four archetypes, the pillars, the project and operating playbooks, promotion arithmetic, leading through failure, time/attention, the pendulum vs ladder, the glue warning, and a compressed operating model in fourteen lines.

## The task
Recursively research the same broad theme online and enrich this post by folding genuinely new, non-redundant material into it, round after round, until coverage converges.

## Ground rules (non-negotiable)
1. **Additive only.** Weave new insight into existing sections. Do not create new top-level headings unless something genuinely demands one. If a search surfaces material the post already covers, that's redundancy — skip it. Only ship content that adds a *distinct operating capability, framework, data point, or counterpoint* the post currently lacks.
2. **Primary sources first.** Prefer the canonical practitioner sources (staffeng.com, lethain.com, leaddev.com, Tanya Reilly's "Being Glue" at noidea.dog, the incident-command/IC literature, decision-framing essays). Use broader web search for gaps. Academic paper search tooling exists but this canon is blog-posts-and-books; plain web search is usually the right tool.
3. **Write to this repo's editorial standard** (read `WRITING-GUIDE.md` at the repo root): specific over vague, a real voice (I/we, contractions), one surprising sentence, no Tier-1 banned words, no filler phrases, em dashes kept lean in newly added text, no "not just X but Y." Run the checklist after every edit.
4. **NEVER leak internal methodology into the published post.** The blog is the reader-facing field guide only. Do not publish anything that exposes how it was researched or synthesized: no meta-commentary about mining, collating, cross-verifying, chasing sources, recursion, rounds, saturation, or ranking sources "by ROI." The post is written as direct operating guidance with no visible reference to its sources or the process that produced it. (Historically this meant an explicit ban on a "how to mine it yourself in waves" section and a "material, collated and ranked" reading list — those already existed and were removed. Keep them gone. If new research suggests something that reads as process-methodology rather than direct advice, fold in the *insight* only and drop the meta framing.) Think of it as: every finished sentence must stand as useful advice to a reader who has no idea a research loop exists.
5. **Verify before shipping.** After edits: `hugo --minify --cleanDestinationDir`, confirm `public/posts/2026-08-30-the-staff-plus-operating-model/index.html` still contains your additions (and watch the `buildFuture: false` date trap). Then `git commit` + `git push origin main` — one commit per round with a clear message.
6. **The convergence signal that stops the loop:** a fresh research round adds **zero distinct new operating capabilities** — nothing a reader would need that the post doesn't already handle. Coverage is qualitative, not citation-count. When a round adds nothing new, that's the dry round; one more confirm-pass to make sure isn't early stopping, then stop and report.
7. **Track your saturation** in `.enrich-loop/ledger.tsv` (round/queries/new_sources/areas/dry) so a later session can resume if you stop mid-way.
8. **Document gotchas** you hit into the repo's `CLAUDE.md` (rate limits, tool quirks, surprising behaviors) so future sessions of this loop don't relearn them.

## History (what's already been added, so you don't redo it)
The post has already received these deepened areas — you are continuing past them, not repeating:
- Time-allocation reality (20-40% coding; writing amplifies; "horizon of focus" / multi-scale planning)
- Incident-command mechanics (IC coordination vs debugging; IC vs tech-lead split; mitigation vs resolution)
- Glue-work objectivity (which glue compounds vs traps) + manager-side rubric fixes
- "The room" / visibility mechanics (bring something the room lacks; transient visibility currency)
- Two-way-door engineering surgery (feature flags/canaries as reversibility; disagree-and-commit)
- PM/tech-lead partnership mechanics (handoff vs shared ownership failure modes)
- Presenting up to the executive layer (preprocessed reality, SCQA, never fight feedback)
- Problem discovery (sponge habit, common-shape finding, loop compounding)
- Bottom-up technical strategy writing (five design docs to a strategy, slow rollout)
- Setting the standard as a fourth pillar (role-model culture, values-are-what-gets-promoted)

## Start here
Pick a thin sub-area the post still doesn't develop and begin the loop. Don't ask me for permission each round — run the loop autonomously to convergence. When you stop, report: which capabilities each round added, the ledger showing saturation, and a short coverage note on what's now in the post that wasn't before.
