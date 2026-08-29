---
title: "The Staff+ Operating Model: a recursive mining of the technical leadership canon"
description: "I went deep on Will Larson, Tanya Reilly, Camille Fournier, Charity Majors and the fifteen authors they recommend, then distilled the invariant operating model for Senior SWE → Tech Lead → Staff/Principal. Here is the shared framework, the concrete playbooks, and the honest watch-outs — with the exact reading order if you want the whole set."
date: 2026-08-30T01:07:00+05:30
tags:
  - Engineering
  - Leadership
  - Career
  - TechLead
categories:
  - Engineering
cover:
  hidden: false
  relative: false
  image: "/images/uploads/staff-plus-leadership-banner.jpeg"
  alt: "The Staff+ operating model — the shared framework across the technical leadership canon"
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
---

Most writing about the technical leadership path is noise shaped like signal: clickbait ladders, ten-point checklists, motivational platitudes sold as frameworks. I wanted the real thing, so I did the opposite of reading one book. I mined the corpus recursively.

I started with the canonical four, **Will Larson, Tanya Reilly, Camille Fournier, and Charity Majors**, then followed every thread they actually point to: Larson's StaffEng resource map, Reilly's chapter-by-chapter reading list, and the authors those sources recommend in turn (Silvia Botros, John Allspaw, Julia Evans, Joy Ebertz, Keavy McMinn, and more). The point was not to hoard leadership trivia. It was to extract the **invariant operating model**: the handful of principles that keep showing up, under different names, across every serious practitioner.

This post is the synthesis. It answers one question: **what actually changes when you move from Senior SWE to Tech Lead to Staff/Principal, and what do you do differently on Monday?**

---

## What this source set is (and what it isn't)

Before the frameworks, a clear-eyed map. All four tier-one authors are practitioners, not career coaches: Larson (Stripe, Uber, senior infra leadership), Reilly (Google, Squarespace, author of *The Staff Engineer's Path*), Fournier (formerly CTO at Rent the Runway, author of *The Manager's Path*), Majors (co-founder and CTO of Honeycomb). They have run real organizations and owned real systems under fire.

Two honest caveats almost nobody mentions.

First, **these are organizational-design tools, not relationship coaches.** Larson himself is roughly 60/40 systems-thinker versus people-coach. His value is "given an org of this shape, here's what breaks." The interpersonal layer, the hard conversations and motivation, is thinner. Get that elsewhere.

Second, **not every org needs every staff archetype.** Reilly's sharpest point: staff roles "come in a lot of shapes, but not all orgs will need all kinds of staff engineers." Role-fit beats brute-force title-chasing. And she frames Senior as a *tenure* level. You don't have to go further to be successful.

---

## The core reframe: leadership without authority

Every author converges on the same uncomfortable premise: **past Senior, your code is not your edge. Your influence over people who do not report to you is.**

Silvia Botros, on becoming a Principal Engineer, put the bluntest version of it: *"Once at a certain level, all problems are solved by people. There is no such thing as 'purely technical problems'... influencing people to do what we want is harder still."* Fournier's *An Incomplete List of Skills Senior Engineers Need, Beyond Coding* leads with: *"How to run a meeting, and no, being the person who talks the most in the meeting is not the same thing as running it."*

This is the shift that breaks most people. John Allspaw's "On Being a Senior Engineer" names the actual bar for maturity: **"the degree to which other people want to work with you is a direct indication on how successful you'll be."** Across all fifteen authors, none defines the role by raw technical output. They define it by the *shape of the team that forms around you.*

---

## The four archetypes (Larson)

Larson's signature contribution was replacing the vague "staff engineer" with four recognizable archetypes. This is not a personality test. It is a way to know which kind of high-impact IC work energizes you, and which one your org actually needs.

1. **Tech Lead** steers complex projects, aligns the team with cross-functional goals, owns technical vision for a single project.
2. **Architect** owns the technical integrity of a domain over time, aligning architecture with business outcomes.
3. **Solver** is the person pulled in when the hardest problem will not die. They grind it to resolution and hand it to a team to maintain.
4. **Right Hand** is the strategic advisor to senior leadership, working problems at the intersection of technology, business, and organization.

