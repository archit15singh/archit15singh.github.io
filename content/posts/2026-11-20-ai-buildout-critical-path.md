---
title: "The AI buildout is a critical-path problem"
description: "A deployment model shows why getting GPUs four months early can buy zero months of revenue and how to find the milestone that matters."
date: 2026-11-20T09:13:00+05:30
tags: ["AI Infrastructure", "data centers", "systems engineering"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-engineering.svg"
  alt: "Dependencies that bring a GPU cluster into service."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

In a model of a new GPU cluster, paying to get the GPUs four months earlier buys exactly zero months of billable capacity. Paying to get grid power four months earlier buys one. Both outcomes follow from the same mistake in thinking about the project. The delivery date on a purchase order belongs to one branch of the schedule. The customer is waiting for the branches to join.

That distinction shows up in actual filings. At the end of September 2026, CoreWeave reported over 4.6 GW of contracted power and over 1.7 GW of active power. Its quarterly filing identifies a single leased site with 453 MW of electrical power still to be delivered in phases, according to the company's expectations. These figures describe different milestones in the development pipeline. A share of contracted power can be years away from service. [CoreWeave Q3 2026 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Third-Quarter-2026-Results/) · [CoreWeave Form 10-Q, Note 8](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm)

## Work backwards from the first customer handoff

Start with one cluster at one site. The operator in this example bills from contractual acceptance. Commissioning means installing and validating the system under load. It needs accelerators, a network fabric, a building with working cooling, and power. At the end, the customer also has to be ready to integrate and accept the cluster.

| Branch | Predecessor | Ready in month |
|---|---|---:|
| Financing | Project start | 2 |
| Accelerator delivery | Financing | 12 |
| Network fabric delivery | Financing | 16 |
| Building and cooling | Financing, then permits | 19 |
| Energization | Grid connection and switchgear | 20 |
| Customer readiness | Financing | 18 |
| Commissioning | Energization, cooling, GPUs, and fabric | 23 |
| Contractual acceptance | Commissioning and customer readiness | 25 |

The numbers are inputs to an illustrative model. Each step starts when its last predecessor finishes. Commissioning takes three months and acceptance takes two. In the baseline, the grid work finishes in month 20, after switchgear in month 14. That puts the grid branch on the critical path, the chain of dependent work that determines the earliest finish date. Cooling has one month of slack. The network fabric has four.

This changes the procurement question. If the accelerators arrive in month 8 and billing still starts in month 25, the business now carries the equipment for four extra months. Whether early delivery is worth paying for depends on how much it insures against a later shortage, whether the supplier offers flexible delivery, and who pays for storage and financing.

## What moves the date?

| Change to the baseline | First billable month | Branch holding up commissioning |
|---|---:|---|
| None | 25 | Grid |
| Accelerators arrive four months earlier | 25 | Grid |
| Grid work finishes four months earlier | 24 | Building and cooling |
| Grid work and cooling finish four months earlier | 21 | Grid and fabric, tied |
| Fabric arrives five months later | 26 | Fabric |

The fourth row shows what the individual delivery dates leave out. Advancing the grid work alone leaves the crew waiting on cooling. Advancing both works until the fabric and the grid finish together in month 16. At that point, bringing the date forward again requires speeding up both branches.

Public statements rarely let you build this schedule for an actual site. Even the demand side of the connection queue calls for care. In its preliminary November 2026 update, ERCOT reported responses from 433 loads covering about 177 GW of **requested** interconnection capacity. It also noted that some projects were still deciding basic equipment configurations such as cooling. Those are requests at different levels of maturity. The useful operational question is how much capacity passed each readiness milestone. [ERCOT preliminary data center impact survey, November 5, 2026](https://www.ercot.com/files/docs/2026/11/05/Community-Impact-RFI-PUC-Update.pdf)

## Put the acceptance date next to the hardware count

Phasing changes the graph. A campus may energize one hall while another waits on switchgear. If an independently useful block can be commissioned and accepted on its own, give it a separate milestone and a separate capacity figure. A training customer that needs one contiguous fabric may have a minimum block size. A serving workload that fits in smaller replicas has a different minimum. The IEA reports that electricity use often ramps gradually as facilities, equipment and workloads come online. [IEA, *Powering Artificial Intelligence*](https://www.iea.org/reports/powering-artificial-intelligence/executive-summary)

Try the [interactive critical-path simulator](/downloads/ai-infrastructure-reality-check/critical-path.html) to change the schedule in your browser. The [downloadable Python model](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) calculates finish dates and critical paths. Run `python3 physical-infrastructure-models.py deployment` for the cases above, or append `--task grid --months 14` to test a shorter grid task. The override is a task duration, measured from its predecessor's finish. Every scenario assumes fixed dependencies and durations. An actual budget decision needs a range for the uncertain finish dates, including correlated delays when several branches need the same vendor or construction crew.

The row I would ask for in a project review is **first customer-accepted MW by month**, with a named dependency and remaining slack. A count of GPUs in the building belongs on the same sheet. Put it next to the date someone can start billing for them.
