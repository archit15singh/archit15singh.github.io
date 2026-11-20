---
title: "How AI demand puts upward pressure on DDR5 prices"
description: "Follow two routes from AI infrastructure orders to PC memory costs, then see where the evidence stops."
date: 2026-11-20T09:16:00+05:30
tags: ["AI Infrastructure", "DRAM", "Semiconductors"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-memory.svg"
  alt: "Six points in the memory supply chain, from DRAM wafers to retail."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

The clearest link between an AI rack and a PC memory bill is a wafer a supplier has to decide how to use. In its fiscal 2025 annual report, Micron said it shifted some DRAM supply toward data-center and hyperscale cloud customers in response to AI demand, with an emphasis on high-bandwidth memory. In November 2026, TrendForce was forecasting that **PC DRAM contract prices would rise 13–18% quarter over quarter in Q4**, even while reporting sluggish PC sales and rising finished-goods inventories. Weak PC sales and higher PC memory quotes can coexist when suppliers cut PC allocations faster than orders soften. [Micron FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/723125/000072312525000028/mu-20250828.htm) · [TrendForce’s November PC procurement report](https://www.trendforce.com/presscenter/news/20261111-13303.html)

## Two orders arrive at the fab

The first order is for high-bandwidth memory, or HBM. Multiple DRAM dies are stacked on a base die, with vertical electrical connections through the silicon. The stack sits close to the accelerator and connects through an interposer in the package. A desktop DDR5 kit takes a different route. Its DRAM chips end up on a module for the CPU's memory channels. The finished products have different interfaces and customers, but their upstream competition includes DRAM wafer starts and cleanroom capacity. A completed DDR5 chip has already passed the point where a supplier could redirect its production slot to HBM. [SK hynix and TSMC on HBM packaging](https://news.skhynix.com/en/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/) · [Micron FY2026 Q2 Form 10-Q](https://www.sec.gov/Archives/edgar/data/723125/000072312526000006/mu-20260226.htm)

Micron says that, for the same number of bits at the same technology node, HBM requires more wafers and cleanroom space. TrendForce's June 2026 outlook gives a sense of scale. Among the top three suppliers, it projected HBM would account for around **22% of DRAM wafer input and 9% of bit supply** at the end of 2026. Divide bit share by wafer share for each category and compare the two. The result is an implied HBM output per wafer of roughly **35% of conventional DRAM output per wafer** in that projection. This is a calculation on rounded industry shares with a mix of products and processes. An individual fab or production node will have its own ratio. [Micron FY2026 Q2 Form 10-Q](https://www.sec.gov/Archives/edgar/data/723125/000072312526000006/mu-20260226.htm) · [TrendForce’s June HBM supply outlook](https://www.trendforce.com/presscenter/news/20260602-13074.html)

The other order is for server main memory. AI infrastructure also needs host CPUs and memory to run the software around the accelerator. A server can use registered DDR5 DIMMs or another design such as LPDDR5X modules. SK hynix credited a significant rise in server DDR5 sales as well as the start of HBM4 shipments at scale for its Q3 2026 DRAM results. HBM earns the headlines. The server DDR5 order matters because it pulls on conventional memory supply, too. [SK hynix Q3 2026 results](https://news.skhynix.com/en/q3-2026-business-results/) · [NVIDIA’s Vera Rubin tuning guide](https://docs.nvidia.com/dccpu/vera-mn-perf-tuning-guide/system.html)

| Starting change | Where it reaches PC memory | What can weaken the effect |
| --- | --- | --- |
| More HBM wafer starts | Less of the shared capacity available for conventional DRAM, all else equal | More wafer starts or more bits per wafer |
| More server DDR5 orders | Suppliers can direct more output to server customers | Lower server orders or added conventional capacity |
| Higher PC DRAM contract quotes | A PC maker or module vendor faces higher replacement costs | Older inventory, weaker sell-through, or a promotion |

This is a dependency map. Its arrows describe a direction under stated conditions. Extra HBM packaging capacity, for example, can improve shipments without moving PC memory prices if wafer allocation holds steady. Conversely, an easing HBM bottleneck could still leave conventional DRAM tight if server DDR5 orders keep absorbing new supply.

## The claim I'd test

I would expect weaker PC DRAM allocations or higher PC contract quotes where suppliers shift the most capacity to HBM and server memory, after accounting for total bit growth and downstream inventory. The argument weakens if suppliers keep raising their HBM and server allocations while PC bit supply grows comfortably and PC DRAM quotes fall across several quarters. In that case, new capacity or weak PC demand could be doing more work than the shift in product mix.

The 13–18% figure concerns contract prices and comes from a forecast, so it can differ from what a builder sees on a retail kit. A same-SKU series with stock status, channel, and country held fixed would measure what happened at checkout. The strongest evidence today sits one step upstream. Suppliers reported moving capacity, and a higher-value order on the same production line can raise the cost of supplying a PC even when fewer PCs are selling.
