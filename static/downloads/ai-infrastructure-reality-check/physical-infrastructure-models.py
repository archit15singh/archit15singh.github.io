#!/usr/bin/env python3
"""Reproduce the infrastructure scenarios in The AI Infrastructure Reality Check."""

import argparse
import math
from collections import deque
from dataclasses import dataclass

# Task duration in months and predecessor tasks. Durations are illustrative.
TASKS = {
    "financing": (2, ()),
    "grid": (18, ("financing",)),
    "switchgear": (12, ("financing",)),
    "permits": (4, ("financing",)),
    "building + cooling": (13, ("permits",)),
    "GPU delivery": (10, ("financing",)),
    "fabric delivery": (14, ("financing",)),
    "customer readiness": (16, ("financing",)),
    "energization": (0, ("grid", "switchgear")),
    "commissioning": (
        3,
        ("energization", "building + cooling", "GPU delivery", "fabric delivery"),
    ),
    "contractual acceptance": (2, ("commissioning", "customer readiness")),
}


def deployment_schedule(overrides):
    finish = {}
    paths = {}
    for task, (duration, predecessors) in TASKS.items():
        start = max((finish[parent] for parent in predecessors), default=0)
        finish[task] = start + overrides.get(task, duration)
        paths[task] = [
            path + (task,)
            for parent in predecessors
            if finish[parent] == start
            for path in paths[parent]
        ] or [(task,)]
    return finish, paths["contractual acceptance"]


def show_deployment(arguments):
    if arguments.months is not None:
        scenarios = [("Custom", {arguments.task: arguments.months})]
    else:
        scenarios = [
            ("Baseline", {}),
            ("GPU delivery four months faster", {"GPU delivery": 6}),
            ("Grid four months faster", {"grid": 14}),
            ("Grid and cooling four months faster", {"grid": 14, "building + cooling": 9}),
            ("Fabric five months later", {"fabric delivery": 19}),
        ]
    for name, overrides in scenarios:
        finish, paths = deployment_schedule(overrides)
        print(f"{name}: first billable capacity in month {finish['contractual acceptance']}")
        print("  Milestones:", ", ".join(f"{task} {month}" for task, month in finish.items()))
        for path in paths:
            print("  Critical path:", " -> ".join(path))


# Verified published rates in NVIDIA's DeepSeek-R1 MLPerf v6.1 submission
# for a GB200 NVL72. The dollar and off-peak inputs below are hypothetical.
TOKEN_RATES = {
    "Offline": 523790,
    "Server": 395940.14,
    "Interactive": 240273.74,
}


def cost_per_million(hourly_cost, tokens_per_second, fill=1.0, usable=1.0):
    return hourly_cost * 1_000_000 / (3_600 * tokens_per_second * fill * usable)


def show_tokens(arguments):
    print("Scenario | benchmark output tokens/s | assumed fill | assumed usable | modeled USD/M")
    for scenario, tokens_per_second in TOKEN_RATES.items():
        cost = cost_per_million(arguments.hourly_cost, tokens_per_second)
        print(f"{scenario} | {tokens_per_second:,.2f} | 100% | 100% | {cost:.3f}")
    tokens_per_second = TOKEN_RATES["Interactive"]
    cost = cost_per_million(
        arguments.hourly_cost, tokens_per_second, arguments.fill, arguments.usable
    )
    print(
        f"Interactive (production scenario) | {tokens_per_second:,.2f} | "
        f"{arguments.fill:.0%} | {arguments.usable:.0%} | {cost:.3f}"
    )
    print(f"Offline / Interactive benchmark throughput: {TOKEN_RATES['Offline'] / tokens_per_second:.3f}")


# Every capacity is in thousands of completed requests/hour for one workload mix.
CAPACITIES = {"accelerators": 72, "power": 80, "cooling": 100, "fabric": 90, "demand": 92}
CHANGES = [
    ("Current", {}),
    ("More accelerators", {"accelerators": 120}),
    ("More firm power", {"power": 110}),
    ("Fabric upgrade", {"fabric": 115}),
    ("Demand grows", {"demand": 105}),
    ("Demand drops", {"demand": 70}),
]


def show_bottlenecks(_arguments):
    capacities = CAPACITIES.copy()
    print("Change | accelerators | power | cooling | fabric | demand | output | limiter")
    for name, changes in CHANGES:
        capacities.update(changes)
        output = min(capacities.values())
        limiters = ", ".join(kind for kind, limit in capacities.items() if limit == output)
        limits = " | ".join(str(value) for value in capacities.values())
        print(f"{name} | {limits} | {output} | {limiters}")


# Rack-group and facility parameters are hypothetical. One slot is one minute.
GROUP_COUNT = 12
FIXED_FACILITY_KW = 1600
FULL_GROUP_KW = 700
CAPPED_GROUP_KW = 450
FULL_REQUESTS_PER_SLOT = 10
NORMAL_ARRIVALS = 75
BURST_ARRIVALS = 100
ARRIVALS = [NORMAL_ARRIVALS] * 10 + [BURST_ARRIVALS] * 10 + [NORMAL_ARRIVALS] * 10