Practice: identify which archetype matches *your* current work, then get honest about whether it is the one your org values. Being a Solver in an org that rewards Architects is a silent career killer.

---

## Reilly's three pillars

Where Larson gives you archetypes, who you are, Reilly gives you pillars, what you actually do. *The Staff Engineer's Path* is built on three.

**Big-picture thinking.** Understand the context across teams so good decisions happen before they become costly. "Good decisions need context" is the entire philosophy. This is where Tanya's famous **"be the glue"** lives: teams left alone settle into local maxima, solving only their own problem. The glue person holds the cross-team context and stops the org from optimizing the wrong thing.

**Project execution.** Take on the ambiguous, messy, cross-org projects everyone else avoids, and do "just enough work on them to make them manageable by someone else." Her brutal reframe: **"the agreement is the work."** Ideas are cheap. Getting humans to agree on what to do, then *deciding*, is the actual job.

**Leveling up others.** Be a force multiplier. "Scale yourself by writing and growing others."

Her single most useful decision tactic, borrowed from the IETF: **seek consent, not consensus.** Do not ask "Is everyone OK with choice A?" Ask *"Can anyone not live with choice A?"* Rough consensus, "lack of disagreement is more important than agreement," lets a decision move in a day instead of a quarter.

---

## Fournier's list: the actual job description

Camille Fournier's single post is worth more than most books. *An incomplete list of skills senior engineers need, beyond coding* is the closest thing the field has to a real job description for this transition. The twenty-three items cluster into four things you must become good at:

- **Communication and coordination.** Run a meeting, write a design doc and *drive it to resolution*, communicate status to stakeholders, explain things to senior people too embarrassed to admit they don't understand.
- **Influence without authority.** Get another team to adopt your solution instead of writing their own. Get another engineer to help you in a way that makes them feel appreciated. Get your ideas heard without making people feel threatened.
- **Listening and self-management.** Listen to others' ideas without feeling threatened. Take negative feedback gracefully. Give up your "baby" project.
- **Teaching and sponsorship.** Help someone get promoted. Teach another engineer to care about the thing you care about.

Her definition of the tech lead role is worth etching in stone. It is *"not a point on the ladder, but a set of responsibilities,"* and the core responsibility is *"the willingness to step away from the code and figure out how to balance your technical commitments with the work the whole team needs."*

---

## The center of gravity: Larson's "Operating at Staff"

The densest practical material in the whole set is the StaffEng "Operating at Staff" sequence. This is the playbook you actually execute. Synthesized and tightened.

**Work on what matters.** Larson's list of traps is the best prioritization framework in the field.

*Snacking* is easy, low-impact work that feels productive. Gloriously rewarded by everyone except reality. *Preening* is low-impact, **high-visibility** work. The seductive one, because many orgs conflate visibility with impact. Doing it well requires near-invulnerability to criticism, and it rots your real work. *Chasing ghosts* means investing in large projects because they echo your *previous* company's problems, not your current one's.

Instead, work where there is **both room and attention**: priorities that will matter but aren't yet swamped. Swarm existential problems when they are existential, but don't pile onto everyone's top priority. And the highest-value, most-neglected place to spend time is **growing the team around you**. Mentoring and coaching beat hiring for engineering velocity, and Larson says it will outlive your tech specs and PRs as your legacy.

Two more from the sequence are genuinely underrated.

**"Editing."** Most projects are one small change, one quick conversation, one unblock away from succeeding. With your relationships and context, you can shift outcomes with ounces of effort. And finishing things, turning a project from risk to asset, is always time well spent.

**"What only you can."** The work that simply won't happen if you don't do it is your single biggest opportunity. Expect this category to get narrower and deeper as you advance.

