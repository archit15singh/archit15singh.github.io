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

On November 20, Corsair wanted $643.99 for a 32 GB kit it couldn't ship. Two months earlier, a snapshot showed the same kit in stock at $559.99. The $84 difference is easy to calculate. What a buyer actually paid is still an open question.

The trail gets clearer at the factory. Micron says it moved some DRAM supply to data-center and cloud customers in response to AI demand, with an emphasis on high-bandwidth memory. In November 2026, TrendForce reported slow PC sales and rising inventories of finished PCs. It still expected PC DRAM contract prices to rise 13–18% quarter over quarter in Q4. PC makers can sell fewer computers and pay more for memory if suppliers cut allocations faster than orders fall. [Micron FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/723125/000072312525000028/mu-20250828.htm) · [TrendForce November PC procurement report](https://www.trendforce.com/presscenter/news/20261111-13303.html)

## Two orders arrive at the fab

An accelerator order calls for high-bandwidth memory, or HBM. The manufacturer stacks several DRAM dies on a base die and links them vertically through the silicon. An interposer connects the stack to the accelerator within the package. A desktop DDR5 chip goes onto a module that plugs into the CPU's memory channels. The competition happens earlier, when the supplier allocates wafer starts and cleanroom space. By the time you can hold a DDR5 module, the wafer decision has already been made. [SK hynix and TSMC on HBM packaging](https://news.skhynix.com/en/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/) · [Micron FY2026 Q2 Form 10-Q](https://www.sec.gov/Archives/edgar/data/723125/000072312526000006/mu-20260226.htm)

Micron says HBM takes more wafers and cleanroom space to produce the same number of bits at the same node. TrendForce projected that HBM would take 22% of DRAM wafer input and account for 9% of bit supply among the top three suppliers at the end of 2026. Divide the bit share by the wafer share for HBM and again for conventional DRAM. On that mix, HBM would produce about 35% as many bits per wafer. Those are rounded projections across several products and processes. Use a fab's own yield and product mix to make the calculation for that fab. [Micron FY2026 Q2 Form 10-Q](https://www.sec.gov/Archives/edgar/data/723125/000072312526000006/mu-20260226.htm) · [TrendForce June HBM supply outlook](https://www.trendforce.com/presscenter/news/20260602-13074.html)

The second order is for the server itself. The host CPU needs memory for the software that feeds the accelerator. Depending on the system, that can mean registered DDR5 DIMMs or LPDDR5X modules. SK hynix attributed its September-quarter DRAM results in part to a jump in server DDR5 sales, alongside its first HBM4 shipments at scale. Both orders draw on the supplier's DRAM output. [SK hynix Q3 2026 results](https://news.skhynix.com/en/q3-2026-business-results/) · [NVIDIA Vera Rubin tuning guide](https://docs.nvidia.com/dccpu/vera-mn-perf-tuning-guide/system.html)

| Starting change | Where it reaches PC memory | What can weaken the effect |
| --- | --- | --- |
| More HBM wafer starts | Less of the shared capacity available for conventional DRAM, all else equal | More wafer starts or more bits per wafer |
| More server DDR5 orders | Suppliers can direct more output to server customers | Lower server orders or added conventional capacity |
| Higher PC DRAM contract quotes | A PC maker or module vendor faces higher replacement costs | Older inventory, weaker sell-through, or a promotion |

A packaging upgrade can let a supplier ship more HBM from the same wafer allocation. PC memory supply can still stay tight if server DDR5 orders absorb the extra bits.

## What a sold-out HBM order book buys

On November 4, 2026, TrendForce reported that Samsung had sold out its planned 2027 HBM supply. It said SK hynix had already agreed on 2027 HBM4 volumes and prices. To find out when each supplier gets paid, you need the contract. [TrendForce November 4 DRAM bulletin](https://www.trendforce.com/research/download/RP261104XL)

Micron's filings show how big the gap between promises and payments can get. At May 28, 2026, it reported about $5 billion allocated to remaining performance obligations, with $422 million recorded as contract liabilities. By September 3 those figures were about $134 billion and $13 billion. Most of the contract liabilities were customer deposits, and Micron expected to repay nearly all of those deposits between 2029 and 2031. It expected to recognize about a quarter of the September obligations as revenue over the following twelve months. The reported balance covers several products and delivery dates. It uses committed volumes and minimum prices and omits agreements without a fixed price or price band. [Micron FY2026 Q3 Form 10-Q](https://www.sec.gov/Archives/edgar/data/723125/000072312526000015/mu-20260528.htm) · [Micron FY2026 Form 10-K, revenue recognition](https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm)

The customer who puts money down has a claim on future supply. Before that memory is useful to a paying AI customer, someone still has to ship it, assemble a working rack and get the rack on a site that can run it.

## Four listings for one desktop kit

In December 2025, Micron announced it was leaving the Crucial consumer business to supply faster-growing data-center customers. It planned to ship Crucial products through its fiscal second quarter, which ended in February 2026. Here the link to PC builders is concrete. One retail brand was leaving the market for reasons its owner put in writing. [Micron's Crucial exit announcement](https://investors.micron.com/news/press-release/2025/Micron-Announces-Exit-from-Crucial-Consumer-Business-12-03-2025/default.aspx)

The sample below tracks one part number, CMK32GX5M2B6000C30. It's a black Corsair Vengeance DDR5-6000 CL30 kit with two 16 GB modules. Prices are in US dollars before tax. I dated the two indexed snapshots by their delivery estimates, September 23–25 for Corsair and November 7 in Sacramento for the Walmart marketplace listing. The last two pages were retrieved on November 20, 2026.

| Listing | Snapshot | Posted price | What the page showed |
| --- | --- | ---: | --- |
| [Corsair direct, earlier snapshot](https://www.corsair.com/us/en/p/memory/cmk32gx5m2b6000c30/vengeance-32gb-2x16gb-ddr5-dram-6000mt-s-c30-memory-kit-black-cmk32gx5m2b6000c30?position=17&queryID=1abf1f3e99539f8d97117880de64a447) | September 2026 | $559.99 | In stock, free shipping advertised |
| [Walmart marketplace](https://www.walmart.com/ip/2005681383) | Early November 2026 | $589.99 | Add to cart, sold by Newegg Inc., shipping to Sacramento advertised |
| [Newegg direct](https://www.newegg.com/corsair-vengeance-32gb-ddr5-6000-cas-latency-30-desktop-memory-black/p/N82E16820982007) | November 20, 2026 | $539.99 | Out of stock |
| [Corsair direct](https://www.corsair.com/us/en/p/memory/cmk32gx5m2b6000c30/vengeance-32gb-2x16gb-ddr5-dram-6000mt-s-c30-memory-kit-black-cmk32gx5m2b6000c30) | November 20, 2026 | $643.99 | Out of stock |

Corsair's posted price rose $84, or 15.0%, between the two snapshots. The September listing was a promotion. In November the kit was out of stock. Newegg also appeared twice, as the seller on Walmart and on its own site. Those were different sales channels. Four listings for one kit give us a record of offers and stock status. Measuring what shoppers paid across the US would take a different dataset. [Download the four observations](/downloads/ai-infrastructure-reality-check/retail-ddr5-observations.csv)

For someone building a local inference box, the RAM budget matters most when a model spills beyond the GPU. A dense 32-billion-parameter model at four bits per weight takes 16 billion bytes, about 14.9 GiB, for the weights alone. That leaves a 16 GiB card about 1.1 GiB for everything else, including quantization metadata and the context cache. Offloading some of the model to the CPU uses system RAM and can slow decoding. Compare builds on the model and context they can actually run at a speed you'd use. [llama.cpp memory and offload guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md)

## GPU rentals have a different price clock

In June 2025, AWS cut the on-demand rate for its H100-based P5 instances by 44% from its May 31 baseline. The H200-based P5en rate fell 25%. AWS credited economies of scale and offered other billing terms on newer B200 capacity. TrendForce's June survey, meanwhile, showed PC DRAM contract prices rising that quarter, with DDR4 leading DDR5. That pairs a change in one provider's list price with a survey of OEM contracts. [AWS June 2025 price announcement](https://aws.amazon.com/blogs/aws/announcing-up-to-45-price-reduction-for-amazon-ec2-nvidia-gpu-accelerated-instances/) · [TrendForce June 2025 DRAM contract survey](https://www.trendforce.com/research/download/RP250630WZ)

A cloud provider has already paid for, or is financing, the machine. Every idle hour expires. If more capacity comes online or customers move to newer GPUs, a discount can be cheaper than leaving an older rack empty. The memory supplier still has to decide which chips to make on its next wafers.

A price comparison over time needs the same cloud provider, region, GPU model and billing terms on each date. For retail RAM, match the seller, country and kit, and put stock status next to the quote. To test the factory story itself, track PC allocations, total bit output and inventory. I'd revise my view if suppliers kept shifting wafer capacity toward HBM and server memory while PC DRAM supply grew comfortably and PC contract prices fell for several quarters. In that case, weak PC demand or a larger supply of bits would be doing more of the work.
