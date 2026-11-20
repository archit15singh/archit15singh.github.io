---
title: "What a sold-out HBM order book tells you"
description: "Follow a memory contract through deposits, shipment, deployment, and the economics of the application it ultimately serves."
date: 2026-11-20T09:11:00+05:30
tags: ["AI Infrastructure", "HBM", "Semiconductors"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-memory.svg"
  alt: "Six points in the memory supply chain, from DRAM wafers to retail."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

TrendForce reported on November 4, 2026 that Samsung's planned 2027 HBM supply was sold out and that SK hynix's next-year HBM4 volumes and prices were already agreed. That tells us about production allocation at two suppliers. The answer to what the buyers have committed to, and when the suppliers get paid, is in the contract. [TrendForce’s November 4 DRAM bulletin](https://www.trendforce.com/research/download/RP261104XL)

Memory buyers can put down billions in aggregate to secure future production, take delivery over several years, and eventually get their deposits back. Micron's fiscal 2026 filing describes that structure. As of September 3 it had approximately **$134 billion** allocated to remaining performance obligations, of which it recorded about **$13 billion** as contract liabilities, primarily customer deposits. It expects to repay nearly all the deposits between 2029 and 2031. These figures span strategic agreements across Micron's business. They show what a commitment and a payment mean before an accelerator has done any useful work. [Micron FY2026 Form 10-K, revenue recognition and remaining performance obligations](https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm)

## Find the obligation before counting the dollars

A buyer can reserve capacity when it needs supply assurance for a launch that is several quarters away. What happens if that launch slips depends on the deal. Some agreements leave pricing to a later negotiation. Micron described a firmer structure for its strategic agreements. They bind buyers to specific volumes over multiple years on a take-or-pay basis. The majority have minimum and maximum pricing. Micron returns a deposit if the buyer meets minimum purchases, and can retain some or all of it if the buyer falls short. The deposit is a way to secure production slots and give the supplier protection if the buyer breaks its commitment. [Micron FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm)

The figure moved quickly. As of May 28, Micron had disclosed around $5 billion of remaining performance obligations, including $422 million recorded as contract liabilities. In September the reported obligations reached $134 billion. Micron estimated that about a quarter of the September balance would turn into revenue in the following twelve months. The filing uses committed volumes and minimum prices, and excludes agreements without fixed prices or price bands. Treat the balance as a measure of disclosed contractual performance still owed. It spans products and delivery dates, so the difference between May and September cannot be read as an increase in HBM orders or reported sales. [Micron FY2026 Q3 Form 10-Q](https://www.sec.gov/Archives/edgar/data/723125/000072312526000015/mu-20260528.htm) · [Micron FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm)

SK hynix supplied a different way to measure commitments. It said in October that long-term agreements covered more than 50% of its 2027–28 production capacity and reported that shipments of HBM4 had begun at scale. The 50% figure covers the company's production capacity as reported, and the release gives no comparable HBM-only figure. It matters whether a headline counts one supplier's output, a specific generation's allocation, or every manufacturer's available capacity. [SK hynix Q3 2026 results](https://news.skhynix.com/en/q3-2026-business-results/)

## Follow a stack through the transaction

| Stage | What to look for | Exposure that remains |
| --- | --- | --- |
| Capacity committed | Supplier, generation, volume, dates, minimums, and pricing basis | Qualification and production ramp |
| Deposit paid, where applicable | Cash received and how the supplier records it | Supplier still owes delivery or other performance under the contract |
| Stack delivered | Transfer under the contract and memory revenue recognized when the performance obligation is satisfied | Accelerator buyer still needs a working, qualified system |
| Rack accepted and serving | Commissioned capacity, uptime, and the date customer billing begins | Idle capacity, rate resets, and operating costs |
| Customer renews | Revenue collected over time and contribution after serving costs | Churn, new competitors, and return on replacement capital |

Here is a scenario the phrase “sold out” leaves open. An accelerator customer takes delivery under a binding agreement. The rack operator then loses two months waiting for a site to be ready. During those two months the memory supplier may already have recognized revenue, while the operator still carries financing and facility costs. Once the rack comes online, the application on top still needs repeat paying usage. One company's protection can leave another company holding the tab.

The follow-up to a sold-out announcement is therefore a specific question about the contract. Who pays, when, and what needs to happen first? The better answer may be a buyer obligated to take delivery at a minimum price. That is real commercial demand for the memory supplier. A repeat customer paying enough to cover the full cost of serving is evidence for a different business farther down the chain.
