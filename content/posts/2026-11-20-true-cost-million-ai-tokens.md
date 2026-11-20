---
title: "The true cost of serving one million AI tokens"
description: "Three public DeepSeek-R1 benchmark runs on the same rack show why a token cost estimate needs a latency target and an occupancy assumption."
date: 2026-11-20T09:03:00+05:30
tags: ["AI Infrastructure", "inference", "performance engineering"]
series: ["The AI Infrastructure Reality Check"]
categories: [Engineering]
cover:
  image: "/images/uploads/ai-infrastructure-engineering.svg"
  alt: "Dependencies that bring a GPU cluster into service."
  hidden: false
format: "Technical note"
---

*Part of [The AI Infrastructure Reality Check](/ai-infrastructure-reality-check/).*

The same GB200 rack posted 523,790 output tokens per second in an offline DeepSeek-R1 benchmark and 240,274 in an interactive benchmark. At the same assumed hourly cost, a million output tokens would cost 2.18 times as much in the second run. That difference appears before a quiet hour, a retry, or any extra idle capacity for a traffic spike. [MLPerf Inference v6.1, NVIDIA DeepSeek-R1 submission](https://github.com/mlcommons/inference_results_v6.1/tree/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1)

## A rack with three throughput numbers

The performance logs come from one submitter, system and model in MLCommons' published repository. All three runs are marked valid. Offline measures bulk processing, while Server and Interactive use online request schedules and latency requirements. Interactive has a tighter time-per-output-token limit. Settings and serving techniques can differ across scenarios, so this is a comparison of submitted runs. The measured differences reflect the full serving configurations.

| Scenario | Output tokens/s, rack-wide | p99 time to first token | p99 time per output token |
|---|---:|---:|---:|
| [Offline](https://github.com/mlcommons/inference_results_v6.1/blob/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1/Offline/performance/run_1/mlperf_log_summary.txt) | 523,790 | N/A | N/A |
| [Server](https://github.com/mlcommons/inference_results_v6.1/blob/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1/Server/performance/run_1/mlperf_log_summary.txt) | 395,940 | 869 ms | 65.8 ms |
| [Interactive](https://github.com/mlcommons/inference_results_v6.1/blob/6623c6c8bac460c46a8768ac261bc0889c9c7f13/closed/NVIDIA/results/GB200-NVL72_GB200-186GB_aarch64x72_TRT/deepseek-r1/Interactive/performance/run_1/mlperf_log_summary.txt) | 240,274 | 527 ms | 14.6 ms |

A rack-wide number adds the output from concurrent requests. An individual user experiences the delay before the first token and the pace of tokens after that. The interactive run trades aggregate throughput for a faster stream in the published measurements.

## Follow one request through the machine

Prefill processes the prompt and builds its key-value (KV) cache. Decode then generates tokens sequentially for that request and uses the cached keys and values for attention. Continuous batching puts work from multiple requests together. It gives the hardware more work per step, but a large prefill or a more crowded batch can change latency for requests already decoding. DistServe's OSDI paper measured the interference and moved prefill and decode onto separate GPU pools, at the cost of moving the KV state between them. The same design that removes a scheduling conflict now needs network bandwidth. [DistServe, OSDI 2024](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)

The cache also decides how large a batch can fit. Take an illustrative transformer with 80 layers, eight KV heads per layer, head dimension 128 and two bytes per value. Keys and values together occupy 320 KiB per cached token across the model, or 2.5 GiB for 8,192 cached tokens per sequence before allocator overhead. Real engines can shard, compress or share that state. The authors of PagedAttention reported two to four times the throughput of their comparison systems at similar latency in their 2023 experiments. Those gains show what efficient allocation can do under the tested workloads. A newer engine might already have removed much of the waste. [PagedAttention and vLLM, SOSP 2023](https://arxiv.org/abs/2309.06180)

## Price the output you actually want to count

Suppose the all-in pool cost is $216 per provisioned hour, equivalent to $3 per GPU-hour across 72 GPUs. This is a rounded scenario input. A hosted deployment can start from its rental bill plus separately charged services. An owned rack needs an hourly share of hardware, facilities, power, networking and operations. The denominator is usable output tokens across the same provisioned hour.

```text
USD per million usable output tokens =
    hourly pool cost * 1,000,000
    / (3,600 * reference output tokens/second * realized throughput share * usable-token share)
```

Under full benchmark throughput and a 100% usable-token share, the model returns $0.115 for Offline, $0.152 for Server, and $0.250 for Interactive. With Interactive as the reference and a production scenario that realizes 55% of that throughput over a provisioned hour, of which 90% meets the service target, the result is **$0.504 per million usable output tokens**. The 55% represents a throughput ratio across time. GPU activity readings would be a poor substitute. The 90% is a share of tokens belonging to qualifying requests, which can differ from the share of requests that qualify.

The figures are serving scenarios, with prompt cost already embedded in each benchmark's workload mix and API pricing left out of the calculation. Production prompt lengths, prefix reuse, reasoning output, cancellations and retries can move both factors. When retries consume capacity, charge that time to the pool and count the accepted output once.

[Download the model](/downloads/ai-infrastructure-reality-check/physical-infrastructure-models.py) and run `python3 physical-infrastructure-models.py tokens` to reproduce the table. Use `--hourly-cost`, `--fill` and `--usable` to test your inputs. For a real service, replay a trace with its prompt and output length distribution, then divide the pool's cost by the output that arrived within its service target. A million tokens only becomes a useful unit once you know when the user received them.
