---
title: "There is no inside"
description: "I asked the agent for a filter and got fourteen files. Every one was an interface to two others. Gray box needs a box."
date: 2026-09-20T02:55:00+05:30
tags: [AI, Agents, Engineering]
categories: [AI]
cover:
  image: "/images/uploads/there-is-no-inside-banner.webp"
  alt: "Fourteen unboxed files on the left, one wrapped module with a top edge on the right"
  hidden: false
---

I asked the agent for a filter on the lesson list. It laid down fourteen files: a port, an adapter, a dto, a mapper, a validator, a hook, a util, two types files, a test for each. I tried the trick I use when I am tired: skip the insides and trust the names.

There were no insides. Every file was an interface to two others. Skipping them was skipping the program.

This is the third in a set I keep writing. [Unsigned decisions](/posts/2026-09-20-ungrounded-codesign/) is silence counted as a spec, and [unbound names](/posts/2026-09-20-a-word-list-is-not-a-language/) is a glossary with no edge. This one is a graph with no box. You can pin the words and still drown, because the layout has no place to stand.

## Shallow graphs are an interface tax

John Ousterhout draws a module as a rectangle. The top edge is everything a caller has to know, the area is what the module does, and depth is benefit over cost. UNIX file I/O is the shape he keeps liking: five calls, tens of thousands of lines behind them. A shallow module is the other shape: the interface is nearly as big as the work. A linked-list wrapper. A file whose only job is re-exporting a type. He has a name for the habit that produces shallow modules: classitis. Make everything small, wind up with a lot of them, and the system becomes a tax of top edges.

David Parnas picked the cut in 1972, and it was not along the flowchart. Hide the decisions that will change, he said, and do not slice a program one module per step. Flowchart decomposition is exactly what the agent did to my filter. Input, map, validate, hook, render: modularization at token speed. Tiny "clean" files are what the training set rewards.

Tests get hard for the same reason. A boundary test needs a boundary. On a mesh you mock neighbors, and the mocks become another interface layer. I have written those tests. They fail when someone renames a dto field. They do not tell me whether the filter works.

## The budget is four

My working set is about four chunks. Nelson Cowan's estimate of the focus of attention, once rehearsal and recoding are blocked, is roughly three to five in young adults (2001, reviewed 2010). I cannot hold fourteen interfaces, and I cannot hold the call graph that ties them. Shipping faster than my brain will hold is that overflow, not a character flaw.

Gray box was supposed to be the relief: design the edge, leave the inside. On a shallow graph the relief has nowhere to sit. There is no inside to leave.

The model has a related limit. Long-context utilization is U-shaped, the start and end of a prompt work while the middle drops, and a model starts every fresh session with no carryover, so dumping the blob graph into a long prompt is not more working memory. It is the same trap as [the glossary](/posts/2026-09-20-a-word-list-is-not-a-language/): a list of names is a cache, not storage, unless the shape lives somewhere a compiler can check.

## Wrap, then close

I wrap related blobs until a top edge exists. One module named `LessonFilter`, one function the rest of the app calls, tests against that call. Only then am I allowed to gray-box the mapper. Not before.

Gray box is an allocation of the four chunks, not a vow of ignorance. A settings panel can close. Finance stays open. Kent Beck's line about investing in the design every day, for this, means keeping depth: the investment is the box, not re-reading fourteen util files.

The fourteen files were a map of a filter I had refused to put in a box. Next time the wrap comes first. Then I can skip an inside that exists.