---
title: "Where will the next AI infrastructure bottleneck move?"
description: "Track how scarcity can move from accelerator supply to power, networking, and customer demand using the throughput of one workload."
date: 2026-11-20T09:08:00+05:30
tags: ["AI Infrastructure", "capacity planning", "systems engineering"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-engineering.svg"
  alt: "Dependencies that bring a GPU cluster into service."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

If I had to find the next bottleneck in an AI buildout, I would look for what sits idle. Accelerators in storage point to a site readiness problem. A running cluster with a saturated network points somewhere else. Spare capacity after customers have been onboarded puts the question to sales and product. All three situations can follow a successful hardware purchase.

There is evidence that several limits coexist. In March 2025, Micron said HBM3E requires roughly three times the silicon of DDR5 per bit. The IEA estimates electricity use at AI-focused data centers rose 50% in 2025. At the level of an inference service, the DistServe authors found that moving prefill and decode to separate GPU pools reduced interference in their tests, with placement decisions now depending on network bandwidth for the KV-cache transfer. Each observation has a different scope. Together they explain why improving supply in one layer can bring a different constraint into view. [Micron fiscal Q2 2025 prepared remarks, p. 5](https://investors.micron.com/static-files/52ce0c07-49dc-4eab-b1d2-a67bde373bca) · [IEA, *Key Questions on Energy and AI*](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) · [DistServe, OSDI 2024](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)

My first candidate for a new campus with secured racks is firm power at the site. The IEA documents grid-connection delays and supply constraints in transformers and gas turbines. For an already energized inference fleet, I would check the fabric and software before looking for more megawatts. The prediction is about projects with different starting conditions. Watch which shortages leave other equipment idle. [IEA, *Electricity 2026*](https://www.iea.org/reports/electricity-2026/grids) · [IEA, *Key Questions on Energy and AI*](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary)

## Put all the constraints in one unit

You cannot take the minimum of megawatts, gigabytes per second and purchase orders. Pick the workload you intend to sell and convert each resource to the same output unit. For a serving cluster that could mean completed requests per hour at a fixed prompt and output mix, with a specified service-level objective (SLO).

Take a site that can deliver 72,000 qualifying requests an hour with its current accelerators. The energized power budget could support 80,000 on the same stack if enough accelerators were available, cooling could support 100,000, and the network could support 90,000. Customers would currently use 92,000. Treat those numbers as independent limits for a fixed operating point.

| Cumulative change | Accelerator limit | Power | Cooling | Fabric | Demand | Served | Active limit |
|---|---:|---:|---:|---:|---:|---:|---|
| Baseline | 72 | 80 | 100 | 90 | 92 | 72 | Accelerators |
| More accelerators | 120 | 80 | 100 | 90 | 92 | 80 | Power |
| More firm power | 120 | 110 | 100 | 90 | 92 | 90 | Fabric |
| Fabric upgrade | 120 | 110 | 100 | 115 | 92 | 92 | Demand |
| Demand grows | 120 | 110 | 100 | 115 | 105 | 100 | Cooling |

All values are hypothetical thousands of requests per hour. Increasing accelerator capacity by 48,000 raises delivered capacity by 8,000. After the power and fabric upgrades, raising demand exposes the cooling limit. If demand falls to 70,000 instead, the same infrastructure ships 70,000. Cooling and demand are both real limits in the model. Which one bites depends on what users are trying to do that hour.

A production system needs measurements at the new operating point. Network traffic might grow faster than load if a larger deployment changes the parallelism scheme or adds cross-rack communication. Raising the power envelope can shift the cooling limit as temperatures rise. A model with independent caps is a quick planning check. For a purchase decision, measure the interactions.

## What would convince me a constraint had moved?

| Candidate limit | Measurement that would move the call |
|---|---|
| HBM and accelerator supply | Time from order to accepted hardware for the same system, alongside confirmed rack delivery volumes |
| Site power | Firm energized MW available to the deployment, plus evidence of sustained operation at that draw |
| Cooling | Temperature margin, flow and thermal throttling during the peak workload mix |
| Network | Transfer time and achieved bandwidth during the same jobs, paired with request latency or training step time |
| Customer demand | Qualifying completed workload and paid demand available at the target price, compared with commissioned capacity |

The first three measurements describe different owners and places in a supply chain. A manufacturer expanding HBM packaging in Singapore tells me about its expected ability to supply memory. It tells me little about the local network and electricity available at an operator's racks. In a January 2026 facility announcement, Micron pointed to a meaningful supply contribution from its separate HBM packaging project in calendar 2027. Calling the bottleneck solved would require evidence of the supply arriving in finished systems and feeding a constrained deployment. [Micron Singapore manufacturing and HBM packaging announcement](https://investors.micron.com/news/press-release/2026/Micron-Breaks-Ground-on-Advanced-Wafer-Fabrication-Facility-in-Singapore-01-26-2026/default.aspx)

Use the [downloadable scenario model](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) with `python3 physical-infrastructure-models.py bottlenecks`. Replace the capacities with measured limits for your workload, then try the proposed upgrade. If a 50% increase in one resource produces a 5% gain in qualifying throughput, identify the resource with the next-lowest limit before buying more of the first.
