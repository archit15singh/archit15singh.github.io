---
title: "The GPU break-even equation nobody shows you"
description: "A per-GPU model for the price and billable hours needed to recover hardware, power, operations and the cost of capital."
date: 2026-11-20T09:14:00+05:30
tags: [AI Infrastructure, GPU Economics, Modeling]
series: [The AI Infrastructure Reality Check]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-economics.svg"
  alt: "The inputs to fleet economics, from upfront cost to realized returns."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

A GPU can sell 90% of the hours in a year and still come up $1,212 short. In the deployment below, the operator realizes $2 an hour, pays for a share of the server and network, and expects to replace the hardware after four years. Push the rental rate to $2.50 and the same machine needs to sell about 77% of the year. Open the [GPU break-even calculator](/downloads/ai-infrastructure-reality-check/gpu-break-even.html) to change any of those inputs.

## Pick a denominator before looking at telemetry

A billing record tells you what the customer owes. GPU telemetry tells you how much work the device did during the sample. The two can move independently. An eight-GPU reservation can be fully billable while a customer's code runs on six GPUs. A week spent testing the provider's software can keep all eight busy without yielding a billable hour. The denominator I use is 8,760 calendar hours per GPU. Every outage, empty slot or maintenance hour reduces the fraction that can be sold.

Publication prices give you a sense of how much the terms matter. Lambda's pricing page listed H100 SXM rates of $3.99 per GPU-hour for an eight-GPU instance and $4.29 for a one-GPU instance, before applicable taxes. Those are posted prices for specific products. The $2 in the model is a scenario for realized proceeds after discounts and credits per billable hour. It is deliberately separate from Lambda's posted prices. [Lambda public GPU instance pricing](https://lambda.ai/instances)

## The equation

Allocate the accelerator, host and initial fabric cost to each GPU. Convert that investment into an annual capital charge using the deployment's economic life and cost of capital. Add annual fixed expenses and the baseline electricity cost. Finally, add the incremental energy cost as the fleet works.

```text
capital charge = installed cost × r / (1 − (1 + r)^(−life))
baseline power cost = idle IT kW × PUE × $/kWh × calendar hours
variable cost per billable hour = (load IT kW − idle IT kW) × PUE × $/kWh
annual fixed cost = capital charge + fixed operations + baseline power cost

break-even rate = annual fixed cost / (8,760 × billable fraction)
                  + variable cost per billable hour
break-even billable fraction = annual fixed cost
                               / (8,760 × (realized rate − variable cost))
```

The annual capital charge is the cash-flow equivalent of recovering the upfront investment at the assumed return. At a zero discount rate it becomes cost divided by life. There is no resale value in this model. The fixed operating line includes staffing, maintenance, space and recurring network costs allocated per GPU. A site budget that charges for power demand or reserved utility capacity can include those charges in that line. PUE is facility electricity divided by IT electricity over a matching period. In this scenario it allocates the cooling and other facility overhead on top of IT load.

## What the inputs buy

| Base case assumption | Amount per GPU |
| --- | ---: |
| Installed cost, including allocated host and fabric | $36,000 |
| Economic life and annual cost of capital | 4 years, 10% |
| Annual fixed operations | $4,800 |
| Allocated idle / loaded IT draw | 0.25 / 0.90 kW |
| PUE and energy tariff | 1.25, $0.09/kWh |
| Realized rate and billable fraction | $2.00/h, 90% |

NVIDIA lists a configurable maximum TDP up to 700 W for the H100 SXM. That is a device specification. The 0.90 kW here is a synthetic loaded allocation for a GPU plus its share of IT equipment. The energy equation treats every billable hour as loaded and every other hour as idle. A fleet running internal jobs should account for their energy use separately. [NVIDIA H100 specifications](https://www.nvidia.com/en-us/data-center/h100/)

The $36,000 investment requires an annual capital charge of about $11,357. Fixed operations and idle electricity bring annual fixed cost to $16,403. Each loaded hour adds about 7.3 cents in electricity. At 90% billable, 7,884 hours earn $15,768 and cost approximately $16,980, including the capital charge. This is an annual economic result before tax. Monthly cash balances will follow the actual payment schedules.

| Realized rate | Share of calendar hours needed |
| ---: | ---: |
| $1.50 | 131.2%, infeasible |
| $2.00 | 97.2% |
| $2.50 | 77.2% |
| $3.00 | 64.0% |
| $4.00 | 47.7% |

That table explains why a cheaper power contract can matter less than a few lost customers. At 90% billable, lowering energy prices from 9 to 7 cents per kWh saves about $183 a year. A drop from 90% to 80% billable costs about $1,688 a year at $2/h after the associated energy savings. Change the location, tariff, model or cooling system and the comparison can change with it.

For an actual deployment, build the inputs from invoices, metered site power, availability records and net realized billing. Use the result to price a specific contract. A utilization screenshot has no space for the terms that decide whether you'd sign it.
