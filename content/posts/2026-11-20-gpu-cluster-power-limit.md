---
title: "What happens when a GPU cluster hits a power limit?"
description: "Under the same site power cap, eight fast rack groups and twelve slower ones produce different queues. The better policy depends on the workload."
date: 2026-11-20T09:07:00+05:30
tags: ["AI Infrastructure", "GPU scheduling", "power"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-engineering.svg"
  alt: "Dependencies that bring a GPU cluster into service."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

A cluster with 98% service-slot utilization missed nearly half its deadlines in a toy power-curtailment experiment. Under the same site power ceiling, a cluster that kept more rack groups active at lower power got every request in on time. The result reverses when capping has a bigger effect on performance. Before choosing a policy, measure the curve.

There is real work behind the premise. The Zeus authors evaluated power caps and batch-size choices across several deep-learning training workloads and reported energy-efficiency gains ranging from 15.3% to 75.8% in their experiments. Google reported signing 1 GW of demand-response capacity across its U.S. data-center agreements in March 2026 and says it can shift a portion of its machine-learning work. The research measures specific training jobs. The Google figure describes contracted flexibility. Neither supplies a latency curve for an inference fleet. [Zeus, NSDI 2023](https://www.usenix.org/system/files/nsdi23-you.pdf) · [Google demand-response announcement](https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/demand-response-data-center-milestone/)

## Give the scheduler a power ceiling

The Python model starts with 12 rack groups and a 10 MW facility envelope. A fixed 1.6 MW covers facility loads and common services. Each full-power group reserves 700 kW and completes ten requests per minute. In the first capped case a group reserves 450 kW and completes eight. The scheduler enumerates the feasible group allocations under a 7.2 MW envelope and can pick the one with the highest modeled service rate. Requests wait in a FIFO queue.

The same trace runs in each case. Every minute for 30 minutes, 75 arrivals join the queue, except for a 10-minute burst at 100 arrivals per minute. The model counts a request as on time if it finishes within two one-minute simulation slots of arrival, including service. At the end of the arrival window it continues until the queue drains. Power figures are reservation envelopes. The model sets envelopes and computes service outcomes.

| Policy | Reserved MW | Completed/min during arrivals | Service-slot utilization | p95 latency | On time | Peak backlog |
|---|---:|---:|---:|---:|---:|---:|
| 12 full-power groups | 10.0 | 83.3 | 69.4% | 1 min | 100% | 0 |
| 8 full-power groups | 7.2 | 78.3 | 97.9% | 4 min | 54.2% | 200 |
| 12 capped groups | 7.0 | 83.3 | 86.8% | 2 min | 100% | 40 |

Eight groups serve 80 requests per minute. The burst sends 100, so 20 more requests wait at the end of each burst minute. The queue reaches 200. When arrivals return to 75, only five slots a minute go toward that backlog. There are still 150 requests waiting after the last arrival. Keeping more groups active gives the queue 96 slots a minute and makes the burst much easier to absorb.

In this example a group at 450 kW keeps 80% of its capacity with about 64% of the reserved power. Suppose it keeps 60% instead. Twelve capped groups then have only 72 slots per minute. Their p95 is six minutes, and 41.0% finish on time. Eight full-power groups keep the four-minute p95 and 54.2% on-time share. The allocation search picks capped groups at the higher assumed rate and full-power groups at the lower one. The model's goal is maximum capacity for identical jobs. A live mixed fleet would need to choose among traffic classes and respect what can actually move.

## Which jobs can absorb the limit?

A training job might accept slower steps if the remaining run meets its deadline. Pausing or relocating it also has a price in checkpoint writes, recovery time and network traffic. A latency-sensitive service can often protect small interactive requests by shedding or postponing a different class of traffic. The feasible policy depends on which workloads the site controls. The IEA notes that providers leasing infrastructure to third parties can have limited visibility into their customers' compute jobs. [IEA, *Powering Artificial Intelligence*](https://www.iea.org/reports/powering-artificial-intelligence/executive-summary)

Try the [downloadable scheduler](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) with `python3 physical-infrastructure-models.py power`, then add `--capped-rate 6` for the reversal. It models identical requests, constant capacity inside each time slot, and a fixed site overhead. For a real curtailment plan, replay a burst trace at each supported power setting and measure completed work, tail latency and the time the site needs to recover. A plan that meets the MW ceiling and leaves customers queued after the event still has a bill to pay.
