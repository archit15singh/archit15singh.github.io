"""Regenerate the finance article figures with Matplotlib and the adjacent CSVs."""
from collections import defaultdict
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
INK = "#13252c"
MUTED = "#48626c"
PAPER = "#f8faf7"
GRID = "#c9d8d5"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": INK,
    "axes.labelcolor": MUTED,
    **{f"axes.spines.{side}": False for side in ("top", "right", "bottom", "left")},
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "savefig.facecolor": PAPER,
})


def read_rows(filename):
    with (HERE / filename).open(newline="") as source:
        return list(csv.DictReader(source))


def format_axis(ax, prefix, suffix=""):
    ax.grid(axis="y", color=GRID, linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=8)
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda value, _: f"{'−' if value < 0 else ''}{prefix}{abs(value):g}{suffix}"
    ))
    ax.axhline(0, color=MUTED, linewidth=0.9)


def gpu_life_chart():
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    fig.subplots_adjust(left=0.13, right=0.88, bottom=0.16, top=0.77)
    fig.text(0.10, 0.90, "When does the GPU earn back its cost?", fontsize=19, weight="bold")
    fig.text(0.10, 0.835, "Illustrative cumulative discounted cash flow per GPU-equivalent",
             color=MUTED, fontsize=10)
    for row, color in zip(read_rows("gpu-economic-life.csv"), ("#116c65", "#2b5792", "#9d443a")):
        decline = float(row["annual_price_decline"])
        npv = -float(row["initial_capital_usd"])
        discount = float(row["discount_rate"])
        path = [npv / 1_000]
        for year in range(1, 6):
            npv += float(row[f"year_{year}_cash_usd"]) / (1 + discount) ** year
            path.append(npv / 1_000)
        ax.plot(range(6), path, color=color, linewidth=2.6, marker="o", markersize=4.6)
        ax.text(5.08, path[-1], f"{decline:.0%} decline", color=color, va="center", weight="bold")

    ax.set_xlim(-0.08, 5.6)
    ax.set_ylim(-38, 30)
    ax.set_xticks(range(6), ["Purchase", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"])
    ax.set_yticks(range(-30, 31, 10))
    format_axis(ax, "$", "k")
    fig.savefig(HERE / "gpu-economic-life.png", dpi=180)
    plt.close(fig)


def capex_chart():
    figures = defaultdict(list)
    for row in read_rows("capex-cash-flow.csv"):
        figures[row["company"]].append(tuple(
            int(row[column]) / 1_000 for column in (
                "operating_cash_flow_usd_m", "cash_ppe_usd_m",
                "operating_cash_less_cash_ppe_usd_m",
            )
        ))

    fig, panels = plt.subplots(1, 3, sharey=True, figsize=(10.0, 4.6))
    fig.subplots_adjust(left=0.085, right=0.98, bottom=0.18, top=0.71, wspace=0.24)
    fig.text(0.075, 0.91, "Cash after equipment spending fell at all three firms",
             fontsize=18, weight="bold")
    fig.text(0.075, 0.846, "Three months ended September 30, USD billions",
             color=MUTED, fontsize=10.5)

    legend = ("Operating cash", "Cash property and equipment", "Cash after equipment")
    colors = ("#116c65", "#ce913b", "#4b6aab")
    for ax, (company, periods) in zip(panels, figures.items()):
        ax.set_title(company, loc="left", pad=10, fontsize=12, weight="bold")
        for column, (label, color) in enumerate(zip(legend, colors)):
            offset = (column - 1) * 0.23
            ax.bar([offset, 1 + offset], [period[column] for period in periods],
                   width=0.20, color=color, label=label)
        ax.set_xticks([0, 1], ["2025", "2026"])
        ax.set_yticks(range(-10, 61, 10))
        ax.set_ylim(-11, 61)
        format_axis(ax, "$")

    handles, labels = panels[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower left", bbox_to_anchor=(0.075, 0.032),
               borderaxespad=0, ncol=3, frameon=False)
    fig.savefig(HERE / "capex-cash-flow.png", dpi=180)
    plt.close(fig)

def put_box(ax, x, y, width, height, label, color="#e1eeeb"):
    ax.add_patch(FancyBboxPatch(
        (x, y), width, height, boxstyle="round,pad=0.012,rounding_size=0.012",
        edgecolor="none", facecolor=color,
    ))
    ax.text(x + width / 2, y + height / 2, label, ha="center", va="center", weight="bold")


def financing_graph():
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    fig.subplots_adjust(left=0.075, right=0.925, bottom=0.10, top=0.74)
    fig.text(0.075, 0.91, "When a chipmaker is also a source of capital",
             fontsize=18, weight="bold")
    fig.text(0.075, 0.838, "Selected flows from the public Anthropic and CoreWeave disclosures",
             fontsize=9.5, color=MUTED)
    ax.set_axis_off()

    def flow(y, label, color, reverse=False):
        start, end = (0.75, 0.25) if reverse else (0.25, 0.75)
        ax.annotate("", (end, y), (start, y),
                    arrowprops={"arrowstyle": "-|>", "color": color, "linewidth": 1.35})
        ax.text(0.5, y + 0.025, label, va="bottom", ha="center", color=color, fontsize=9, parse_math=False)

    put_box(ax, 0.005, 0.29, 0.22, 0.46, "NVIDIA")
    put_box(ax, 0.775, 0.29, 0.22, 0.46, "CoreWeave")
    flow(0.71, "GPUs", "#116c65")
    flow(0.58, "$2bn completed equity investment", "#2b5792")
    flow(0.45, "Residual capacity payment obligation", "#9d443a")
    flow(0.32, "Residual compute access, subject to delivery", "#116c65", reverse=True)

    put_box(ax, 0.005, 0.04, 0.22, 0.15, "AMD")
    put_box(ax, 0.775, 0.04, 0.22, 0.15, "Anthropic")
    flow(0.11, "$2.5bn equity counted against $5bn cap", "#2b5792")

    fig.savefig(HERE / "circular-ai-financing.png", dpi=180)
    plt.close(fig)


def demand_funnel():
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    fig.subplots_adjust(left=0.075, right=0.925, bottom=0.095, top=0.76)
    fig.text(0.075, 0.91, "Four stages of a GPU cloud business",
             fontsize=18, weight="bold")
    fig.text(0.075, 0.838, "CoreWeave disclosures for the September 2026 quarter",
             fontsize=9.5, color=MUTED)
    ax.set_axis_off()

    rows = [
        ("Commercial demand", "$132.5bn revenue backlog"),
        ("Deliverable capacity", ">1.7 GW active, versus >4.6 GW contracted"),
        ("Billable service and activity", "98% committed-contract revenue\nGPU active time undisclosed"),
        ("Operating and financing results", "$207m operating income\n$709m net loss"),
    ]
    for i, (title, datum) in enumerate(rows):
        y = 0.84 - 0.245 * i
        put_box(ax, 0.005, y - 0.052, 0.385, 0.12, title)
        ax.text(0.455, y + 0.008, datum, va="center", fontsize=10)
        if i < len(rows) - 1:
            ax.annotate("", (0.198, y - 0.165), (0.198, y - 0.070),
                        arrowprops={"arrowstyle": "-|>", "color": MUTED, "linewidth": 1.25})
    fig.savefig(HERE / "ai-demand-utilization-profit.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    gpu_life_chart()
    capex_chart()
    financing_graph()
    demand_funnel()
