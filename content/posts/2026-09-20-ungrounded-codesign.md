---
title: "Ungrounded co-design"
description: "You skim the plan, type go, and get the wrong feature. The model counted silence as acceptance and wrote defaults into every unsigned branch."
date: 2026-09-20T02:30:00+05:30
tags:
  - AI
  - Agents
  - Engineering
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/ungrounded-codesign-banner.jpg"
  alt: "Two overlapping decision trees on tracing paper, filled in different inks, under a green lamp"
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
UseHugoToc: true
---

I typed "add search" and went to make tea. Ten minutes later the agent had a plan: inverted index, query parser, ranking features, a `search_events` table, dashboards for zero-result queries. The headings said search. I said go.

The PR was 1,400 lines. The lesson list still had no box. A new page ranked posts by a score I had never named.

I did the usual postmortem. Tighter prompt. "Simple filter on the existing list. No new index."

The next session built a smaller index.

---

## Silence is a spec the model will fill

Herbert Clark and Susan Brennan wrote this down in 1991, for people talking. The same cost structure shows up when one of them is a model. A contribution has two phases: you present something, the other person accepts it, and only then does it enter common ground. The bar is low on purpose. You need understanding "sufficient for current purposes." A mind meld is extra. Both of you try to spend as little total effort as possible. Accepting is cheap. Repairing is expensive.

A plan dump exploits that cost. The model presents twenty decisions in one markdown file. Skimming is cheaper than walking each branch. Silence reads as acceptance. The defaults land in git as if I chose them.

Auth method, session storage, whether old lessons get points, whether the box filters or ranks: I signed none of those. The model sampled a prior. I paid for the code.

I have started calling those priors **unowned decisions**. A silent default has no owner. If it blows up in production, the blame meeting will hunt for a prompt. The prompt never contained the decision. The gap did.

---

## Eager plans are a grounding attack

Plan mode wants an artifact. It is good at emitting one. It is bad at waiting.

You get a tree of choices, already filled, in the shape of a document you can approve. Approval here means "I did not object." That is a different speech act from "I chose this." Clark and Brennan's grounding criterion was mutual belief that the listener understood the speaker. Non-rejection of a 400-line plan is fatigue with a checkbox.

I have done this to myself on purpose. I watch the plan appear, I feel the pull to type go, and I notice that the pull is the cheap move. The expensive move is to stop at the first unsigned branch and say yes or no to that branch only.

Upstream before downstream. If we have not picked "filter vs rank," the ranking table is a fiction. If we have not picked "magic link vs password," the session store is a fiction. Signing a leaf while the root is still blank is how you throw the leaf away next week.

This is ungrounded co-design. Two designers, one of them a sampler, acting as if they share a picture they have not checked.

---

## Exploration that does not exit

Shraddha Barke, Michael James, and Nadia Polikarpova sat 20 programmers in front of Copilot and coded the sessions. Two modes showed up.

In **acceleration**, the person already knew the next step. The model typed faster. Flow held.

In **exploration**, the person did not know the next step, so they let the model drive. They foraged in the suggestion pane. They validated more. They slowed down.

They timed it. 248.6 minutes in exploration across the study. More than twice the time in acceleration.

My "add search" session was exploration I never left. I had no next step. I had a vibe. The model supplied a tree and I rode it until the PR existed. Then I called the tree wrong, which it was, because I had never gotten on it.

Priyan Vaithilingam, Tianyi Zhang, and Elena Glassman ran a CHI 2022 study with 24 people on Copilot versus ordinary IntelliSense. Copilot did not win on the numbers that were supposed to matter. Task time: 9 minutes 18 seconds versus 10 minutes 23 seconds, not significant. Success: 19 of 24 versus 22 of 24. People preferred Copilot anyway. They could not understand, edit, or debug the snippets it wrote.

Preference without a shared concept. You like the feeling of motion. You do not have a picture you can defend.

---

## The concept is not the file

Frederick Brooks, in *The Design of Design*, treats the design concept as an invisible thing two people gesture at. Rachael Luck spotted it in architect-client talk: they pointed at the drawings and meant something else. They were protecting unity. The paper is a projection. The concept is the thing they are trying to keep intact.

I keep making the opposite move. I let the plan file stand in for the concept, then I get angry when the code, which is a second projection, does not match the picture in my head. Of course it doesn't. The file was the model's picture. I nodded at the headings.

Brooks also logged 180 pages of notes on a house, extracted a decision tree from them, and called the experiment a failure: "surprisingly little" benefit. Capture after the fact is not sharing during the fact. A PRD you write once the conversation is over can help the next session. It cannot replace the conversation. Reset the agent and the concept dies. The markdown is a note for a deaf intern, not the intern's brain.

Bill Curtis, Herb Krasner, and Neil Iscoe interviewed people on 17 large projects for CACM in 1988. The problem they heard most was the thin spread of application domain knowledge. One or two people could hold the product in their head. The rest of the staff held a slice.

That person is scarce. I have been spending them on questions the repo can answer. "Do we already have auth?" is a lookup. "Should login be a magic link?" is a commit. If the agent asks me for the lookup, it is lazy. If it commits the magic link because I went quiet, it stole a decision.

---

## A stop I can run

I walk the unsigned branches before I type go.

Facts first, off my plate. The agent reads the repo. I do not narrate the filesystem.

Decisions in dependency order. One unsigned branch at a time if the branches hang off each other. Independent branches can come as a batch, each with a recommended answer I can refuse. The recommendation is an affordance. Rubber-stamping it reprints plan mode with extra ceremony.

Stop when a fresh session, given only a short note, could continue without asking. If the note is not enough, we are not done. If we are still picking button copy on a two-hour bug, we overshot. Clark's phrase was "sufficient for current purposes." A new product surface and a typo fix do not share a purpose, so they do not share a stop.

I have been using that deaf-session test as a check on myself. Paste the note into an empty chat. If the model has to ask a product question, I skipped a signature. If it only asks where the files live, I skipped a lookup I should have put in the note. If it can start, we start.

The code I got from "add search" was a map of my silences. Next time I will sign the branches, or the model will.
