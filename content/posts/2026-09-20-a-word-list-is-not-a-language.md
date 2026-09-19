---
title: "A word list is not a language"
description: "I gave the agent a glossary harvested from the repo, and the next plan got longer. A list of every name the compiler has is a pile of collisions, not a shared language."
date: 2026-09-20T02:44:00+05:30
tags: [AI, Agents, Engineering]
categories: [AI]
cover:
  image: "/images/uploads/word-list-not-language-banner.webp"
  alt: "Two bounded-context boxes naming the same string with different meanings"
  hidden: false
---

I dropped `GLOSSARY.md` into the repo. Two columns: term, meaning, harvested from the tree. I told the agent to use it.

The next plan was longer. "User (the Customer in billing, also called Account when we mean the login)…" It had found every synonym in the tree and decided to keep them all in play. I asked for a shared language and handed it a pile of collisions.

This post is the names half of a pair I keep writing. The other half is about [silence filling a spec](/posts/2026-09-20-ungrounded-codesign/). Here the default was a scan: grep the monorepo, list the identifiers, call it a language. You can share a picture of the work and still talk past each other when "search" means filter in your head and rank in the model's.

## A scan is not a bounded context

Eric Evans called the fix a ubiquitous language: a language structured around the domain model, used by the whole team within a bounded context, including in the code. The bounded context part is not decoration. In the DDD reference the model is the backbone and the context is the edge, and day-to-day talk that has come loose from the names in the code is the failure mode.

A scan of the repo does not give you that. It gives you the strings the compiler already has: `User`, `Customer`, `Account`, `search`, `index`. No invariant, no edge. Account in billing is money; Account in auth is a login. Merge the glossaries and you have told the model both are in play, so the next plan narrates the merge. It looks thorough. It is unbounded language.

I had also seen the cost before I could name it. The model does not have a live name, so it defines, hedges, and lists synonyms to make the plan readable, and the plan grows. A 2025 analysis of 500 responses from twelve models found the minimal answer was 42% of the output length; the rest was extra information, irrelevance, and explanation. Some of that is reward-model taste for length, and a glossary will not fix that leak. It will also not excuse the leak I manufactured, which was teaching the model that every homonym belongs in play at once.

## The compiler is the partner

Treating the glossary as the language missed the one member of the team who rejects a wrong term: the compiler. The file I had stood in for the language is actually a cache. Reset the session and the cache is gone, unless the names live in code next to the module that owns them. If `Customer` is not a type in this context, the glossary should not mention it in this context.

## What I do with the file now

Split it. One list per bounded context, sitting next to the module that owns the types. Each row names a type or an invariant, not a synonym: "Account, in billing: `LedgerAccount`. Login lives in auth as `User`." The map between the two contexts is a second, short file, and it is allowed to say these two strings collide on purpose.

When a plan introduces a name that is not in that context's list, I stop and bind it or kill it. I do not let the agent keep both spellings "for clarity". Clarity was the tax.

I still cap the plan length when I need to; the 42% finding is real. But the fix is not a bigger glossary. The louder plan was a map of names I had refused to pin. Next time the file will be smaller, and it will have an edge.