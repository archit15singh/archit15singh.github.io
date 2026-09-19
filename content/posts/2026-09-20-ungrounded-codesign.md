---
title: "Ungrounded co-design"
description: "I typed 'add search' and agreed to 1,400 lines of ranking features I never signed off. A plan dump reads as a spec, and silence reads as acceptance."
date: 2026-09-20T02:30:00+05:30
tags: [AI, Agents, Engineering]
categories: [AI]
cover:
  image: "/images/uploads/ungrounded-codesign-banner.webp"
  alt: "A decision tree where only one branch is signed and the rest default"
  hidden: false
---

I typed "add search" and went to make tea. Ten minutes later the agent had a plan: inverted index, query parser, ranking features, a `search_events` table, dashboards for zero-result queries. Every heading said search. I said go.

The PR was 1,400 lines. The lesson list still had no search box. There was a new page that ranked posts by a score I had never named.

I did the usual postmortem and tightened the prompt: "Simple filter on the existing list. No new index." Next session the agent built a smaller index.

The model was not being lazy. It was building where I had gone silent, and that failure is specific enough to name.

## Silence reads as acceptance

Grounding cost theory (Clark and Brennan, 1991) says two people build shared understanding in two steps: you present something, the other person accepts it, and only then is it common ground. The bar for acceptance is deliberately low, just enough understanding for current purposes, because repairing later is expensive and accepting now is cheap. I have been skipping the accept step. When the plan lands, I skim the headings and feel the pull to type go. Non-rejection is fatigue with a checkbox, not a choice.

A plan dump exploits that cost. Twenty decisions arrive in one markdown file, and walking each branch is expensive enough that silence wins. The defaults land in git as if I had chosen them. Auth method, session storage, whether old lessons get points, whether the box filters or ranks. I signed none of those, then paid for the code.

I call those priors unowned decisions. A silent default has no owner. If it blows up in production, the blame meeting hunts for a prompt, and the prompt never contained the decision. The gap did.

## Sign the root before the leaves

The roots are cheaper to sign than the leaves. If we have not decided filter versus rank, the ranking table is a fiction. If we have not decided magic link versus password, the session store is a fiction. This is what I mean by ungrounded co-design: two designers, one of them a sampler, acting as if they share a picture they have not checked.

The Copilot studies say the same thing from the measurement side. In an observational study of 20 programmers, sessions split into acceleration, where the person already knew the next step and the model typed faster, and exploration, where the person foraged in the suggestion pane and let the model drive. Exploration took more than twice the wall-clock time (248.6 minutes across the whole study). A controlled CHI 2022 experiment found people preferred the assistant even though they could not understand, edit, or debug the snippets it wrote. Preference without a shared picture. My "add search" was exploration I never left: I had a vibe, no next step, so the model supplied the tree and I rode it until the PR existed. Then I called the tree wrong, which it was, because I had never gotten on it.

The plan file is a projection, not the conclusion. Rachael Luck watched architect-client meetings where both sides pointed at the drawings and meant something else, and Frederick Brooks's design-diary experiment found "surprisingly little" benefit from extracting a decision tree from 180 pages of notes after the fact. Capture after the conversation cannot replace the conversation. A PRD written later helps the next session; it does not give that session the concept. Reset the agent and the concept dies. The markdown is a note for a deaf intern, not the intern's brain.

## A stop I can run

Here is the gate I run before I type go in plan mode.

Facts first, off my plate. The agent reads the repo. I do not narrate the filesystem to it.

Decisions in dependency order. One unsigned branch at a time when the branches hang off each other. Independent branches can come as a batch, each with a recommended answer I can refuse. The recommendation is an affordance, not a summary; rubber-stamping it reprints plan mode with extra ceremony.

Stop when a fresh session, given only a short note, could continue without asking. That is the test: paste the note into an empty chat. If the model has to ask a product question, I skipped a signature. If it only asks where the files live, I skipped a lookup that belonged in the note. If it can start, we start. A new product surface and a typo fix do not share a stop point.

I still build with agents every day. The change is the gate, not the tool. The stronger the plan artifact gets, the more the unsigned branches hide in it, so the gate has to get stricter to keep pace. This is one of the failure modes I track on the [reliable agent systems](/research/#2--reliable-agent-systems) line.

The code I got from "add search" was a map of my silences. Next time I will sign the branches, or the model will.