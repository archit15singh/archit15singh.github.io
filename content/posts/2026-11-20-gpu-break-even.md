---
title: "GPU economics from break-even to cost per token"
description: "Use a break-even calculator, a hardware-life model and three MLPerf runs to price the work a GPU can deliver."
date: 2026-11-20T09:14:00+05:30
tags: [AI Infrastructure, GPU Economics, Modeling]
series: [The AI Infrastructure Reality Check]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-economics.svg"
  alt: "The inputs to fleet economics, from upfront cost to realized returns."
  hidden: false
format: "Technical note"
aliases:
  - "/posts/2026-11-20-gpu-economic-life/"
  - "/posts/2026-11-20-true-cost-million-ai-tokens/"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

A GPU can sell 90% of the hours in a year and still come up $1,212 short. In the deployment below, the operator realizes $2 an hour, pays for a share of the server and network, and expects to replace the hardware after four years. Push the rental rate to $2.50 and the same machine needs to sell about 77% of the year. Open the [GPU break-even calculator](/downloads/ai-infrastructure-reality-check/gpu-break-even.html) to change any of those inputs.

## Price the billable hour

A billing record tells you what the customer owes. GPU telemetry tells you how much work the device did during the sample. The two can move independently. An eight-GPU reservation can be fully billable while a customer's code runs on six GPUs. A week spent testing the provider's software can keep all eight busy without yielding a billable hour. The denominator I use is 8,760 calendar hours per GPU. Every outage, empty slot or maintenance hour reduces the fraction that can be sold.

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

## Put a price on years four and five

The physical life ends when the machine stops being serviceable. The accounting life is the period over which management expects to depreciate the asset, subject to its accounting policies and estimates. CoreWeave's 2025 annual report lists six years for technology equipment. Meta extended the estimated useful life of most servers and network assets to 5.5 years in January 2025. Those are policies for asset classes that include more than one GPU generation and, in Meta's case, network equipment. [CoreWeave 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) · [Meta 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm)

The four-year break-even calculation holds the hourly rate steady. If a new generation pushes the rental rate down, spread the cash flows across years and test how much the later years are worth. This second scenario uses a different equipment budget and a starting rate of $3.20.

Consider an illustrative GPU-equivalent slice of a deployment. It costs $35,000 up front, including its share of server and network hardware. The year-one realized rate is $3.20 per billable GPU-hour. At 72% of 8,760 calendar hours, it bills 6,307.2 hours a year. Annual operating cash cost is $4,200, covering the modeled allocation of power, hosting, maintenance and labor. All rates and costs are assumed. The model discounts year-end cash flows at 10%, with zero salvage value and no taxes, working-capital changes or financing cash flows.

```text
rate in year t = $3.20 × (1 − annual rate decline)^(t − 1)
year t cash = 6,307.2 × rate in year t − $4,200
NPV through year T = −$35,000 + sum of year t cash / 1.10^t
```

| Annual decline in realized rate | Year 5 cash | 3-year NPV | 5-year NPV |
| --- | ---: | ---: | ---: |
| 0% | $15,983 | +$4,747 | +$25,588 |
| 15% | $6,336 | −$1,963 | +$7,569 |
| 30% | $646 | −$7,990 | −$5,729 |

![Three cash-flow curves for the modeled GPU. At a 15% annual price decline, discounted cash turns positive in year four. At 30%, it remains negative through year five.](/downloads/ai-infrastructure-reality-check/gpu-economic-life.png)

Year one is identical across all three rows. At a 15% decline, years four and five rescue the economics. At a 30% decline, the GPU is still generating a little operating cash in year five and still falls $5,729 short in present-value terms. At that steeper decline, a five-year project needs a starting rate of about $3.61 per billable hour to break even under the same assumptions.

The model holds billable hours constant while the price falls. In practice, an older fleet can lose both at once if a customer leaves. Alternatively, a lower price can fill previously idle capacity. Neither relationship is estimated here. The table is a sensitivity test. [Run the Python model](/downloads/ai-infrastructure-reality-check/gpu-economic-life.py) · [Download the default results](/downloads/ai-infrastructure-reality-check/gpu-economic-life.csv)

