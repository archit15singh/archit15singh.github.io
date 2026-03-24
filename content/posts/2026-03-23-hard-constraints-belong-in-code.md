---
title: "Hard Constraints Belong in Code: The Probabilistic-Deterministic Hybrid Agent Pattern"
description: "LLMs are probabilistic reasoners - great at exploring solution spaces using model priors, bad at guaranteeing correctness. Deterministic code is the opposite. The right architecture for high-stakes decisions wires them together: model priors for exploration, code for enforcement."
date: 2026-03-23T10:00:00+05:30
tags:
  - AI
  - Agents
categories:
  - AI
cover:
  hidden: false
  relative: false
  image: "/images/uploads/hard-constraints-belong-in-code-banner.jpeg"
  alt: "Control panel with dials and gauges - deterministic precision and probabilistic exploration in one system"
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

# Hard Constraints Belong in Code

LLMs are probabilistic reasoners. They draw on model priors to interpret ambiguous inputs, frame hypotheses, and synthesize trade-offs across a large solution space. That's exactly what makes them useful for complex decisions - and exactly what makes them unreliable for enforcing hard rules.

Deterministic code is the opposite. It has no priors, no judgment, no ability to explore. But it guarantees correctness on anything reducible to math or a lookup.

The right architecture for high-stakes decisions uses both. The LLM does what probabilistic reasoning is good at - exploring the space of possible responses using its priors about costs, risks, and trade-offs. Deterministic code does what it's good at - enforcing constraints, running calculations, and returning structured results the model can reason over. Neither alone is sufficient. The failure mode of pure LLM is subtle: the model sounds confident, the output looks reasonable, and then someone catches that the recommended supplier isn't certified for that part, or the suggested order quantity violates a contractual minimum. The failure mode of pure deterministic optimization is different: it answers the question you asked, not the question you needed to ask.

Getting the boundary between the two right is the core design decision.

---

## The Problem with Pure LLM Optimization

Take a concrete scenario: a policy event changes import tariffs on a particular trade lane. A supply chain team needs to know what to do - which parts to reroute, to which suppliers, over what timeline, at what cost.

A naive approach sends this to a model and asks for a recommendation. The model will give you one. It will sound authoritative. It will probably even be structurally reasonable. But it has no access to your actual supplier contracts, no way to check certification requirements against each part number, no mechanism to validate that the recommended order volumes are actually achievable given supplier capacity.

```
User: "25% tariff on China -> Korea lane. What should we do?"
LLM:  "Consider rerouting to Vietnam suppliers, or absorbing cost,
       or diversifying across multiple lanes..."

What the LLM cannot do:
  ✗ Calculate the actual annualized cost delta across 340 affected SKUs
  ✗ Check whether Vietnam suppliers are certified for each spec
  ✗ Verify contractual minimum order quantities at forecast volumes
  ✗ Guarantee the math is right under any scenario
  ✗ Produce an output with an audit trail
```

The model doesn't know what it doesn't know about your constraints. It will happily recommend something that looks optimal and is operationally impossible.

---

## The Problem with Pure Deterministic Optimization

The reflex fix is to throw this at an operations research model - minimize cost subject to constraints, return the optimal routing.

```
minimize:   Σ(cost[i] * volume[i])
subject to: lead_time[i] ≤ max_lead_time
            supplier_capacity[i] ≥ demand[i]
            certification_valid[i,j] = true
            moq[i,j] ≤ order_quantity[i,j]
```

This is correct and reproducible. It will also only answer the question you asked. The question you need answered is: *which scenarios are worth evaluating?* A 25% tariff shock doesn't have one obvious response - it has a space of possible responses, each with different risk profiles, transition timelines, and strategic implications. The optimization model needs a human to frame each scenario, encode each trade-off, and decide what the objective function should be.

That's the gap. The deterministic system can compute any scenario you give it with perfect accuracy. It cannot decide which scenarios to explore.

```
                WHAT CODE DOES WELL         WHAT LLMs DO WELL
                ---------------------       -----------------------
                Arithmetic                  Interpreting policy language
                Constraint enforcement      Framing scenario hypotheses
                Reproducible math           Exploring the parameter space
                Audit trails                Synthesizing trade-offs
                Checking feasibility        Explaining decisions
```

Neither alone solves the problem. The answer is to wire them together so each does what it's actually good at.

---

## The Architecture: LLM as Explorer, Code as Enforcer

The core design principle:

> **Hard constraints are enforced by code. The LLM explores the optimization parameter space via simulator access.**

