---
title: "What limits an AI cluster from delivery to peak load"
description: "Model first billable capacity, moving bottlenecks and how a power cap changes inference queues."
date: 2026-11-20T09:13:00+05:30
tags: ["AI Infrastructure", "data centers", "systems engineering"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-engineering.svg"
  alt: "Dependencies that bring a GPU cluster into service."
  hidden: false
format: "Technical note"
aliases:
  - "/posts/2026-11-20-next-ai-infrastructure-bottleneck/"
  - "/posts/2026-11-20-gpu-cluster-power-limit/"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

In a model of a new GPU cluster, paying to get the GPUs four months earlier buys exactly zero months of billable capacity. Paying to get grid power four months earlier buys one. Both outcomes follow from the same mistake in thinking about the project. The delivery date on a purchase order belongs to one branch of the schedule. The customer is waiting for the branches to join.

That distinction shows up in actual filings. At the end of September 2026, CoreWeave reported over 4.6 GW of contracted power and over 1.7 GW of active power. Its quarterly filing identifies a single leased site with 453 MW of electrical power still to be delivered in phases, according to the company's expectations. These figures describe different milestones in the development pipeline. A share of contracted power can be years away from service. [CoreWeave Q3 2026 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Third-Quarter-2026-Results/) · [CoreWeave Form 10-Q, Note 8](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm)

## Work backward from the first customer handoff

Start with one cluster at one site. The operator in this example bills from contractual acceptance. Commissioning means installing and validating the system under load. It needs accelerators, a network fabric, a building with working cooling, and power. At the end, the customer also has to be ready to integrate and accept the cluster.

| Branch | Predecessor | Ready in month |
|---|---|---:|
| Financing | Project start | 2 |
| Accelerator delivery | Financing | 12 |
| Network fabric delivery | Financing | 16 |
| Building and cooling | Financing, then permits | 19 |
| Energization | Grid connection and switchgear | 20 |
| Customer readiness | Financing | 18 |
| Commissioning | Energization, cooling, GPUs, and fabric | 23 |
| Contractual acceptance | Commissioning and customer readiness | 25 |

The numbers are inputs to an illustrative model. Each step starts when its last predecessor finishes. Commissioning takes three months and acceptance takes two. In the baseline, the grid work finishes in month 20, after switchgear in month 14. That puts the grid branch on the critical path, the chain of dependent work that determines the earliest finish date. Cooling has one month of slack. The network fabric has four.

This changes the procurement question. If the accelerators arrive in month 8 and billing still starts in month 25, the business now carries the equipment for four extra months. Whether early delivery is worth paying for depends on how much it insures against a later shortage, whether the supplier offers flexible delivery, and who pays for storage and financing.

## Which deadline moves the billing date?

| Change to the baseline | First billable month | Branch holding up commissioning |
|---|---:|---|
| None | 25 | Grid |
| Accelerators arrive four months earlier | 25 | Grid |
| Grid work finishes four months earlier | 24 | Building and cooling |
| Grid work and cooling finish four months earlier | 21 | Grid and fabric, tied |
| Fabric arrives five months later | 26 | Fabric |

The fourth row shows what the individual delivery dates leave out. Advancing the grid work alone leaves the crew waiting on cooling. Advancing both works until the fabric and the grid finish together in month 16. At that point, bringing the date forward again requires speeding up both branches.

Public statements rarely let you build this schedule for an actual site. Even the demand side of the connection queue calls for care. In its preliminary November 2026 update, ERCOT reported responses from 433 loads covering about 177 GW of **requested** interconnection capacity. It also noted that some projects were still deciding basic equipment configurations such as cooling. Those are requests at different levels of maturity. The useful operational question is how much capacity passed each readiness milestone. [ERCOT preliminary data center impact survey, November 5, 2026](https://www.ercot.com/files/docs/2026/11/05/Community-Impact-RFI-PUC-Update.pdf)

Try the [interactive critical-path simulator](/downloads/ai-infrastructure-reality-check/critical-path.html) to change the schedule in your browser. The [downloadable Python model](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) calculates finish dates and critical paths. Run `python3 physical-infrastructure-models.py deployment` for the cases above, or append `--task grid --months 14` to test a shorter grid task. The override is a task duration, measured from its predecessor's finish. Every scenario assumes fixed dependencies and durations. An actual budget decision needs a range for the uncertain finish dates, including correlated delays when several branches need the same vendor or construction crew.

## After commissioning, measure every constraint in one unit

Firm power is the first place I would look for a new campus with secured racks. At a site already serving customers, the test changes. Measure the throughput of the same workload against each candidate constraint. A service-level objective (SLO), such as a latency target, defines which completed requests count. [IEA on grids](https://www.iea.org/reports/electricity-2026/grids)

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

Use the [downloadable scenario model](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) with `python3 physical-infrastructure-models.py bottlenecks`. Replace the capacities with measured limits for your workload, then try the proposed upgrade. If a 50% increase in one resource produces a 5% gain in qualifying throughput, identify the resource with the next-lowest limit before buying more of the first.

## During a power cap, the queue can become the limit

Power caps change how a scheduler allocates the remaining capacity. The Zeus authors evaluated power caps and batch-size choices across several deep-learning training workloads and reported energy-efficiency gains ranging from 15.3% to 75.8% in their experiments. Google reported signing 1 GW of demand-response capacity across its U.S. data-center agreements in March 2026 and says it can shift a portion of its machine-learning work. Those measurements concern training efficiency and contracted flexibility. To set an inference policy, measure how power caps affect request latency on the serving workload. [Zeus, NSDI 2023](https://www.usenix.org/system/files/nsdi23-you.pdf) · [Google demand-response announcement](https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/demand-response-data-center-milestone/)

The Python model starts with 12 rack groups and a 10 MW facility envelope. A fixed 1.6 MW covers facility loads and common services. Each full-power group reserves 700 kW and completes ten requests per minute. In the first capped case a group reserves 450 kW and completes eight. The scheduler enumerates the feasible group allocations under a 7.2 MW envelope and can pick the one with the highest modeled service rate. Requests wait in a FIFO queue.

The same trace runs in each case. Every minute for 30 minutes, 75 arrivals join the queue, except for a 10-minute burst at 100 arrivals per minute. The model counts a request as on time if it finishes within two one-minute simulation slots of arrival, including service. At the end of the arrival window it continues until the queue drains. Power figures are reservation envelopes. The model sets envelopes and computes service outcomes.

| Policy | Reserved MW | Completed/min during arrivals | Service-slot utilization | p95 latency | On time | Peak backlog |
|---|---:|---:|---:|---:|---:|---:|
| 12 full-power groups | 10.0 | 83.3 | 69.4% | 1 min | 100% | 0 |
| 8 full-power groups | 7.2 | 78.3 | 97.9% | 4 min | 54.2% | 200 |
| 12 capped groups | 7.0 | 83.3 | 86.8% | 2 min | 100% | 40 |

With 7.2 MW available, concentrating power in eight groups leaves a peak queue of 200 requests. Spreading power across twelve groups cuts the queue to 40. The result depends on how well the workload responds to the cap. In this example a group at 450 kW keeps 80% of its capacity with about 64% of the reserved power. Suppose it keeps 60% instead. Twelve capped groups then have only 72 slots per minute. Their p95 is six minutes, and 41.0% finish on time. Eight full-power groups keep the four-minute p95 and 54.2% on-time share. The allocation search picks capped groups at the higher assumed rate and full-power groups at the lower one. The model's goal is maximum capacity for identical jobs. A live mixed fleet would need to choose among traffic classes and respect what can actually move.

Try the [downloadable scheduler](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) with `python3 physical-infrastructure-models.py power`, then add `--capped-rate 6` for the reversal. It models identical requests, constant capacity inside each time slot, and a fixed site overhead. For a real curtailment plan, replay a burst trace at each supported power setting and measure completed work, tail latency and the time the site needs to recover. A plan that meets the MW ceiling and leaves customers queued after the event still has a bill to pay.