## Convert rack-hours to useful tokens

The same GB200 rack posted 523,790 output tokens per second in an offline DeepSeek-R1 benchmark and 240,274 in an interactive benchmark. At the same assumed hourly cost, a million output tokens would cost 2.18 times as much in the second run. That difference appears before a quiet hour, a retry, or any extra idle capacity for a traffic spike. [MLPerf Inference v6.1, NVIDIA DeepSeek-R1 submission](https://github.com/mlcommons/inference_results_v6.1/tree/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1)

The performance logs come from one submitter, system and model in MLCommons' published repository. All three runs are marked valid. Offline measures bulk processing, while Server and Interactive use online request schedules and latency requirements. Interactive has a tighter time-per-output-token limit. Settings and serving techniques can differ across scenarios, so this is a comparison of submitted runs. The measured differences reflect the full serving configurations.

| Scenario | Output tokens/s, rack-wide | p99 time to first token | p99 time per output token |
|---|---:|---:|---:|
| [Offline](https://github.com/mlcommons/inference_results_v6.1/blob/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1/Offline/performance/run_1/mlperf_log_summary.txt) | 523,790 | N/A | N/A |
| [Server](https://github.com/mlcommons/inference_results_v6.1/blob/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1/Server/performance/run_1/mlperf_log_summary.txt) | 395,940 | 869 ms | 65.8 ms |
| [Interactive](https://github.com/mlcommons/inference_results_v6.1/blob/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1/Interactive/performance/run_1/mlperf_log_summary.txt) | 240,274 | 527 ms | 14.6 ms |

The hourly model prices the capacity you provision. A rack-wide throughput number adds the output from concurrent requests. An individual user experiences the delay before the first token and the pace of tokens after that. The interactive run trades aggregate throughput for a faster stream in the published measurements.

Prefill processes the prompt and builds its key-value (KV) cache. Decode then generates tokens sequentially for that request and uses the cached keys and values for attention. Continuous batching puts work from multiple requests together. It gives the hardware more work per step, but a large prefill or a more crowded batch can change latency for requests already decoding. DistServe's OSDI paper measured the interference and moved prefill and decode onto separate GPU pools, at the cost of moving the KV state between them. The same design that removes a scheduling conflict now needs network bandwidth. [DistServe, OSDI 2024](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)

Suppose the all-in pool cost is $216 per provisioned hour, equivalent to $3 per GPU-hour across 72 GPUs. This is a rounded scenario input. A hosted deployment can start from its rental bill plus separately charged services. An owned rack needs an hourly share of hardware, facilities, power, networking and operations. The denominator is usable output tokens across the same provisioned hour.

```text
USD per million usable output tokens =
    hourly pool cost * 1,000,000
    / (3,600 * reference output tokens/second * realized throughput share * usable-token share)
```

Under full benchmark throughput and a 100% usable-token share, the model returns $0.115 for Offline, $0.152 for Server, and $0.250 for Interactive. With Interactive as the reference and a production scenario that realizes 55% of that throughput over a provisioned hour, of which 90% meets the service target, the result is **$0.504 per million usable output tokens**. The 55% represents a throughput ratio across time. GPU activity readings would be a poor substitute. The 90% is a share of tokens belonging to qualifying requests, which can differ from the share of requests that qualify.

The figures are serving scenarios, with prompt cost already embedded in each benchmark's workload mix and API pricing left out of the calculation. Production prompt lengths, prefix reuse, reasoning output, cancellations and retries can move both factors. When retries consume capacity, charge that time to the pool and count the accepted output once.

[Download the model](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) and run `python3 physical-infrastructure-models.py tokens` to reproduce the table. Use `--hourly-cost`, `--fill` and `--usable` to test your inputs. For a real service, replay a trace with its prompt and output length distribution, then divide the pool's cost by the output that arrived within its service target. A million tokens only becomes a useful unit once you know when the user received them.