The LLM is an agent that calls a deterministic simulator as a tool. The simulator enforces all hard constraints - certifications, MOQs, capacity limits, contractual minimums - and returns structured results. The LLM reasons over those results, adjusts its hypotheses, runs more simulations, and synthesizes a recommendation.

```
+-----------------------------------------------------------------+
|                    HYBRID AGENT SYSTEM                          |
|                                                                 |
|   +--------------+         +-------------------------------+   |
|   |              |         |      DETERMINISTIC            |   |
|   |  LLM AGENT   |-------->|        SIMULATOR              |   |
|   |              |<--------|                               |   |
|   |  Explores    |  tool   |  Enforces hard constraints    |   |
|   |  Reasons     |  calls  |  Runs cost calculations       |   |
|   |  Synthesizes |         |  Returns structured results   |   |
|   |  Explains    |         |  Reproducible math            |   |
|   |              |         |                               |   |
|   +--------------+         +-------------------------------+   |
|                                                                 |
|   LLM decides WHAT to simulate.                                 |
|   Code decides WHETHER it's feasible and WHAT it costs.        |
+-----------------------------------------------------------------+
```

---

## The Execution Loop

Walking through the tariff scenario with this architecture:

### Step 1: The LLM frames the scenario space

Before touching the simulator, the agent reasons about the response categories:

```
LLM internal reasoning:
  "25% tariff affects ~340 SKUs on the China -> Korea lane.
   Response strategies fall along two axes:
     cost delta vs. transition risk
     breadth of rerouting vs. selectivity

   I'll construct 5 scenarios spanning the trade-off space:
   1. Absorb full tariff - baseline
   2. Full reroute to Vietnam alternatives
   3. Selective reroute - highest-impact SKUs only
   4. Nearshore to Korea domestic for top volume SKUs
   5. Reroute + contract renegotiation hybrid"
```

The LLM isn't computing anything yet. It's deciding what's worth computing - which is exactly what it's good at.

### Step 2: Scenario runs with structured feedback

The agent calls the simulator five times. Each call returns not just costs but constraint status:

```
Scenario 1: Absorb full tariff
------------------------------
agent -> simulator({routing: current, tariff_applied: true})
<- {
    annual_cost_delta: +$47M,
    lead_time_delta: 0 days,
    constraint_violations: []
  }

Scenario 2: Full Vietnam reroute
---------------------------------
agent -> simulator({routing: vietnam_all, affected_skus: 340})
<- {
    annual_cost_delta: +$12M,
    lead_time_delta: +18 days,
    constraint_violations: [
      "SKU-4421: Vietnam supplier not certified for this spec",
      "SKU-8839: MOQ minimum unmet at forecast volume"
    ]
  }

Scenario 3: Selective reroute (>15% impact SKUs)
--------------------------------------------------
agent -> simulator({routing: vietnam_subset, affected_skus: 127})
<- {
    annual_cost_delta: +$21M,
    lead_time_delta: +4 days,
    constraint_violations: []    <- clean
  }
```

Scenario 2 comes back with violations. The LLM doesn't average over them or hope the violations are minor - it takes them as hard stops and adjusts the next hypothesis accordingly. This is the feedback loop that makes the system trustworthy.

### Step 3: Synthesis over validated results

After all five runs, the LLM synthesizes across scenarios where constraint violations are zero. It's comparing apples to apples - every option on the final shortlist has already been verified as operationally feasible:

```
LLM synthesis:
  Scenario 1: $47M annual exposure, zero routing flexibility - baseline
              for comparison only.
  Scenario 2: Eliminated - constraint violations on 2 SKUs, high
              supply risk with unproven suppliers.
  Scenario 3: Best balance. $21M delta, +4 days lead time, no
              violations. Recommend this.
  Scenario 4: Similar cost to Scenario 3, reduces Korea-domestic
              strategic optionality.
  Scenario 5: Dependent on contract renegotiation - timeline
              uncertain, not executable within Q1.
```

### The output

```
+------------------------------------------------------------+
|  RECOMMENDATION: Scenario 3 - Selective Reroute            |
|                                                            |
|  Reroute 127 SKUs (>15% tariff impact) to Vietnam          |
|  alternative suppliers over 60 days.                       |
|                                                            |
|  Annual cost delta:  +$21M  (vs. +$47M absorb baseline)   |
|  Lead time impact:   +4 days average                       |
|  Constraint status:  CLEAN - no violations                 |
|                                                            |
|  Why not Scenario 2: Certification gaps on 2 SKUs,        |
|  MOQ violation at forecast volume.                         |
|  Why not Scenario 5: Renegotiation timeline exceeds Q1.   |
+------------------------------------------------------------+
```

