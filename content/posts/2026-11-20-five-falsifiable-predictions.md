---
title: "Five predictions that could falsify my AI boom thesis"
description: "Five public indicators with deadlines, baseline values and rules for scoring a miss."
date: 2026-11-20T09:12:00+05:30
tags: [AI Infrastructure, Economics, Forecasting]
series: [The AI Infrastructure Reality Check]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-evidence.svg"
  alt: "Measures of AI demand, deployment, activity and economics."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

The claim I want to test is that paid AI demand can grow faster than the infrastructure underneath it becomes profitable. The bottleneck shifts from getting equipment to earning enough from it, with local power and commissioning delays slowing the transition. Five observations would give me reasons to revise parts of that thesis.

This is a forward test frozen on November 20, 2026. Each threshold is an editorial prediction based on the dated baseline, with no fitted probability or confidence interval. The [scorecard CSV](/downloads/ai-infrastructure-reality-check/prediction-scorecard.csv) leaves the result fields empty so they can be filled against the named disclosures.

## 1. A model company will turn usage growth into a lower compute ratio

**Prediction.** Anthropic's compute and infrastructure operating expense will be below 50% of revenue for the nine months ending September 30, 2027. Its final prospectus puts the expense at $18.808 billion on $33.242 billion of revenue in the first nine months of 2026, or 56.6%. The filing's category includes research and development compute as well as production infrastructure. A threshold of 50% tests whether sales grow faster than that combined bill. [Anthropic final prospectus, MD&A](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)

If the ratio stays at 50% or above, I would soften the claim that monetization is outpacing the compute bill at this company. A falling ratio could also come from mix, contract changes, or shifting spend between periods. It cannot tell us the gross margin of a million tokens. Use the nine-month totals on the same reporting basis, including any applicable restatement.

## 2. CoreWeave will bring a larger fraction of its contracted power online

**Prediction.** Active power divided by contracted power will reach at least 45% in CoreWeave's Q3 2027 disclosures. In Q3 2026 it reported over 1.7 GW active and over 4.6 GW contracted. Those rounded figures imply roughly 37%. The prediction calls for a material change in the ratio. [CoreWeave Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000461/coreweave3q26earningspress.htm)

A miss could mean the operator signed new power faster than it brought older sites online. Record absolute active GW next to the ratio and check the disclosure for a definition change before interpreting the outcome. Active power measures capacity. The billing system has the customer usage.

## 3. An operator's operating income will still trail its net interest bill

**Prediction.** CoreWeave's GAAP operating income will be less than its positive net interest expense in Q3 2027. It reported $207 million of operating income and $846 million of net interest expense in Q3 2026. Use the current filing's comparable quarterly income-statement lines. [CoreWeave Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000461/coreweave3q26earningspress.htm)

If operating income covers net interest in the quarter, the financing squeeze in this example has eased faster than forecast. This deliberately excludes adjusted EBITDA. The operator still has principal repayments, capital expenditure and taxes, each with its own cash timing.

## 4. New leases will still carry a double-digit wait to commencement

**Prediction.** Digital Realty's weighted-average lag between new leases signed in Q3 2027 and contractual commencement will be at least 12 months. The Q3 2026 baseline was 17 months. [Digital Realty Q3 2026 results](https://www.sec.gov/Archives/edgar/data/1297996/000110465926120212/dlr-ex99d1.htm)

A shorter lease lag would weaken the time-to-revenue argument for this landlord's signing mix. Record the large-capacity share alongside the result if the company discloses it. A quarter dominated by smaller, already-built deals could shorten the average even while a new hyperscale site waits for its switchgear.

## 5. Chip sales will grow through the conversion delays

**Prediction.** NVIDIA's Data Center revenue for Q3 FY2028 will be at least $120 billion on a comparable segment basis. The Q3 FY2027 baseline is $107.6 billion, so the threshold implies an increase of roughly 11.5%. [NVIDIA Q3 FY2027 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx)

A miss would make me revisit the idea that supply-chain revenue can keep climbing through a difficult conversion to profitable installed compute. A launch delay, customer inventory reduction or segment change would shape the interpretation.

## When to score it

Check all five by December 31, 2027, using the first comparable filings and earnings material available by that date. If a metric changes definition, a rounded figure straddles the threshold, or a company skips the disclosure, mark that row **unscorable**. Keep the original threshold visible even if a better indicator appears midyear.

These are tests of observable pieces, with overlap. The two CoreWeave rows describe the same company and may move together. A clean win for all five would support this series' account of upstream growth and uneven project returns. A model company holding its expense ratio above 50% while an operator covers its interest would force a more interesting rewrite. The part of the stack absorbing the pressure would have changed.
