---
title: "Self-Improving AI Agents: A Recursive Taxonomy"
description: "Six families of self-improving AI agent, 109 methods, ranked: what each one changes about itself, how durable that change is, and the handful that matter."
date: 2026-09-22T01:30:00+05:30
tags:
  - AI
  - Agents
  - Engineering
  - Research
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/self-improving-agents-taxonomy-banner.webp"
  alt: "A branching map of self-improving agent families, from single-answer refinement to recursive self-modification"
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

# Self-Improving AI Agents: A Recursive Taxonomy

An agent that gets better on its own isn't one idea. It's at least six, and they differ by how much of the agent is allowed to change. This post sorts the 2023 to 2026 work into six families, names 109 methods across them, and ranks them all. It's the map.

Two questions separate every method here.

**What does the agent change about itself?** Its prompt, its stored experience, its tools, its own design, its source code, or the world it trains in.

**How durable is that change?** Either it's text the agent reads back later, which I call *in-context*, or it's a rewrite of weights, code, or environment, which I call *structural*. In-context improvement vanishes when you clear the buffer. Structural improvement survives a restart.

Almost every method below is one cell in that grid. And one mechanism runs through all of them: turn an execution result, a passed test, a self-critique, or a majority vote into a learning signal, and feed it back.

The families run from how little the agent touches to how much: from polishing a single answer, up to rewriting the codebase that produced it, and finally to co-evolving with its own training environment. There's a seventh kind I've left out on purpose, model-centric self-training (STaR, RLAIF, self-play weight updates), where the agent retrains its own weights. Dropping it is why the numbering skips 4 and runs 1, 2, 3, 5, 6, 7.

Here's how the 109 methods distribute:

| Family | Kind | Methods |
|---|---|---|
| 1. Self-refinement / reflection | in-context | 16 |
| 2. Memory-based evolution | in-context | 23 |
| 3. Tool-based evolution | in-context | 21 |
| 5. Automated agent / architecture design | structural | 15 |
| 6. Recursive self-modification | structural | 15 |
| 7. Co-evolution / open-ended | structural | 19 |

Memory-based work leads. Durable, in-context experience is where the most recent research clustered, because it buys cross-session competence without paying to retrain anything.

## 1. Self-refinement / reflection (in-context)

The agent generates output, critiques it in plain language, and retries. It improves at test time with no weight update. This is the cheapest form of self-improvement and the one most systems already ship.