The output isn't just a number. It includes the reasoning, the rejected alternatives, and the assumptions - which means a supply chain director can actually review it rather than trust it blindly.

---

## The Constraint Feedback Loop

The detail that makes or breaks this architecture is what happens when the simulator returns violations.

A naive implementation ignores violations or logs them and continues. The right implementation treats them as information the LLM needs to update its hypothesis:

```
WITHOUT the feedback loop:

  LLM proposes Scenario 2 (full Vietnam reroute)
  Simulator returns violations
  Violations included in final comparison
  LLM picks Scenario 2 anyway because it's cheapest
  Recommendation is operationally impossible

WITH the feedback loop:

  LLM proposes Scenario 2
  Simulator returns violations
  LLM reads violations as constraints on the next hypothesis
  LLM designs Scenario 3 to explicitly avoid those violation conditions
  Scenario 3 comes back clean
  Final comparison only includes clean scenarios
  Recommendation is both optimal AND feasible
```

The loop is what allows the LLM to act like an experienced analyst who adjusts their recommendation when new data comes in, rather than a one-shot generator who ignores feedback.

---

## Production: From Interactive to Batch

The interactive version - five scenarios, real-time response - is a demo. The production version is different in scale but identical in structure:

```
INTERACTIVE (demo)          PRODUCTION (batch)
--------------------        ----------------------------------
5 scenarios                 Hundreds to thousands of simulations
Real-time output            Runs offline (nightly or on trigger)
Single policy event         Continuous monitoring for policy signals
One recommendation          Portfolio of documented recommendations
                            with confidence ranges and sensitivities
```

The production architecture adds a scheduler that detects policy changes above a materiality threshold, spawns analysis agents per affected trade lane, runs simulations in parallel, and stores the results in a structured recommendation store with full audit trails. The LLM's synthesis job shifts from "pick one recommendation" to "summarize the portfolio and flag the high-urgency items."

```
Policy signals --> Scheduler --> Simulation Farm --> Synthesis Agent --> Recommendation Store
                   (trigger)       (vectorized,         (LLM reads         (versioned, auditable,
                                   parallel runs)        batch output)       human-reviewable)
```

The key property that scales: the LLM never touches math. It reads structured outputs. So adding more simulation capacity doesn't require changing the LLM layer, and improving the LLM doesn't require revalidating the simulator.

---

## Where to Draw the Line

The architectural question that comes up in every variant of this problem is: what belongs in code, and what belongs in the model?

The rule I've found most reliable:

> **If the question has a correct answer derivable from data, it belongs in code. If the question requires judgment over structured results, it belongs in the LLM.**

```
IN CODE:                            IN THE LLM:
--------------------------------    ----------------------------------
Tariff rate arithmetic              "Which scenarios should I test?"
Supplier certification lookup       "What does this policy imply?"
Capacity constraint checking        "Which result is the best overall?"
MOQ enforcement                     "Why did this scenario fail?"
Cost aggregation across SKUs        "How should I explain this?"
Lead time calculation               "What am I missing in my analysis?"
```

The failure mode when you get this wrong in the LLM direction: the model does math, gets it slightly wrong, sounds confident, and someone trusts it. The failure mode when you get this wrong in the code direction: the optimizer runs on a poorly-framed scenario, returns an "optimal" answer to the wrong question, and nobody catches it until a supplier misses an order.

The hybrid exists precisely because both failure modes are real and neither is acceptable in production.

---

## The Broader Pattern

This architecture - LLM as explorer, deterministic system as enforcer, structured feedback loop between them - isn't specific to supply chain. It applies anywhere the problem has both:

1. A large space of possible actions that requires judgment to navigate
2. Hard constraints that must hold in the output regardless of what the model recommends

Loan underwriting, treatment protocol recommendation, infrastructure change management, legal contract review - any domain where a human expert would say "here are the options I'd consider" AND "here's what would absolutely disqualify each one" is a candidate for this pattern.

The insight that makes it work in practice: **the LLM doesn't need to know the constraints in detail. It needs to be wired to a system that enforces them and returns violations as data.** The model's job is to respond to that data intelligently - which is exactly what it's good at.

---

## Closing

The temptation with capable frontier models is to route everything through the model and treat the results as reliable. For exploration, synthesis, and explanation - that trust is usually warranted. For anything with a ground truth derivable from data, it isn't.

The architectural discipline of separating these two modes - and building the feedback loop that connects them - is what takes an AI system from "impressive demo" to something a production team can actually depend on.

Hard constraints belong in code. Not because models can't reason about them. Because production systems can't afford to find out when they got it slightly wrong.
