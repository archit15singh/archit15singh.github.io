#!/usr/bin/env python3
"""Render ten figures for the series with Matplotlib and Pillow.

Run beside the published CSVs and physical-infrastructure-models.py.
The chart inputs are from the articles and their cited disclosures.
"""

import csv
from collections import defaultdict
from pathlib import Path
from runpy import run_path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, PercentFormatter

HERE = Path(__file__).resolve().parent
PAPER = "#f8faf7"
INK = "#13252c"
MUTED = "#425e65"
GRID = "#d5e0db"
TEAL = "#146c61"
BLUE = "#2e5890"
RUST = "#983e35"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "text.color": INK,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.facecolor": PAPER,
    "figure.facecolor": PAPER,
    "savefig.facecolor": PAPER,
    "axes.formatter.use_mathtext": False,
    "text.parse_math": False,
})


def sheet(title, subtitle, height=4.0):
    fig = plt.figure(figsize=(7.4, height))
    fig.text(0.055, 0.94, title, fontsize=21, weight="bold", va="top")
    fig.text(0.055, 0.94 - 0.37 / height, subtitle, color=MUTED, fontsize=12, va="top")
    return fig


def axes(fig, bounds):
    ax = fig.add_axes(bounds)
    ax.tick_params(length=0, pad=7)
    ax.set_axisbelow(True)
    return ax


def save(fig, slug):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for label in fig.findobj(matplotlib.text.Text):
        if not label.get_visible() or not label.get_text():
            continue
        bbox = label.get_window_extent(renderer=renderer)
        if bbox.x0 < 0 or bbox.x1 > fig.bbox.width or bbox.y0 < 0 or bbox.y1 > fig.bbox.height:
            raise ValueError(f"{slug}: label outside figure: {label.get_text()!r}")
    fig.savefig(HERE / f"{slug}.webp", dpi=160, pil_kwargs={"lossless": True, "method": 6})
    plt.close(fig)


def read_csv(name):
    with (HERE / name).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def hbm_allocation():
    fig = sheet("HBM uses 22% of wafers for 9% of bits",
                "TrendForce projection for the top three DRAM suppliers, end of 2026", 3.55)
    ax = axes(fig, [0.25, 0.2, 0.69, 0.5])
    shares = np.array([22, 9])
    rows = [1, 0]
    ax.barh(rows, shares, color=TEAL, height=0.42)
    ax.barh(rows, 100 - shares, left=shares, color=GRID, height=0.42)
    for y, share in zip(rows, shares):
        ax.text(share / 2, y, f"{share}%", ha="center", va="center", color="white", weight="bold")
        ax.text((share + 100) / 2, y, f"{100 - share}% conventional DRAM", ha="center", va="center")
    ax.set(xlim=(0, 100), ylim=(-0.49, 1.49), yticks=rows,
           yticklabels=["Wafer input", "Bit supply"], xticks=[0, 25, 50, 75, 100])
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    fig.text(0.25, 0.085, "Teal = high-bandwidth memory (HBM)", color=TEAL, weight="bold")
    save(fig, "hbm-wafer-and-bit-shares")


def retail_quotes():
    fig = sheet("The latest two quotes were out of stock",
                "Four U.S. listings for the same Corsair 32 GB DDR5 kit", 4.0)
    ax = axes(fig, [0.32, 0.18, 0.61, 0.57])
    data = read_csv("retail-ddr5-observations.csv")
    rows = np.arange(3, -1, -1)
    labels = ["Corsair direct\nSep. snapshot", "Walmart marketplace\nEarly Nov. snapshot",
              "Newegg direct\nNov. 20", "Corsair direct\nNov. 20"]
    for y, record in zip(rows, data):
        price = float(record["price_usd"])
        out = record["stock_signal"] == "Out of stock"
        color = RUST if out else TEAL
        ax.scatter(price, y, s=86, color=PAPER if out else color, edgecolor=color, linewidth=2, zorder=3)
        ax.text(price + 6, y, f"${price:,.2f}", va="center", color=color, weight="bold")
    ax.set(xlim=(505, 693), ylim=(-0.55, 3.55), yticks=rows, yticklabels=labels, xticks=[520, 560, 600, 640, 680])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:g}"))
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    fig.text(0.32, 0.07, "Filled = in stock or add to cart     Open = out of stock", color=MUTED, fontsize=11)
    save(fig, "ddr5-stock-and-posted-prices")


