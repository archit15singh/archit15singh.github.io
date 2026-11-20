---
title: "Why GPU rental and RAM prices can move in opposite directions"
description: "An AWS rate cut and a rising PC DRAM contract market show how installed capacity and fresh manufacturing respond to different constraints."
date: 2026-11-20T09:09:00+05:30
tags: ["AI Infrastructure", "Cloud Economics", "DRAM"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-memory.svg"
  alt: "Six points in the memory supply chain, from DRAM wafers to retail."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

In June 2025, AWS cut the on-demand rate for its H100-based EC2 P5 instances by 44% against its May 31 baseline. TrendForce's June survey recorded rising PC DRAM contract prices in the same quarter, with DDR4 leading the increase and DDR5 rising more slowly. These are narrow observations with opposite signs. One is a named provider's discrete repricing. The other describes a class of memory contracts that PC manufacturers negotiate. [AWS’s June 2025 announcement](https://aws.amazon.com/blogs/aws/announcing-up-to-45-price-reduction-for-amazon-ec2-nvidia-gpu-accelerated-instances/) · [TrendForce’s June 2025 DRAM contract survey](https://www.trendforce.com/research/download/RP250630WZ)

## A factory sells a new part. A cloud rents an installed machine.

When a memory supplier sets a contract quote, it has to decide what to manufacture and which customer gets the output. Wafer availability, yield, older products nearing end of life, and competing server orders can all change the answer. In June 2025 TrendForce pointed to production reductions and early procurement as reasons DDR4 prices rose more than DDR5. In April it also reported tariff-related stockpiling. That quarter's divergence needs no assumption that AI demand caused every memory increase. [TrendForce’s June 2025 DRAM contract survey](https://www.trendforce.com/research/download/RP250630WZ) · [TrendForce’s April 2025 stockpiling report](https://www.trendforce.com/presscenter/news/20250417-12551.html)

A cloud provider already running a paid-for or financed accelerator faces a different decision. Once the current hour passes unused, it cannot sell that hour tomorrow. If available supply of an older generation grows, or customers move work to newer GPUs, a provider can cut its asking rate while new hardware remains expensive. This is a mechanism, and AWS gave its own explanation for the June price change. It attributed the move to economies of scale and published different cuts for different instance types and billing plans. AWS reported a 44% on-demand reduction for P5 and a 25% reduction for the H200-based P5en. Its launch article also discussed newer B200 capacity with different purchase terms. [AWS’s June 2025 announcement](https://aws.amazon.com/blogs/aws/announcing-up-to-45-price-reduction-for-amazon-ec2-nvidia-gpu-accelerated-instances/)

An hourly quote is also a bundle. An AWS p5.48xlarge includes eight H100s, host CPUs and memory, and high-speed networking. Dividing the instance rate by eight gives an effective price per GPU-hour *when the whole instance is the unit you buy*. It cannot tell you what one H100 costs on a shared host. A prepaid capacity block, a spot instance that can be interrupted, and an on-demand slot buy different assurances. [AWS P5 specifications](https://aws.amazon.com/ec2/instance-types/p5/) · [AWS Capacity Blocks pricing](https://aws.amazon.com/ec2/capacityblocks/pricing/)

## Keep both series fixed before claiming a trend

| What a chart should track | Hold fixed across dates | Record separately |
| --- | --- | --- |
| Cloud rental | Provider, region, instance, accelerator variant, GPU count, billing terms | Availability, interruption policy, networking, and storage charges |
| PC RAM | Country, seller, exact part number, condition, and stock status | Promotions, shipping, tax, and marketplace fulfillment |
| OEM memory contracts, if used | Product class, buyer segment, and contract window | Whether each figure is an observation or a forecast |

Use price changes within each series. If you want both on one chart, index each to 100 at the same starting date and leave a gap when an offer is unavailable. An unavailable listing can still tell you something about scarcity, but today's displayed price on a slot that cannot be bought is a poor stand-in for today's cost of renting it.

The June 2025 comparison establishes that a cloud rate can fall while a memory contract market rises. It does not establish a persistent divergence in 2026. On November 17, 2026, GPU provider Runpod described a tighter rental market. On November 11, TrendForce forecast Q4 PC DRAM contract prices up 13–18% quarter over quarter. Runpod's account is a provider's assessment and refers to external contract-rate data. TrendForce's estimate concerns PC OEM procurement. A matched multi-provider rental series and a same-SKU retail basket would be needed to tell whether the respective market prices actually diverged through that period. [Runpod’s November GPU supply assessment](https://www.runpod.io/blog/the-gpu-supply-supercycle-is-here) · [TrendForce’s November PC procurement report](https://www.trendforce.com/presscenter/news/20261111-13303.html)

A cheaper rental quote tells you something about the machine and contract on the screen. The next kit off the production line has its own buyers, production schedule, and price.
