---
title: "There is no inside"
description: "I asked the agent for a filter and got fourteen files. I tried not to read them. Every file was an interface. Gray box needs a box."
date: 2026-09-20T02:55:00+05:30
tags:
  - AI
  - Agents
  - Engineering
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/there-is-no-inside-banner.jpg"
  alt: "A heap of tiny empty boxes beside one closed wooden chest with a single latch"
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

I asked for a filter on the lesson list. The agent laid down fourteen files: a port, an adapter, a dto, a mapper, a validator, a hook, a util, two types files, a test for each. I tried the trick I use when I am tired. Skip the insides. Trust the names.

There were no insides. Every file was an interface to two others. Skipping them was skipping the program.

This sits next to the last two posts. [Unsigned decisions](/posts/2026-09-20-ungrounded-codesign/) is silence counted as a spec. [Unbound names](/posts/2026-09-20-a-word-list-is-not-a-language/) is a glossary with no edge. This one is a graph with no box. You can share a picture and pin the words and still drown, because the layout has no place to stand.

---

## Cost is the top edge

John Ousterhout draws a module as a rectangle. The top edge is the interface: everything a caller has to know. The area is what the module does. Depth is benefit over cost. UNIX file I/O is the picture he likes: five calls, tens of thousands of lines behind them. A shallow module is the other shape. The interface is almost as big as the work. A linked-list wrapper. `addNullValueForAttribute`. A file whose only job is to re-export a type.

He has a name for the habit that produces the second shape: classitis. Conventional advice says make classes small. You get a lot of them. The interfaces accumulate. The system is a tax of top edges.

David Parnas already picked the cut in 1972. Do not slice a program on the flowchart, one module per step. Hide the decisions that will change. Flowchart decomposition is what the agent did to my filter. Input, map, validate, hook, render: modularization 1, at token speed. The model's prior is that grain. "Clean" tiny files are the training set.

Tests get hard for the same reason. A boundary test needs a boundary. On a mesh you mock neighbors, and the mocks are another interface layer. I have written those tests. They fail when someone renames a dto field. They do not tell me the filter works.

---

## The budget is four

Nelson Cowan put the number at about four chunks in the focus of attention, three to five in young adults, once you block rehearsal and recoding (2001, reviewed 2010). Miller's seven includes the tricks. An agent dump blocks the tricks. It does not recode fourteen files into one "filter." It hands you fourteen.

I cannot hold fourteen interfaces. I also cannot hold the call graph that ties them. Shipping faster than my brain is that overflow. It is not a character flaw. Gray box was supposed to be the relief: design the edge, leave the inside. On a shallow graph the relief has nowhere to sit. There is no inside to leave.

The model has a related limit. Nelson Liu and colleagues (TACL 2023) showed a U-shaped use of long context: beginning and end work, the middle drops. GPT-3.5-Turbo on multi-document QA can lose more than twenty points when the useful document sits in the middle, down below the closed-book baseline (56.1%). A 16K window did not fix utilization. Dumping the blob graph into a long prompt is not more working memory. The file you need is in the middle of the dump.

---

## Wrap, then close

I wrap related blobs until a top edge exists. One module named `LessonFilter`, one function the rest of the app calls, tests against that call. Then I am allowed to gray-box the mapper. Not before.

Finance stays open. A settings panel can close. Gray box is an allocation of the four chunks, not a vow of ignorance.

I keep a short map of those names. That map is the cache across sessions. Reset kills the conversation. It does not have to kill the boxes if the names live in the tree.

I still write small functions when they hide a decision. I do not write a file per step of a flowchart and call it design. Kent Beck's line about investing in the design every day, for this, means keeping depth. Re-reading fourteen util files is not the investment.

The fourteen files were a map of a filter I had refused to put in a box. Next time the wrap comes first. Then I can skip an inside that exists.