def break_even():
    fig = sheet("At $2/hour, break-even takes 97%",
                "Illustrative model · share of calendar hours to break even", 4.35)
    ax = axes(fig, [0.14, 0.18, 0.79, 0.59])
    hours = 8760
    rate = 0.10
    fixed = 36000 * rate / (1 - (1 + rate) ** -4) + 4800 + hours * 0.25 * 1.25 * 0.09
    variable = (0.90 - 0.25) * 1.25 * 0.09
    price = np.linspace(1.43, 4.15, 140)
    def share(price):
        return 100 * fixed / (hours * (price - variable))
    ax.axhspan(100, 145, color="#f3e5e1")
    ax.axhline(100, color=RUST, linestyle="--", linewidth=1.2)
    ax.plot(price, share(price), color=TEAL, linewidth=2.5)
    for price_tick, offset in [(1.5, (8, 3)), (2, (9, 6)), (2.5, (8, 6)), (3, (7, 6)), (4, (-12, 9))]:
        y = share(price_tick)
        ax.scatter(price_tick, y, color=TEAL, s=34, zorder=4)
        ax.annotate(f"{y:.1f}%", (price_tick,y), xytext=offset, textcoords="offset points",
                    ha="right" if price_tick == 4 else "left", color=TEAL, weight="bold", fontsize=12)
    ax.text(4.10, 104, "Above 100% is infeasible", ha="right", color=RUST, fontsize=11, weight="bold")
    ax.set(xlim=(1.4, 4.18), ylim=(40, 145), xticks=[1.5, 2, 2.5, 3, 3.5, 4],
           yticks=[40, 60, 80, 100, 120, 140], xlabel="Realized rate per billed GPU-hour")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:.2f}"))
    ax.yaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    save(fig, "gpu-break-even-curve")


def token_speed(model):
    fig = sheet("One rack, three throughput numbers",
                "Published DeepSeek-R1 runs · one GB200 NVL72 rack", 4.35)
    names = list(model["TOKEN_RATES"])
    rows = np.arange(2, -1, -1)
    rates = [model["TOKEN_RATES"][name] / 1000 for name in names]
    cost = [model["cost_per_million"](216, rate * 1000) for rate in rates]
    left = axes(fig, [0.21, 0.17, 0.35, 0.49])
    right = axes(fig, [0.65, 0.17, 0.28, 0.49])
    fig.text(0.21, 0.70, "Output tokens/sec", fontsize=13, weight="bold")
    fig.text(0.65, 0.70, "Cost / million*", fontsize=13, weight="bold")
    left.barh(rows, rates, color=TEAL, height=0.35)
    right.barh(rows, cost, color=BLUE, height=0.35)
    for y, output, usd in zip(rows, rates, cost):
        left.text(output + 12, y, f"{output:,.0f}k", va="center", weight="bold", fontsize=12)
        right.text(usd + 0.006, y, f"${usd:.3f}", va="center", weight="bold", fontsize=12)
    left.set(xlim=(0, 650), ylim=(-0.55, 2.55), yticks=rows, yticklabels=names, xticks=[])
    right.set(xlim=(0, 0.335), ylim=(-0.55, 2.55), yticks=[], xticks=[])
    fig.text(0.055, 0.068, "*Modeled at $216/rack-hour, fully loaded and 100% usable output.",
             color=MUTED, fontsize=11)
    save(fig, "mlperf-throughput-and-token-cost")