**Create space for others.** Larson's most counterintuitive and most correct idea: the best measure of your long-term success is that the org **benefits from but doesn't rely on** you. "A good discussion is, in this new world, one that it turns out you didn't need to attend." Techniques: shift toward asking questions instead of giving answers, pull in exactly one non-participant at a time, volunteer to take notes (it is a leadership act, not a demotion, and it frees a real notetaker to contribute), circulate decisions early *before* they crystallize, separate style feedback from substance feedback (stop giving style notes that won't change outcomes), and the big one, **change your mind**. If senior leaders never change their minds, everyone learns to correlate bluster with success.

**Sponsorship over mentorship.** Allspaw's maturity test and Larson's operating model converge here. Mentorship gives advice; sponsorship gives **opportunity and visibility**. When critical work comes to you, your first question must become *"who could be both successful with and grown by this work?"* Then scaffold it for their success and let it be theirs, including letting them take an approach you wouldn't. Rule of thumb: keep a sponsorship journal and sponsor someone at least a few times a month, but also make sure you still do *some* direct technical work yourself.

**Stay aligned with authority.** This is the one most ambitious ICs resist, and it is the one that decides whether they get the title at all. Your organizational authority flows from alignment with your direct manager, who is your *bestowing sponsor*. "To lead, you have to follow." People who make Staff don't fight their manager's initiatives. They make their own work *advance* the manager's goals, so the manager becomes a willing advocate.

---

## The honest arithmetic: getting the title

All the operating brilliance is worthless if it never converts to the title, because, fairly or not, your org's ceiling is the constraint. StaffEng's promotion material is refreshingly explicit.

**Promotion is a team activity, not a solo one.** "Don't play team games alone, you'll lose." Write the promotion packet *collaboratively* with your manager, bring them into the fold *early*, and temper your expectations.

**Find and activate a sponsor.** The most important person is your direct manager. If they've never promoted anyone to Staff, build credibility with a skip-level too. Ask questions that are easy to answer usefully. "If I don't get promoted this cycle, what are the likely causes?" beats "What should I do to improve?" Avoid ones that "prompt your sponsor to make up an answer."

**Visibility is a job.** "Get in the room, and stay there." Being visible across the org is a prerequisite, not a vanity exercise.

**Staff projects.** Whether or not your company formally requires one, they are "the sort of work that will stretch and develop you into a better engineer," and having done one gives you dispositive evidence of staff-level impact.

The uncomfortable truth underneath all of this, from the "staff projects" guide: even the most capable people often have *done the work* but not converted it into **recognized** impact. That gap is precisely what a sponsor closes.

---

## Charity Majors: the judgment check

Charity is your reality check, not your curriculum. Her material exists to develop judgment about the whole thing, especially what to say no to.

**The Engineer/Manager Pendulum.** The best technical leaders *oscillate* between deep engineering and management over a career, rather than picking a ladder and climbing it forever. The two demand opposite things. Great engineering needs long, uninterrupted focus. Good management needs to be available and interruptible. You can't do both deeply at once. "You have to choose one at a time." Her reframe is freeing: leadership does not equal management, and a stint in management arms you with skills, connecting business problems to technical outcomes, understanding what motivates people, having hard conversations, that make you a *better* staff IC, especially at *influence without authority*.

**Things to know about engineering levels.** Her warning against the default narratives, that management is a one-way trip, always a promotion, and the best engineers make the best managers, is the antidote to the "ladder must be climbed" instinct. Her career-sustainability advice is the most-cited line in the set, via Reilly: *"If you want a sustainable career in tech, you are going to need to keep learning your whole life... spend your time mostly in alignment with what makes you happy."*

**The distinction that matters most.** A manager's first responsibility is the humans. A tech lead's first responsibility is landing the project. Confusing these two is why promoting your best engineer to manager so often fails. Technical leadership is not a consolation prize. It is just as important as management.

---

## The glue warning (underrated and important)

Tanya Reilly's **"Being Glue"** deserves its own slot. It is the one piece of this set that can save your career from the trap the rest of it describes.

The trap: you do a ton of invaluable, non-promotable work. Onboarding, docs, unblocking others, spotting the dropped ball, standards, cross-team alignment. It makes the team wildly better and gets you glowing reviews. Then it **fails to get you promoted**, because "you didn't really have a technical contribution." If you are the glue before you are senior, it can be career-limiting. Women are asked to do 44% more of this thankless work and volunteer for 48% more of it. It is not merit-based. It is bias-shaped.

Her four-step defense, if you find yourself stuck in glue without a promotion:

1. Have the direct career conversation: *"Will I get promoted? What work gets me promoted?"* Get the manager's honest read.
2. Get a title that grants tech credibility, tech lead or similar, so you can do glue *as* a leader instead of as a scapegoat.
3. Create **artifacts** that tell the impact story: "due to my work and technical judgment, this thing happened." Make the manager tell the same story.
4. If it still doesn't convert, **temporarily stop doing glue work.** Declare a lot of things not your problem. Write code. Do unarguably-technical work. Let things drop. Getting promoted is itself the most powerful form of representation you can offer.

The deeper point applies to everyone: *if you only do glue, you will only get better at glue.* You're making the team more effective while quietly hurting your future self. Keep investing in the deep technical skill your title is supposed to certify.

---

## The recursive mining strategy (your actual reading list)

The whole point of this exercise is that the material compounds. Here is the exact order I'd ingest it in, and why.

**30 hours, done deliberately (the 80/20):**

- **Will Larson.** Start with the StaffEng *guides* (Operating at Staff → Work on what matters → Create space for others → Find your sponsor → Staff projects), then 5 to 7 of the *staff stories*. Michelle Bu, Ritu Vincent, and Katie Sylor-Miller are the ones that kept surfacing. His books *Staff Engineer* and *An Elegant Puzzle* consolidate the same material. (~10h)
- **Tanya Reilly.** *The Staff Engineer's Path*, parts I through III (big picture → execution → influence), plus *Being Glue*. (~8h)
- **Camille Fournier.** *The Manager's Path*, especially Ch. 3 (Tech Lead) and the *Incomplete List* essay. (~6h)
- **Charity Majors.** The Engineer/Manager Pendulum plus Things to Know About Engineering Levels. (~3h)
- **Slices of Julia Evans** ("What's a senior engineer's job?") and **Joy Ebertz** (Senior Staff day-to-day) for the *work*, not the *traits*. (~3h)

**Why this order.** Larson gives you the shared vocabulary (archetypes, operating-at-staff). Reilly gives you the day-to-day mechanics. Fournier grounds it in the manager's perspective you'll be negotiating against. Majors gives you the judgment to know when to stop. The tier-two authors (Botros, Allspaw, McMinn, Ebertz, Evans) are best mined *after* you have the core vocabulary, as case studies and future-state models, not as primary curriculum.

The recursive trick, for anyone who wants to go deeper: **don't read people, mine the network around the people.** Every time you read someone, chase the sources *they* cite. Larson's StaffEng learning-materials page and Reilly's chapter-by-chapter resource list are both literal maps of the field. That is how a five-book syllabus becomes a compounding, self-recommending set, and how you eventually see the same invariant operating principles wearing different names across fifteen authors.

---

## The invariant model, in ten lines

Everything above, compressed to the operating core.

1. **Your code stops being your edge; your influence over people who don't report to you becomes it.**
2. **Leadership ≠ management, and technical leadership is just as valid.** (Majors)
3. **Know your archetype** (Tech Lead, Architect, Solver, Right Hand) and whether your org values it. (Larson)
4. **Own the big picture** so good decisions happen before they get expensive. (Reilly)
5. **The agreement is the work.** Seek consent, not consensus. (Reilly)
6. **Refuse snacking and preening;** work where there's room and attention; finish things. (Larson)
7. **Create space for others** and change your mind when you should. (Larson)
8. **Sponsor, don't merely mentor:** give opportunity and visibility, not advice. (Allspaw, Larson, Hogan)
9. **Stay aligned with authority** and make the title a team effort with your sponsor-manager. (Larson)
10. **Guard against the glue trap:** keep investing in the deep skill your title certifies. (Reilly)

Prove it to yourself, not to a reviewer. Pick one item, *create space for others* is a good first, and run it at your actual job for two weeks. Watch your meetings shrink and your org's dependence on you shift from "the go-to person" to "the person who grew the team." That, more than any title, is the model working.

---

*If you found this useful, the deeper dive is worth it. Start at [staffeng.com](https://staffeng.com) (Larson) and [noidea.dog/staff-resources](https://www.noidea.dog/staff) (Reilly's curated map). Those are the two hubs the entire set hangs from.*