@dataclass(frozen=True)
class Allocation:
    full: int
    capped: int
    capped_rate: int

    @property
    def kilowatts(self):
        return FIXED_FACILITY_KW + FULL_GROUP_KW * self.full + CAPPED_GROUP_KW * self.capped

    @property
    def rate(self):
        return FULL_REQUESTS_PER_SLOT * self.full + self.capped_rate * self.capped


def feasible_allocations(budget_kw, capped_rate):
    return [
        allocation
        for full in range(GROUP_COUNT + 1)
        for capped in range(GROUP_COUNT - full + 1)
        if (allocation := Allocation(full, capped, capped_rate)).kilowatts <= budget_kw
        and allocation.rate > 0
    ]


def simulate_queue(allocation, deadline):
    queue = deque()
    latencies = []
    peak_backlog = 0
    slot = 0
    completed_during_arrivals = 0
    while slot < len(ARRIVALS) or queue:
        if slot < len(ARRIVALS):
            queue.extend([slot] * ARRIVALS[slot])
        completions = min(len(queue), allocation.rate)
        for _ in range(completions):
            latencies.append(slot - queue.popleft() + 1)
        if slot < len(ARRIVALS):
            completed_during_arrivals += completions
        peak_backlog = max(peak_backlog, len(queue))
        slot += 1

    latencies.sort()
    p95 = latencies[math.ceil(0.95 * len(latencies)) - 1]
    on_time = sum(latency <= deadline for latency in latencies) / len(latencies)
    utilization = completed_during_arrivals / (allocation.rate * len(ARRIVALS))
    throughput = completed_during_arrivals / len(ARRIVALS)
    return p95, on_time, throughput, utilization, peak_backlog, slot - len(ARRIVALS)


def show_power(arguments):
    full_budget = feasible_allocations(10_000, arguments.capped_rate)
    tight_budget = feasible_allocations(arguments.budget_kw, arguments.capped_rate)
    full_only = [option for option in tight_budget if option.capped == 0]
    caps_only = [option for option in tight_budget if option.full == 0]
    scenarios = [
        ("10 MW, full-power only", max(full_budget, key=lambda x: x.full)),
        ("Reduced budget, full-power only", max(full_only, key=lambda x: x.full, default=None)),
        ("Reduced budget, capped only", max(caps_only, key=lambda x: x.capped, default=None)),
        ("Reduced budget, best mix", max(tight_budget, key=lambda x: (x.rate, -x.kilowatts))),
    ]
    print("Policy | full | capped | MW envelope | rated requests/min | effective requests/min | "
          "service-slot utilization | p95 minutes | on time | peak backlog | drain minutes")
    for name, allocation in scenarios:
        if allocation is None:
            print(f"{name} | infeasible")
            continue
        p95, on_time, throughput, utilization, backlog, drain = simulate_queue(
            allocation, arguments.deadline
        )
        print(
            f"{name} | {allocation.full} | {allocation.capped} | "
            f"{allocation.kilowatts / 1000:.2f} | {allocation.rate} | {throughput:.1f} | "
            f"{utilization:.1%} | {p95} | {on_time:.1%} | {backlog} | {drain}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    deployment = subparsers.add_parser("deployment", help="model first billable capacity")
    deployment.add_argument("--task", choices=TASKS)
    deployment.add_argument("--months", type=int)
    deployment.set_defaults(function=show_deployment)

    tokens = subparsers.add_parser("tokens", help="compute cost per usable million output tokens")
    tokens.add_argument("--hourly-cost", type=float, default=216)
    tokens.add_argument("--fill", type=float, default=0.55)
    tokens.add_argument("--usable", type=float, default=0.90)
    tokens.set_defaults(function=show_tokens)

    bottlenecks = subparsers.add_parser("bottlenecks", help="show changes in the limiting stage")
    bottlenecks.set_defaults(function=show_bottlenecks)

    power = subparsers.add_parser("power", help="model request queues under a site power budget")
    power.add_argument("--budget-kw", type=int, default=7_200)
    power.add_argument("--capped-rate", type=int, default=8)
    power.add_argument("--deadline", type=int, default=2)
    power.set_defaults(function=show_power)

    arguments = parser.parse_args()
    if arguments.command == "deployment":
        if (arguments.task is None) != (arguments.months is None):
            parser.error("--task and --months must be supplied together")
        if arguments.months is not None and arguments.months < 0:
            parser.error("--months must be nonnegative")
    if arguments.command == "tokens" and (
        not math.isfinite(arguments.hourly_cost)
        or arguments.hourly_cost < 0
        or not 0 < arguments.fill <= 1
        or not 0 < arguments.usable <= 1
    ):
        parser.error("--hourly-cost must be finite and nonnegative, --fill and --usable in (0, 1]")
    if arguments.command == "power" and (
        arguments.budget_kw < FIXED_FACILITY_KW + CAPPED_GROUP_KW
        or not 1 <= arguments.capped_rate <= FULL_REQUESTS_PER_SLOT
        or arguments.deadline < 1
    ):
        parser.error("budget must fit one capped group, capped rate must be 1–10, deadline positive")

    arguments.function(arguments)


if __name__ == "__main__":
    main()
