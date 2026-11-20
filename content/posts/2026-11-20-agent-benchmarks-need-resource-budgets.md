---
title: "An agent benchmark needs a resource budget"
description: "Anthropic moved a coding benchmark by six points without changing models. Here is how to tell a better agent from a better test environment."
date: 2026-11-20T20:00:00+05:30
tags: [AI Agents, Evaluation, Reliability]
categories: [Engineering]
cover:
  image: "/images/uploads/agent-resource-budget.webp"
  alt: "Three rectangular execution environments with increasing amounts of headroom."
---

A six-point lead on a coding benchmark would get my attention. So would learning that the same agent gained six points when its test environment stopped killing processes at a strict resource limit.

Anthropic reported that gap between its tightest and uncapped Terminal-Bench 2.0 configurations. The model comparison people want to make is harder than it looks. The agent is writing files, running tests and pulling dependencies inside a real environment. A change to the worker can change the work it manages to finish. [Anthropic's infrastructure experiment](https://www.anthropic.com/research/infrastructure-noise) · [Terminal-Bench 2.0 release](https://www.tbench.ai/news/announcement-2-0)

## The container has a vote

Under Anthropic's strict per-task ceilings, 5.8% of runs hit infrastructure errors. Giving tasks three times the recommended resources as a ceiling brought that figure to 2.1%. With the caps removed it fell to 0.5%. The change from strict to three times headroom reduced infrastructure errors by 3.7 percentage points. Anthropic did not see a statistically significant difference in task success over that range in its experiment. [Anthropic's resource sweep](https://www.anthropic.com/research/infrastructure-noise)

{{< figure class="series-figure" src="/downloads/software-reliability/benchmark-headroom.webp" link="/downloads/software-reliability/benchmark-headroom.webp" alt="Anthropic reported infrastructure errors on 5.8% of runs at a strict ceiling, 2.1% at three times headroom, and 0.5% with no cap." caption="Infrastructure error rate across three configurations in Anthropic's Terminal-Bench 2.0 experiment." width="1200" height="675" >}}

The next step is the interesting one. From three times headroom to uncapped, infrastructure errors fell by another 1.6 points, while task success rose by almost four points. The extra room also let agents pursue approaches that took more resources. You cannot subtract the infrastructure error rate from the success rate to convert one score into another. Some crashed runs would have failed anyway. Some agents change what they can accomplish when the room gets bigger. [Anthropic's breakdown of the uncapped runs](https://www.anthropic.com/research/infrastructure-noise)

## Decide what the score is for

For a model selection decision, I'd rerun both candidates on the same tasks and harness revision, with the same tools, time and resource policy. Keep the result for each task and trial, including whether its counterpart solved the same job. A two-point aggregate lead tells me very little if the supposed winner is just passing the tasks its competitor kept timing out on. The failure logs tell me where to rerun, including in cases where the timeout is part of the product constraint.

For a deployment decision, I'd run a second comparison under the actual production resource envelope. The question then is which complete system solves more jobs within the budget I can give it. A model that wins in a roomy container can be a poor fit for a service with a tight deadline. I'd show solved jobs out of all attempts, alongside a breakdown of infrastructure errors, exhausted budgets and graded failures. Hiding failed starts behind an exclusion rule can hide the cost the operator will pay.

The harness and task version belong in the same row as the score. So do the guaranteed resources, hard ceilings, wall-clock limit and what happened to failed trials. Record the model revision and concurrency too. If these differ, a comparison can still tell you which complete setup worked better under its own conditions. It takes another run to make a claim about the model.

Anthropic's six-point number came from one experiment on Terminal-Bench 2.0. I'd use it to justify a resource sensitivity check, then measure the size of the effect on the tasks I actually care about.

[Download the figure script and its source values](/downloads/software-reliability/experiment.py).
