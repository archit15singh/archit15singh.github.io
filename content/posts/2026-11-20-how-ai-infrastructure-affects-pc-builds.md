---
title: "What the AI buildout changes for a PC builder"
description: "A matched DDR5 kit shows why posted price and stock both matter, especially for a local AI workstation."
date: 2026-11-20T09:10:00+05:30
tags: ["AI Infrastructure", "PC Hardware", "Local AI"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-memory.svg"
  alt: "Six points in the memory supply chain, from DRAM wafers to retail."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

In November 2026, Newegg showed $539.99 for a 32 GB Corsair DDR5 kit. Corsair's own site showed $643.99 for the same part number. Both showed it out of stock. A price comparison would hand the win to Newegg. A shopping cart would give you neither kit. [Newegg product page](https://www.newegg.com/corsair-vengeance-32gb-ddr5-6000-cas-latency-30-desktop-memory-black/p/N82E16820982007) · [Corsair direct product page](https://www.corsair.com/us/en/p/memory/cmk32gx5m2b6000c30/vengeance-32gb-2x16gb-ddr5-dram-6000mt-s-c30-memory-kit-black-cmk32gx5m2b6000c30)

The upstream change is clearer than the size of any retail price increase. In December 2025, Micron announced it would exit its Crucial consumer business, citing demand from faster-growing data-center customers. It said consumer shipments would continue through fiscal Q2, which ended in February 2026. That's a documented change in one supplier's priorities and a direct example of how strategic data-center orders can change the choices available to builders. Crucial is a retail brand, so the announcement applies to its consumer-branded business. [Micron’s Crucial exit announcement](https://investors.micron.com/news/press-release/2025/Micron-Announces-Exit-from-Crucial-Consumer-Business-12-03-2025/default.aspx)

## Four listings, one part number

I matched the manufacturer part number **CMK32GX5M2B6000C30**, the black Corsair Vengeance 32 GB kit with two 16 GB modules, rated for DDR5-6000 CL30. Prices are displayed US dollars before tax. The September Corsair observation comes from an indexed snapshot with a September 23–25 delivery estimate. The Walmart marketplace observation comes from a snapshot quoting November 7 delivery to Sacramento. Those estimates identify the snapshots approximately. The two remaining listings were retrieved November 20.

| Listing | Snapshot | Posted price | What the page showed |
| --- | --- | ---: | --- |
| [Corsair direct, earlier snapshot](https://www.corsair.com/us/en/p/memory/cmk32gx5m2b6000c30/vengeance-32gb-2x16gb-ddr5-dram-6000mt-s-c30-memory-kit-black-cmk32gx5m2b6000c30?position=17&queryID=1abf1f3e99539f8d97117880de64a447) | September 2026 | $559.99 | In stock, free shipping advertised |
| [Walmart marketplace](https://www.walmart.com/ip/2005681383) | Early November 2026 | $589.99 | Add to cart, sold by Newegg Inc., shipping to Sacramento advertised |
| [Newegg direct](https://www.newegg.com/corsair-vengeance-32gb-ddr5-6000-cas-latency-30-desktop-memory-black/p/N82E16820982007) | November 20, 2026 | $539.99 | Out of stock |
| [Corsair direct](https://www.corsair.com/us/en/p/memory/cmk32gx5m2b6000c30/vengeance-32gb-2x16gb-ddr5-dram-6000mt-s-c30-memory-kit-black-cmk32gx5m2b6000c30) | November 20, 2026 | $643.99 | Out of stock |

Corsair's two matching listings show an $84 increase in posted price, or 15.0% relative to the September figure, and a shift from listed in stock to out of stock. The September price was promotional, which makes the change even harder to attribute to wholesale memory costs. None of these observations is a completed sale. The only same-seller pair ends with an unavailable listing, so there is no same-seller purchase-price change to report. The November marketplace figure is a separate fulfillment channel even though Newegg appears on both pages. These four records document a specific kit and give no basis for a US retail index. [Download the observations](/downloads/ai-infrastructure-reality-check/retail-ddr5-observations.csv)

## The cost of cutting the RAM budget

For a local AI workstation with a discrete GPU, there are two memory budgets. A model hosted fully on the GPU needs video memory for weights, context cache, and runtime buffers. A model distributed across CPU and GPU draws on system RAM as well. If you cut system memory to reduce the build price, a model that would have fit through partial CPU offload may force you to shorten the context, use a smaller model, or rent the compute. More RAM helps with capacity in the offloaded case. Speed still depends on the GPU allocation, host bandwidth, and workload. [llama.cpp memory and offload guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md)

Take a hypothetical dense 32-billion-parameter model at four bits per weight. Its raw weights take 16 billion bytes, or about **14.9 GiB**, before quantization metadata and runtime overhead. A 16 GiB GPU leaves about 1.1 GiB after that idealized weight allocation. The model and its context can exceed that budget. If part of the model moves onto the CPU, the RAM bill changes what the machine can run, and the CPU work can lower decode speed. The relevant purchase comparison is the cheapest available setup that fits the intended model and context at a tolerable speed. [llama.cpp memory and offload guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md)

A buyer can learn more from tracking a few exact part numbers and filtering for available inventory than from a headline about memory prices. The same discipline applies to a vendor's forecast. TrendForce projected PC DRAM contracts up 13–18% quarter over quarter in Q4 2026 and client SSD contracts up less than 5%, in the same release. A build has separate line items for a reason. [TrendForce’s November PC procurement report](https://www.trendforce.com/presscenter/news/20261111-13303.html)