The seed method is [**Self-Refine**](https://arxiv.org/pdf/2303.17651): generate, feed back on your own work, refine, repeat. [**Reflexion**](https://arxiv.org/pdf/2303.11366) made it stick by turning scalar feedback into a written reflection stored in episodic memory, used as a semantic gradient on the next episode. [**CRITIC**](https://arxiv.org/pdf/2305.11738) and [**Chain-of-Verification**](https://arxiv.org/pdf/2309.11495) point the critique outward: CRITIC verifies against external tools in a Verify, Critique, Correct loop, and CoVe drafts, writes its own verification questions, answers them independently, then revises to cut hallucination.

The other half of this family isn't one agent thinking harder but many samples voting. [**Self-Consistency**](https://arxiv.org/pdf/2311.17311) samples diverse reasoning paths and majority-votes the answer. **Best-of-N** keeps the best of N candidates by scoring. [**Multi-Agent Debate**](https://arxiv.org/abs/2305.14325) has several models argue to cross-verify claims. And [**test-time compute scaling**](https://arxiv.org/abs/2408.03314) simply spends more inference on longer chains with per-step reflection, with adaptive variants that hand out that budget by confidence instead of a fixed cap.

One honest caveat: iterative revision has diminishing returns after three or four rounds. More loops isn't free accuracy.

## 2. Memory-based evolution (in-context)

Agents build up experience in an external, durable store and pull it back across tasks. Weights never change; the store does.

The canonical example is [**Voyager**](https://arxiv.org/abs/2305.16291), whose skill library is an executable-code repository of behaviors that worked, retrieved and composed for new tasks. [**MemGPT**](https://arxiv.org/pdf/2310.08560) is the systems take: virtual context paging across working, recall, and archival tiers, memory managed the way an OS manages RAM. Both treat memory as infrastructure, not as a log.

Underneath sit the harder problems. What do you keep, and how do you find it again? [**SelfMem**](https://arxiv.org/pdf/2607.03726) and [**MEM1**](https://arxiv.org/pdf/2506.15841) learn the store/compress/retrieve/discard policy itself from feedback rather than hard-coding it. [**A-MEM**](https://arxiv.org/pdf/2502.12110) and [**AtomMem**](https://arxiv.org/pdf/2606.19847) fight context pollution, one with agent-driven retrieval, the other by breaking memories into atomic facts with temporal profiles. A cluster of graph methods ([**experience graphs**](https://arxiv.org/pdf/2606.29823), [**GAM**](https://arxiv.org/html/2604.12285v1), [**ReaGAN**](https://arxiv.org/html/2508.00429v3)) argue that memory should be a structured causal object, not a flat vector index, so you can retrieve a whole reasoning subtree instead of a paragraph.

There's also a prompt-optimization corner here (**MemAPO**, [**DelvePO**](https://arxiv.org/pdf/2510.18257), [**MemPro**](https://arxiv.org/pdf/2606.00619)) that stores winning templates and error patterns as evolvable programs, and a belief-memory corner ([**BeliefMem**](https://arxiv.org/pdf/2605.05583)) for agents acting under partial observability, holding candidate conclusions with probabilities and updating confidence as evidence arrives.

## 3. Tool-based evolution (in-context)

Agents write, test, and refine new tools, or get better at using the tools they already have. If family 2 remembers what worked, family 3 remembers it as a callable function.

[**Toolformer**](https://openreview.net/pdf?id=Yacmpz84TH) is the landmark, and it's self-supervised: the model annotates its own corpus with API calls, learning when and how to invoke a tool without human labels. From there the field splits.

One branch builds tools on demand. **CREATOR** abstracts a reusable function from a concrete use so it transfers. [**CRAFT**](https://github.com/jjakimoto/research-issues/issues/1605) and [**TroVE**](https://arxiv.org/pdf/2507.21046) curate validated code snippets with dedup and simplicity metrics so the toolset stays clean. [**ATLASS**](https://arxiv.org/pdf/2503.10071) closes the loop: decide whether a tool is needed, retrieve or generate it, then set up the environment to run it.

Another branch evolves tools at inference time rather than in training. [**Live-SWE-Agent**](https://www.emergentmind.com/topics/live-swe-agent) continuously rewrites its own scaffold online, self-validated. [**SkillGen**](https://arxiv.org/pdf/2605.10999) and [**SkillWeaver**](https://arxiv.org/pdf/2504.07079) distill auditable, reusable skills out of trajectories by contrasting successes against failures. A tool is really just a piece of experience that happens to be executable, so every memory question from family 2 comes back here in code form.

## 5. Automated agent / architecture design (structural)

Now the change becomes durable. A meta-agent or outer optimizer discovers, evolves, or synthesizes new agent designs, modules, or workflows, and the result is a new artifact, not a longer context window.

[**ADAS**](https://arxiv.org/abs/2408.08435) searches over agent codebases to invent new building blocks, an LLM writing the architecture of the next LLM agent. [**AgentSquare**](https://arxiv.org/abs/2410.06153) narrows that to a modular space (Planning, Reasoning, Tool, Memory) and uses an in-context surrogate to predict which combination will work before paying to run it.

The prompt-optimization work is the most production-ready slice. [**DSPy**](https://arxiv.org/abs/2310.03714) compiles typed modules into few-shot examples and instructions via Bayesian search, and it's widely adopted because it treats the prompt as a compiler target rather than a craft. [**EvoPrompt**](https://arxiv.org/abs/2309.08532) does discrete prompt optimization with genetic algorithms. [**PromptBreeder**](https://arxiv.org/pdf/2309.16797) goes self-referential: the mutation-prompts that edit your task-prompts are themselves evolving. Alongside these, [**GPTSwarm**](https://arxiv.org/abs/2402.16823) and [**EvoAgent**](https://arxiv.org/abs/2406.14228) generate whole multi-agent systems, one by optimizing the graph topology of agents, the other by mutation and crossover over a single expert.

## 6. Recursive self-modification (structural)

The agent rewrites its own code, prompts, or architecture, and each improvement raises its ability to improve itself. This is the family everyone means when they say "recursive self-improvement," and it's where theory and practice diverge hardest.

The theory anchor is Schmidhuber's [**Gödel Machine**](https://link.springer.com/chapter/10.1007/978-3-540-68677-4_7): it rewrites its own code only after *proving* the change raises expected utility. Provably safe, practically unbuildable. What actually shipped is the empirical version. Sakana's [**Darwin Gödel Machine**](https://sakana.ai/dgm/) drops the proof, tests code mutations directly, and keeps improvements by selection, moving SWE-bench from 20% to 50%. [**SICA**](https://arxiv.org/pdf/2504.15228) edits its own Python codebase after inspecting its own failures, 17% to 53% on SWE-Bench Verified. [**AlphaEvolve**](https://www.mindstudio.ai/blog/what-is-alphaevolve-google-ai-self-improvement-2) runs an LLM ensemble to generate and score algorithmic candidates, feeding the best back as the next round's seed.

This family also carries the only part of the map that's mostly warnings. Self-modifying agents can alter their own safety measures, amplify a misspecified objective a little more each cycle, or collapse into representation drift under unbounded iteration. The safety papers here aren't decoration. They're the reason "let it edit itself" is still a research setting and not a default.

## 7. Co-evolution / open-ended (structural)

The agent and its environment, curriculum, or opponent improve together. There's no fixed task distribution, so there's no fixed ceiling.

[**POET**](https://dl.acm.org/doi/10.1145/3321707.3321799) keeps a population of environment-agent pairs and mutates the environments under a "not too easy, not too hard" filter, so the curriculum chases the agent's frontier on its own. [**PAIRED**](https://arxiv.org/abs/2012.02096) makes that adversarial: a protagonist and antagonist compete while a third agent designs tasks that maximize the regret gap between them. OpenAI's [**hide-and-seek**](https://arxiv.org/abs/1909.07528) self-play produced six emergent strategic phases, including tool use, with no reward shaping at all, just competition.

Around those sit the curriculum machinery ([**ACCEL**](https://arxiv.org/abs/2203.01302) editing high-regret levels to hold them at the capability frontier, [**Prioritized Level Replay**](https://arxiv.org/abs/2010.03934) picking levels by learning potential) and the quality-diversity search ([**MAP-Elites**](https://www.emergentmind.com/topics/map-elites-algorithm) keeping the best solution per cell of a feature space) that keeps the population diverse instead of collapsing onto one strategy. The newest entrants ([**GenEnv**](https://arxiv.org/abs/2512.19682), [**SEAL**](https://arxiv.org/abs/2605.24426), [**COvolve**](https://arxiv.org/html/2603.28386)) put an LLM on both sides, generating and mutating the environment in step with the policy.

## Which of these actually matter

I scored every method on four axes and combined them into a 0 to 100 composite:

- **Relevance.** How directly it embodies self-improvement, versus a general technique borrowed into the field.
- **Influence.** How much later work builds on it. Seminality and recognition.
- **Reputation.** Venue and lab. A top peer-reviewed venue or a major industry lab outranks a workshop, which outranks an unreviewed preprint.
- **Maturity.** Real adoption and reproduction, versus a single fresh preprint.

One caveat, and it's the difference between honest and fake precision: these scores are a qualitative rubric, not scraped citation counts. I couldn't verify live citation numbers for 109 papers, many of them 2026 preprints sitting near zero. So the scores encode seminality, venue and lab reputation, and adoption maturity as reasoned estimates. Read them as tiers, not decimals.

The landmark tier, top 12:

| # | Method | Family | Composite |
|---|---|---|---|
| 1 | Toolformer | Tools | 96 |
| 2 | Reflexion | Self-refine | 95 |
| 3 | Self-Consistency | Self-refine | 95 |
| 4 | Voyager | Memory / Co-evo | 94 |
| 5 | Self-Refine | Self-refine | 93 |
| 6 | MemGPT | Memory | 92 |
| 7 | DSPy | Auto-design | 92 |
| 8 | Multi-Agent Debate | Self-refine | 90 |
| 9 | CRITIC | Self-refine | 89 |
| 10 | Chain-of-Verification | Self-refine | 88 |
| 11 | Darwin Gödel Machine | Recursive | 88 |
| 12 | AlphaEvolve | Recursive | 88 |

Below the landmarks the field sorts into bands. The **Established** tier (70 to 79) is where reproduced-but-not-canonical work lives: AgentSquare, SICA, A-MEM, EvoAgent, SkillWeaver, MAP-Elites, PAIRED. The **Emerging** tier (58 to 69) holds solid recent work that hasn't yet been widely built on. And the **Early-stage** tier (44 to 57) is almost entirely 2026 arXiv preprints: high topical relevance, unreviewed, not yet cited, scored low by construction rather than by any judgment of quality.

## What the ranking says

The top is dominated by 2023 and 2024 peer-reviewed work that named a pattern the field then reused. Reflexion, Self-Refine, Toolformer, Voyager, and DSPy worked, and then they gave everyone else a word for the thing. The two most ambitious families, recursive self-modification and co-evolution, each carry a few high-scoring landmarks (Darwin Gödel Machine, AlphaEvolve, POET) sitting on top of a long tail of fresh, unreviewed preprints.

High relevance and low maturity is the signature of a field moving fast. The safe, in-context families are mature and shipping. The structural families, the ones where an agent genuinely rewrites itself or its world, are where the interesting risk lives, and most of that work is younger than a year.

If you're building an agent today, the honest reading is: reach for families 1 and 2 first, because they're proven and cheap, use family 3 to make hard-won behavior durable, and treat families 5 through 7 as the research frontier they still are.