def deployment_timeline(model):
    fig = sheet("The grid sets the first billing date",
                "Baseline schedule for one hypothetical site", 4.85)
    ax = axes(fig, [0.315, 0.15, 0.62, 0.63])
    finish, paths = model["deployment_schedule"]({})
    critical = paths[0]
    names = ["financing", "grid", "GPU delivery", "fabric delivery", "building + cooling",
             "energization", "commissioning", "contractual acceptance"]
    labels = ["Financing", "Grid connection", "GPU delivery", "Fabric delivery", "Building + cooling",
              "Energization", "Commissioning", "Customer acceptance"]
    rows = np.arange(len(names) - 1, -1, -1)
    for y, task in zip(rows, names):
        duration, _ = model["TASKS"][task]
        month = finish[task]
        color = TEAL if task in critical else BLUE
        if duration:
            ax.barh(y, duration, left=month-duration, color=color, height=0.42)
        else:
            ax.scatter(month, y, marker="D", color=color, s=42, zorder=4)
        ax.text(month + 0.55, y, str(month), va="center", color=color, weight="bold", fontsize=12)
    ax.set(xlim=(0, 27.8), ylim=(-0.58, 7.58), yticks=rows, yticklabels=labels,
           xticks=[0, 5, 10, 15, 20, 25])
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    fig.text(0.315, 0.045, "Project months · teal = critical path · ◇ = milestone", color=MUTED, fontsize=11)
    save(fig, "cluster-commissioning-timeline")


def power_queue(model):
    fig = sheet("One power cap, three queue outcomes",
                "7.2 MW limit · simulated requests meeting a two-minute deadline", 4.15)
    ax = axes(fig, [0.34, 0.18, 0.59, 0.57])
    policies = [model["Allocation"](8,0,8), model["Allocation"](0,12,8), model["Allocation"](0,12,6)]
    labels = ["8 full-power groups\n80 req/min total", "12 capped groups\n96 req/min total",
              "12 capped groups\n72 req/min total"]
    rows = [2,1,0]
    shares = [100 * model["simulate_queue"](item, 2)[1] for item in policies]
    ax.barh(rows, shares, height=0.45, color=[BLUE, TEAL, RUST])
    for y, share in zip(rows, shares):
        ax.text(share + 2, y, f"{share:g}%" if share == 100 else f"{share:.1f}%",
                va="center", weight="bold", fontsize=14)
    ax.set(xlim=(0, 117), ylim=(-0.55, 2.55), yticks=rows, yticklabels=labels, xticks=[0, 25, 50, 75, 100])
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    fig.text(0.055, 0.065, "The last two rows vary how much throughput a capped group retains.", color=MUTED, fontsize=11)
    save(fig, "power-cap-deadline-sensitivity")


def waterfall(slug, title, subtitle, labels, starting, changes, ylim, ticklabels, precision=1):
    fig = sheet(title, subtitle, 4.35)
    ax = axes(fig, [0.12, 0.22, 0.82, 0.53])
    starts = [0]
    values = [starting, *changes, starting + sum(changes)]
    level = starting
    for change in changes:
        starts.append(level)
        level += change
    starts.append(0)
    width = 0.56
    for index, (before, change) in enumerate(zip(starts, values)):
        total = index in (0, len(values) - 1)
        color = BLUE if total else TEAL if change > 0 else RUST
        after = before + change
        ax.bar(index, abs(change), bottom=min(before, after), width=width, color=color, zorder=3)
        if index < len(values) - 1:
            ax.hlines(after, index + width / 2, index + 1 - width / 2, colors=MUTED,
                      linewidth=0.85, linestyles="--")
        sign = "−" if change < 0 else "" if total else "+"
        annotate_at = min(before, after) if change < 0 else max(before, after)
        label = f"{sign}{abs(change):,.{precision}f}"
        if change < 0 and not total and abs(change) > 0.25 * (ylim[1] - ylim[0]):
            ax.text(index, (before + after) / 2, label, ha="center", va="center",
                    weight="bold", color="white", fontsize=13)
        else:
            ax.annotate(label, (index, annotate_at),
                        xytext=(0, -8 if change < 0 else 8), textcoords="offset points",
                        va="top" if change < 0 else "bottom", ha="center", weight="bold", color=color, fontsize=13)
    ax.set(xlim=(-0.48, len(values)-0.52), ylim=ylim, xticks=range(len(values)),
           xticklabels=labels, yticks=ticklabels)
    ax.tick_params(axis="x", labelsize=11)
    ax.axhline(0, color=MUTED, linewidth=0.8)
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    save(fig, slug)


