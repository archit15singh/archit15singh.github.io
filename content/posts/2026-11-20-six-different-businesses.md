---
title: "Six AI businesses and five tests of the boom"
description: "Follow the money across six businesses, examine the strongest demand evidence and revisit five predictions in 2027."
date: 2026-11-20T09:15:00+05:30
tags: [AI Infrastructure, Economics, Data Centers]
series: [The AI Infrastructure Reality Check]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-market.svg"
  alt: "Six businesses in the AI stack, from memory to paid applications."
  hidden: false
format: "Technical note"
aliases:
  - "/posts/2026-11-20-strongest-bullish-countercase/"
  - "/posts/2026-11-20-five-falsifiable-predictions/"
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

## The strongest evidence of real demand

One of the better arguments against an AI bubble story is buried in Anthropic's final prospectus. For the nine months ended September 30, 2026, revenue rose from $2.545 billion a year earlier to $33.242 billion. The company attributes $24.2 billion of that increase to consumption-based revenue and $6.5 billion to subscriptions. If you dismiss the entire buildout as a wager on customers who have yet to appear, that income statement is a problem. [Anthropic final prospectus, MD&A](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)

Anthropic reports more than 11,900 customers with at least $100,000 of trailing-twelve-month revenue at September 30, 2026, versus more than 950 a year earlier. It reports that customers above this threshold represented about 74% of first-nine-month revenue. These are company-defined customer and revenue measures, with concentration risk still possible inside the group. They put a firmer floor under the demand argument than an account signup count. [Anthropic final prospectus, revenue comparison](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)

Researchers using the U.S. Census Bureau's nationally representative Business Trends and Outlook Survey AI supplement found that 18% of firms used AI in a business function in the November 2025 to January 2026 reference period. On an employment-weighted basis the figure was 32%, reflecting higher adoption at larger businesses. The employment-weighted result describes employment at firms that use AI. Counting individual employees who actually touch a model would require a different measure. [U.S. Census Bureau working paper, The Microstructure of AI Diffusion](https://www.census.gov/library/working-papers/2026/adrm/CES-WP-26-25.html)

Self-reported use says little about spend per workflow or return on investment. It is valuable because it samples organizations across the economy with a known method. In conjunction with reported revenue it makes a narrower bullish case. The product has paying users, and adoption reaches beyond the handpicked customer examples on a model vendor's site.

The IEA estimates that global data-center electricity demand rose 17% in 2025, with electricity demand at AI-focused data centers up 50%. The first figure covers data centers broadly. The second is for the IEA's AI-focused group, which is a facility-level estimate. Electricity draw records production activity and supporting overhead, and cannot price the output. It still gives an independent physical check on the buildout. [IEA, Key Questions on Energy and AI](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary)

## Five tests to score by December 31, 2027

My working thesis is that paid demand can grow while parts of the buildout remain constrained by commissioning, the cost of capital or slow payback. Each threshold was set on November 20, 2026 and can be checked against a named public disclosure.

[Download the scorecard CSV](/downloads/ai-infrastructure-reality-check/prediction-scorecard.csv). The result fields are open until comparable filings are available.

### 1. A model company will turn usage growth into a lower compute ratio

**Prediction.** Anthropic's compute and infrastructure operating expense will be below 50% of revenue for the nine months ending September 30, 2027. Its final prospectus puts the expense at $18.808 billion on $33.242 billion of revenue in the first nine months of 2026, or 56.6%. The filing's category includes research and development compute as well as production infrastructure. A threshold of 50% tests whether sales grow faster than that combined bill. [Anthropic final prospectus, MD&A](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)

If the ratio stays at 50% or above, I would soften the claim that monetization is outpacing the compute bill at this company. A falling ratio could also come from mix, contract changes, or shifting spend between periods. It cannot tell us the gross margin of a million tokens. Use the nine-month totals on the same reporting basis, including any applicable restatement.

### 2. CoreWeave will bring a larger fraction of its contracted power online

**Prediction.** Active power divided by contracted power will reach at least 45% in CoreWeave's Q3 2027 disclosures. In Q3 2026 it reported over 1.7 GW active and over 4.6 GW contracted. Those rounded figures imply roughly 37%. The prediction calls for a material change in the ratio. [CoreWeave Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000461/coreweave3q26earningspress.htm)

A miss could mean the operator signed new power faster than it brought older sites online. Record absolute active GW next to the ratio and check the disclosure for a definition change before interpreting the outcome. Active power measures capacity. The billing system has the customer usage.

### 3. An operator's operating income will still trail its net interest bill

**Prediction.** CoreWeave's GAAP operating income will be less than its positive net interest expense in Q3 2027. It reported $207 million of operating income and $846 million of net interest expense in Q3 2026. Use the current filing's comparable quarterly income-statement lines. [CoreWeave Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000461/coreweave3q26earningspress.htm)

If operating income covers net interest in the quarter, the financing squeeze in this example has eased faster than forecast. This deliberately excludes adjusted EBITDA. The operator still has principal repayments, capital expenditure and taxes, each with its own cash timing.

### 4. New leases will still carry a double-digit wait to commencement

**Prediction.** Digital Realty's weighted-average lag between new leases signed in Q3 2027 and contractual commencement will be at least 12 months. The Q3 2026 baseline was 17 months. [Digital Realty Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1297996/000110465926120212/dlr-ex99d1.htm)

A shorter lease lag would weaken the time-to-revenue argument for this landlord's signing mix. Record the large-capacity share alongside the result if the company discloses it. A quarter dominated by smaller, already-built deals could shorten the average even while a new hyperscale site waits for its switchgear.

### 5. Chip sales will grow through the conversion delays

**Prediction.** NVIDIA's Data Center revenue for Q3 FY2028 will be at least $120 billion on a comparable segment basis. The Q3 FY2027 baseline is $107.6 billion, so the threshold implies an increase of roughly 11.5%. [NVIDIA Q3 FY2027 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx)

A miss would make me revisit the idea that supply-chain revenue can keep climbing through a difficult conversion to profitable installed compute. A launch delay, customer inventory reduction or segment change would shape the interpretation.

Check all five by December 31, 2027, using the first comparable filings and earnings material available by that date. If a metric changes definition, a rounded figure straddles the threshold, or a company skips the disclosure, mark that row **unscorable**. Keep the original threshold visible even if a better indicator appears midyear.

These are tests of observable pieces, with overlap. The two CoreWeave rows describe the same company and may move together. A clean win for all five would support this series' account of upstream growth and uneven project returns. A model company holding its expense ratio above 50% while an operator covers its interest would force a more interesting rewrite. The part of the stack absorbing the pressure would have changed.
