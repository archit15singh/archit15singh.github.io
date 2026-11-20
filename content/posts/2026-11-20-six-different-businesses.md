---
title: "There isn't one AI bubble. There are six different businesses."
description: "Follow the invoices from DRAM fabs to paying AI users to see who earns revenue and who carries the risk."
date: 2026-11-20T09:15:00+05:30
tags: [AI Infrastructure, Economics, Data Centers]
series: [The AI Infrastructure Reality Check]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-market.svg"
  alt: "Six businesses in the AI stack, from memory to paid applications."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

NVIDIA reported $107.6 billion in Data Center revenue for the quarter ended October 25, 2026. CoreWeave reported $3.66 billion in revenue and a $709 million net loss for the quarter ended September 30. One company sells the hardware. The other has to keep selling access to hardware long enough to pay for it. The quarter-end dates differ, and these figures describe two businesses, with no attempt to trace a shared dollar between them. [NVIDIA Q3 FY2027 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx) · [CoreWeave Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000461/coreweave3q26earningspress.htm)

The phrase “AI bubble” makes it tempting to treat both numbers as evidence for opposing sides. I would draw the market as a set of invoices. Each invoice buys a different thing, and the risk often moves across the invoice before the end user sees the product.

## Six invoices, six ways to get paid

![Market map. Memory feeds accelerators. Accelerators, power and facilities enable compute, which applications buy to deliver paid workloads.](/downloads/ai-infrastructure-reality-check/ai-market-map.svg)

| Business | Who pays for what | Where the risk sits |
| --- | --- | --- |
| Accelerator and network silicon | Cloud and system buyers pay for accelerators, switches and other equipment. | The supplier has to plan production before demand settles. The buyer takes on the useful life and resale risk after accepting the equipment. |
| Memory | Accelerator makers and system vendors pay for HBM or conventional DRAM. | Memory producers allocate wafer capacity and invest ahead of demand. Buyers may commit to supply before the downstream machine earns anything. |
| Data-center development | Tenants pay for commissioned capacity, space and connectivity. | The party funding construction carries the delivery risk. Lease commencement, guarantees and remedies determine who pays for the delay. |
| Power | Facilities or their suppliers pay for energy, capacity and grid or on-site infrastructure. | The contract and local tariff determine who carries demand shortfalls and who funds upgrades. A power reservation is one milestone on the way to energization. |
| Compute | Labs and enterprises pay for reserved capacity or metered usage. | The operator has equipment, financing and delivery exposure. A take-or-pay contract can transfer some occupancy risk to the customer once the service is available. |
| Applications and models | People and businesses pay for API usage, subscriptions or software that performs a task. | The seller has to retain customers and cover serving and development costs. Renewal is where the original usage claim meets a budget decision. |

The division is analytical. A hyperscaler can occupy several rows. Its internal transfer price can help one division manage a budget, while the consolidation accounts eliminate internal revenue. A cloud booking and a GPU sale can also be genuine transactions between separate companies. Adding them together still answers a supply-chain activity question, with a different answer from what outsiders paid for AI products.

## Find the clock on the invoice

Digital Realty said new leases signed in Q3 2026 had a weighted-average lag of 17 months to **contractual commencement**. It reported $627 million of expected annualized GAAP base rent from that quarter's bookings at its share. The $627 million describes the annualized economics of leases signed that quarter. The 17 months tell you why a leasing headline can go up before rent starts. Neither item identifies the date a tenant will process its first customer request. [Digital Realty Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1297996/000110465926120212/dlr-ex99d1.htm)

CoreWeave's $132.5 billion revenue backlog at September 30 includes amounts expected under committed customer contracts and is subject to delivery and service availability. CoreWeave also reported $207 million in operating income and $846 million of net interest expense for the quarter. The backlog gives visibility into future deliveries. Interest is already a line on the income statement. [CoreWeave Q3 2026 results and backlog definition](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000461/coreweave3q26earningspress.htm)

At the top of the stack, Anthropic's final prospectus reported $33.24 billion of revenue and $18.81 billion of compute and infrastructure operating expenses for the nine months ended September 30, 2026. The expense category spans more than serving, including research and development compute. The filing shows monetization at scale and a large cost base, while leaving the margin of an individual request unresolved. [Anthropic final prospectus, MD&A](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)

## Follow a slowdown all the way back

Suppose an enterprise renews an AI product at half the usage. The application vendor feels that change first if the contract is metered. A cloud reservation can still be owed in full. The same can hold for a data-center lease even as the compute operator goes looking for another workload. A purchased GPU is already on the buyer's books. The next accelerator order is where a durable change in end demand may reach the chipmaker.

Contracts determine how long each layer can defer the reckoning. A cloud operator with a strong counterparty, prepayments and usable capacity has a different risk profile from an operator with the same equipment and short-term, uncontracted demand. Conversely, an application that starts earning more per dollar of compute may be able to cut its compute bill even as its own product improves.

That leaves me with a narrower question than “is AI a bubble?” Pick a company and trace one unit of capacity through the contracts. Ask who pays if commissioning slips, who pays if usage falls, and which renewal tests whether the capacity created enough value. The answer can change three times before you get to the GPU.