def finance_figures():
    quarters = defaultdict(lambda: [0,0])
    for row in read_csv("capex-cash-flow.csv"):
        totals = quarters[row["quarter_end"]]
        totals[0] += int(row["operating_cash_flow_usd_m"])
        totals[1] += int(row["cash_ppe_usd_m"])
    (prev_cash, prev_spend), (cash, spend) = [quarters[key] for key in sorted(quarters)]
    waterfall("hyperscaler-cash-spend-bridge", "Equipment spending ate the cash gain",
              "Combined Microsoft, Alphabet and Meta · September quarters · USD billions",
              ["Cash left\n2025", "More operating\ncash", "More equipment\nspending", "Cash left\n2026"],
              (prev_cash - prev_spend) / 1000, [(cash-prev_cash)/1000, -(spend-prev_spend)/1000],
              (-6, 84), [0,20,40,60,80])
    # CoreWeave Q3 2026 statement, rounded millions as disclosed in the article.
    waterfall("coreweave-net-loss-bridge", "Interest erased operating profit",
              "CoreWeave · Q3 2026 · USD millions",
              ["Operating\nincome","Net\ninterest","Other\nincome","Income\ntax","Net\nloss"],
              207, [-846, 13, -83], (-840, 340), [-800,-600,-400,-200,0,200], precision=0)


def survey():
    fig = sheet("AI use was more common at larger firms",
                "U.S. Census working paper · November 2025 to January 2026", 3.55)
    ax = axes(fig, [0.30, 0.20, 0.62, 0.46])
    rates = [18,32]
    rows = [1,0]
    ax.barh(rows,rates,color=[TEAL,BLUE],height=0.42)
    for y, value in zip(rows, rates):
        ax.text(value+0.9,y,f"{value}%", va="center", weight="bold", fontsize=16)
    ax.set(xlim=(0,42), ylim=(-0.5,1.5), yticks=rows,
           yticklabels=["Share of firms", "Share of employment"], xticks=[0,10,20,30,40])
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    fig.text(0.055, 0.075, "Employment share counts workers at firms reporting AI use.", color=MUTED, fontsize=11)
    save(fig, "ai-adoption-two-denominators")


def scorecard():
    fig = sheet("Five predictions to check in 2027",
                "2026 baselines and thresholds fixed on November 20, 2026", 4.75)
    ax = fig.add_axes([0.055, 0.11, 0.89, 0.66])
    ax.set_axis_off()
    numbers = read_csv("prediction-scorecard.csv")
    metric = ["Anthropic compute / revenue", "CoreWeave active / contracted power",
              "CoreWeave operating income less interest", "Digital Realty signing-to-start lag",
              "NVIDIA Data Center revenue"]
    unit = {"percent":"%", "USD million":"M", "months":" mo", "USD billion":"B"}

    def fmt(value, units):
        if units.startswith("USD"):
            value = f"−${value[1:]}" if value.startswith("-") else f"${value}"
        return value + unit[units]

    ax.text(0.015,0.95,"Metric", color=MUTED, weight="bold")
    ax.text(0.68,0.95,"Baseline", ha="center", color=MUTED, weight="bold")
    ax.text(0.89,0.95,"2027 threshold", ha="center", color=MUTED, weight="bold")
    for idx,(label,row) in enumerate(zip(metric,numbers)):
        y = 0.80 - idx * 0.168
        ax.axhline(y-0.079, color=GRID, linewidth=0.8)
        raw = row["baseline"].replace("roughly ", "~")
        operator = row["operator"].replace(">=", "≥")
        ax.text(0.015,y,label, va="center", fontsize=12)
        ax.text(0.68,y,fmt(raw,row["unit"]), va="center", ha="center", weight="bold")
        ax.text(0.89,y,operator + " " + fmt(row["target"],row["unit"]), va="center", ha="center",
                color=TEAL, weight="bold")
    fig.text(0.055, 0.054, "Score against comparable filings by December 31, 2027.", color=MUTED, fontsize=11)
    save(fig, "ai-boom-prediction-scorecard")


def main():
    model = run_path(str(HERE / "physical-infrastructure-models.py"))
    hbm_allocation()
    retail_quotes()
    break_even()
    token_speed(model)
    deployment_timeline(model)
    power_queue(model)
    finance_figures()
    survey()
    scorecard()


if __name__ == "__main__":
    main()
