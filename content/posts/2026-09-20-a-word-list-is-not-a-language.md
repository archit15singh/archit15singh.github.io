---
title: "A word list is not a language"
description: "I gave the agent a glossary harvested from the repo. The next plan got longer. It had learned every homonym and kept them all in play."
date: 2026-09-20T02:44:00+05:30
tags:
  - AI
  - Agents
  - Engineering
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/word-list-not-language-banner.jpg"
  alt: "Three open ledgers on a wooden table, each drawing a different meaning of the same idea"
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

I dropped `GLOSSARY.md` into the repo. Two columns: term, meaning. I told the agent to use it.

The next plan was longer. "User (the Customer in billing, also called Account when we mean the login)…" It had found every synonym in the tree and decided to keep them all in play. I had asked for a shared language. I had handed it a pile of collisions.

I wrote the other half of this as [silence as a spec](/posts/2026-09-20-ungrounded-codesign/). That post was unsigned decisions. This one is unbound names. You can share a picture of the work and still talk past each other if "search" means filter in your head and rank in the model's.

---

## The tax

Eric Evans called the fix ubiquitous language: a language structured around the domain model, used by the whole team *within a bounded context*, including in the code. The 2015 [DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) is blunt about it. The model is the backbone. The context is the edge. Day-to-day talk that is disconnected from the names in the code is the failure mode.

A scan of the repo does not give you that. It gives you strings the compiler already has. `User`, `Customer`, `Account`, `search`, `index`. No invariant. No edge. Evans's knowledge crunching is the opposite job: pick which string is live here, and what it is allowed to do. Harvest without crunch is how the file gets fat.

The extra words are a paraphrase tax. The model does not have a live name, so it defines, hedges, and lists synonyms. Soham Poddar and colleagues annotated 500 responses from 12 models on five datasets (2025). The minimal answer was 42% of the length. The rest was extra information (21%), irrelevance (18%), explanations (11.5%). Some of that is reward-model taste for length. Sainbayar Sukhbaatar, Jason Weston, and Jing Xu's length-instructed AlpacaEval run had GPT-4 Turbo violating the length constraint 46 to 49% of the time. A glossary will not fix that leak. It also will not excuse the other leak: hedge-lists of homonyms I taught it.

---

## One file, no edge

Evans put the language *inside a bounded context* because the same English word is two models. Account in billing is money. Account in auth is a login. Merge the glossaries and you have told the model both are in play. The plan that follows will narrate the merge. That looks thorough. It is unbounded language.

Peter Galison's trading zones are the same fact from the other side. Two groups can exchange without sharing global meaning. They start with a jargon, thicken it into a pidgin, sometimes grow a creole rich enough to live in. A dump of every identifier in the monorepo is a jargon dump. The creole is the type you can grow code in.

Susan Leigh Star and James Griesemer called the useful object a boundary object: plastic enough for each side, robust enough to keep identity across them. Repositories, forms, coincident boundaries. A union of all terms is a repository with no coincident boundary. It does not keep identity. It lists identities.

I have been treating `GLOSSARY.md` as if it were the language. It is a cache. Reset the session and the cache is gone unless the names live in code. The compiler is the only partner who rejects a wrong term. If `Customer` is not a type in this context, the glossary should not mention it.

---

## What I do with the file now

Split it. One list per bounded context, sitting next to the module that owns the types. Each row names a type or an invariant, not a synonym. "Account, in billing: `LedgerAccount`. Login lives in auth as `User`." The map between contexts is a second, short file. It is allowed to say "these two strings collide on purpose."

If a plan introduces a name that is not in that context's list, I stop and bind it or kill it. I do not let the agent keep both spellings "for clarity." Clarity was the tax.

I still cap length when I need to. The 49% number is real. I do not ask the glossary to do RLHF's job, and I do not ask `max_tokens` to pick `User` over `Customer`.

The louder plan was a map of names I had refused to pin. Next time the file will be smaller, and it will have an edge.
