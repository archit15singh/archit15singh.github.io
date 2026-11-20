---
title: "How the AI buildout reaches your DDR5 bill"
description: "Trace HBM and server demand through wafer allocation, supply contracts, retail listings and GPU rental prices."
date: 2026-11-20T09:16:00+05:30
tags: ["AI Infrastructure", "DRAM", "Semiconductors"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-memory.svg"
  alt: "Six points in the memory supply chain, from DRAM wafers to retail."
  hidden: false
format: "Technical note"
aliases:
  - "/posts/2026-11-20-sold-out-hbm-contracts/"
  - "/posts/2026-11-20-how-ai-infrastructure-affects-pc-builds/"
  - "/posts/2026-11-20-why-gpu-rent-and-ram-prices-diverge/"
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

## What a sold-out HBM order book buys

TrendForce reported on November 4, 2026 that Samsung's planned 2027 HBM supply was sold out and that SK hynix's next-year HBM4 volumes and prices were already agreed. That tells us about production allocation at two suppliers. The answer to what the buyers have committed to, and when the suppliers get paid, is in the contract. [TrendForce’s November 4 DRAM bulletin](https://www.trendforce.com/research/download/RP261104XL)

Memory buyers can put down billions in aggregate to secure future production, take delivery over several years, and eventually get their deposits back. Micron's fiscal 2026 filing describes that structure. As of September 3 it had approximately **$134 billion** allocated to remaining performance obligations, of which it recorded about **$13 billion** as contract liabilities, primarily customer deposits. It expects to repay nearly all the deposits between 2029 and 2031. These figures span strategic agreements across Micron's business. They show what a commitment and a payment mean before an accelerator has done any useful work. [Micron FY2026 Form 10-K, revenue recognition and remaining performance obligations](https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm)

The figure moved quickly. As of May 28, Micron had disclosed around $5 billion of remaining performance obligations, including $422 million recorded as contract liabilities. In September the reported obligations reached $134 billion. Micron estimated that about a quarter of the September balance would turn into revenue in the following twelve months. The filing uses committed volumes and minimum prices, and excludes agreements without fixed prices or price bands. Treat the balance as a measure of disclosed contractual performance still owed. It spans products and delivery dates, so the difference between May and September cannot be read as an increase in HBM orders or reported sales. [Micron FY2026 Q3 Form 10-Q](https://www.sec.gov/Archives/edgar/data/723125/000072312526000015/mu-20260528.htm) · [Micron FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm)

A memory buyer's payment secures capacity upstream. Between that commitment and a paid AI workload sit product qualification, shipment, rack acceptance and customer renewal. Each milestone gives a different business a reason to put revenue on the books.

## Four listings for one desktop kit

The upstream change is clearer than the size of any retail price increase. In December 2025, Micron announced it would exit its Crucial consumer business, citing demand from faster-growing data-center customers. It said consumer shipments would continue through fiscal Q2, which ended in February 2026. That's a documented change in one supplier's priorities and a direct example of how strategic data-center orders can change the choices available to builders. Crucial is a retail brand, so the announcement applies to its consumer-branded business. [Micron’s Crucial exit announcement](https://investors.micron.com/news/press-release/2025/Micron-Announces-Exit-from-Crucial-Consumer-Business-12-03-2025/default.aspx)

I matched the manufacturer part number **CMK32GX5M2B6000C30**, the black Corsair Vengeance 32 GB kit with two 16 GB modules, rated for DDR5-6000 CL30. Prices are displayed US dollars before tax. The September Corsair observation comes from an indexed snapshot with a September 23–25 delivery estimate. The Walmart marketplace observation comes from a snapshot quoting November 7 delivery to Sacramento. Those estimates identify the snapshots approximately. The two remaining listings were retrieved November 20.

| Listing | Snapshot | Posted price | What the page showed |
| --- | --- | ---: | --- |
| [Corsair direct, earlier snapshot](https://www.corsair.com/us/en/p/memory/cmk32gx5m2b6000c30/vengeance-32gb-2x16gb-ddr5-dram-6000mt-s-c30-memory-kit-black-cmk32gx5m2b6000c30?position=17&queryID=1abf1f3e99539f8d97117880de64a447) | September 2026 | $559.99 | In stock, free shipping advertised |
| [Walmart marketplace](https://www.walmart.com/ip/2005681383) | Early November 2026 | $589.99 | Add to cart, sold by Newegg Inc., shipping to Sacramento advertised |
| [Newegg direct](https://www.newegg.com/corsair-vengeance-32gb-ddr5-6000-cas-latency-30-desktop-memory-black/p/N82E16820982007) | November 20, 2026 | $539.99 | Out of stock |
| [Corsair direct](https://www.corsair.com/us/en/p/memory/cmk32gx5m2b6000c30/vengeance-32gb-2x16gb-ddr5-dram-6000mt-s-c30-memory-kit-black-cmk32gx5m2b6000c30) | November 20, 2026 | $643.99 | Out of stock |

Corsair's two matching listings show an $84 increase in posted price, or 15.0% relative to the September figure, and a shift from listed in stock to out of stock. The September price was promotional, which makes the change even harder to attribute to wholesale memory costs. The sample measures posted offers. The later direct offer was unavailable, leaving the change in actual purchase prices unmeasured. The November marketplace figure is a separate fulfillment channel even though Newegg appears on both pages. These four records document a specific kit and give no basis for a US retail index. [Download the observations](/downloads/ai-infrastructure-reality-check/retail-ddr5-observations.csv)

Take a hypothetical dense 32-billion-parameter model at four bits per weight. Its raw weights take 16 billion bytes, or about **14.9 GiB**, before quantization metadata and runtime overhead. A 16 GiB GPU leaves about 1.1 GiB after that idealized weight allocation. The model and its context can exceed that budget. If part of the model moves onto the CPU, the RAM bill changes what the machine can run, and the CPU work can lower decode speed. The relevant purchase comparison is the cheapest available setup that fits the intended model and context at a tolerable speed. [llama.cpp memory and offload guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md)

## GPU rentals have a different price clock

In June 2025, AWS cut the on-demand rate for its H100-based EC2 P5 instances by 44% against its May 31 baseline. TrendForce's June survey recorded rising PC DRAM contract prices in the same quarter, with DDR4 leading the increase and DDR5 rising more slowly. These are narrow observations with opposite signs. One is a named provider's discrete repricing. The other describes a class of memory contracts that PC manufacturers negotiate. [AWS’s June 2025 announcement](https://aws.amazon.com/blogs/aws/announcing-up-to-45-price-reduction-for-amazon-ec2-nvidia-gpu-accelerated-instances/) · [TrendForce’s June 2025 DRAM contract survey](https://www.trendforce.com/research/download/RP250630WZ)

A cloud provider already running a paid-for or financed accelerator faces a different decision. Once the current hour passes unused, it cannot sell that hour tomorrow. If available supply of an older generation grows, or customers move work to newer GPUs, a provider can cut its asking rate while new hardware remains expensive. This is a mechanism, and AWS gave its own explanation for the June price change. It attributed the move to economies of scale and published different cuts for different instance types and billing plans. AWS reported a 44% on-demand reduction for P5 and a 25% reduction for the H200-based P5en. Its launch article also discussed newer B200 capacity with different purchase terms. [AWS’s June 2025 announcement](https://aws.amazon.com/blogs/aws/announcing-up-to-45-price-reduction-for-amazon-ec2-nvidia-gpu-accelerated-instances/)

To compare the two through time, keep the provider, region, GPU SKU and billing terms fixed for rentals. On the RAM side, track available offers for the same kit, seller and country. A change in stock belongs beside the price.

I would expect weaker PC DRAM allocations or higher PC contract quotes where suppliers shift the most capacity to HBM and server memory, after accounting for total bit growth and downstream inventory. The argument weakens if suppliers keep raising their HBM and server allocations while PC bit supply grows comfortably and PC DRAM quotes fall across several quarters. In that case, new capacity or weak PC demand could be doing more work than the shift in product mix.
