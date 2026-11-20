#!/usr/bin/env python3
"""Reproduce the reliability field notes' figures and derived values.

Requires matplotlib and Pillow. Source numbers and scenario inputs are below.
"""
from math import ceil, expm1, log, log1p
from pathlib import Path

from PIL import Image, ImageDraw

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
INK, ACCENT, ORANGE, BG = "#14213a", "#3157a1", "#a44c12", "#f5f8fe"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12, "text.color": INK,
    "axes.labelcolor": INK, "axes.edgecolor": "#aab8d2", "axes.facecolor": BG,
    "figure.facecolor": BG, "xtick.color": INK, "ytick.color": INK,
})


def frame(title, subtitle):
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    fig.subplots_adjust(left=.17, right=.94, bottom=.19, top=.72)
    fig.text(.075, .91, title, size=21, weight="bold")
    fig.text(.075, .825, subtitle, size=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, name):
    fig.savefig(HERE / f"{name}.webp", pil_kwargs={"lossless": True})
    plt.close(fig)


def benchmark():
    # Anthropic's reported Terminal-Bench 2.0 infrastructure error rates.
    settings = ("1× hard ceiling", "3× headroom", "Uncapped")
    errors = (5.8, 2.1, .5)
    fig, ax = frame("Same benchmark, fewer infra failures",
                    "Anthropic’s Terminal-Bench 2.0 experiment · reported values")
    fig.subplots_adjust(left=.26, bottom=.20)
    for index, (label, value) in enumerate(zip(settings, errors)):
        ax.barh(label, value, height=.48, color=ACCENT)
        ax.text(value + .13, index, f"{value:.1f}%", va="center", weight="bold")
    ax.invert_yaxis()
    ax.set(xlim=(0, 7), xlabel="Trials with infrastructure errors (%)")
    ax.grid(axis="x", alpha=.25)
    save(fig, "benchmark-headroom")


def chance(n, occurrence):
    return -expm1(n * log1p(-occurrence))


def exposure():
    fig, ax = frame("A small canary can miss a rare failure",
                    "Scenario · independent requests, with perfect detection when a failure occurs")
    for occurrence, color in ((.001, ACCENT), (.0001, ORANGE)):
        samples = range(0, 40001, 100)
        ax.plot(samples, [100 * chance(n, occurrence) for n in samples], lw=2.6, color=color,
                label=f"Failure in 1 of {round(1 / occurrence):,} canary requests")
        required = ceil(log(.05) / log1p(-occurrence))
        print(f"{occurrence:.4%}: P(detect in 1,000)={chance(1000, occurrence):.2%}, n95={required:,}")
    ax.axhline(95, color="#6a7487", lw=1, ls=":")
    ax.text(39100, 93, "95%", ha="right", va="top", color="#4f5971")
    ax.legend(loc="lower right", fontsize=10, frameon=False)
    ax.set(xlabel="Canary requests", ylabel="Chance of observing ≥1 failure (%)",
           xlim=(0, 40000), ylim=(0, 103))
    ax.grid(axis="y", alpha=.25)
    save(fig, "canary-sample-size")


def migration():
    phases = ("Baseline", "Copy finishes", "New read path", "New-only write", "Rollback read")
    old = [1, 2, 2, 2, 2]
    new = [float("nan"), 2, 2, 3, 3]
    assert old[2] == new[2] and old[-1] < new[-1]
    fig, ax = frame("Equal at cutover. Stale at rollback.",
                    "Scenario · one record, dual writes stop after the read cutover")
    fig.subplots_adjust(bottom=.24)
    ax.plot(phases, old, color=ORANGE, marker="s", lw=2.1, drawstyle="steps-post", label="Old store")
    ax.plot(phases, new, color=ACCENT, marker="o", ls="--", lw=2.1, drawstyle="steps-post", label="New store")
    ax.set(ylabel="Record version", yticks=[1, 2, 3], ylim=(.78, 3.3))
    ax.tick_params(axis="x", labelsize=10, rotation=19)
    ax.legend(loc="lower right", frameon=False)
    ax.grid(axis="y", alpha=.25)
    save(fig, "migration-revisions")


def covers():
    """Generate three small article thumbnails from the figure concepts."""
    output = HERE.parents[1] / "images" / "uploads"
    output.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1200, 675), INK)
    draw = ImageDraw.Draw(image)
    for i, width in enumerate((150, 275, 435)):
        x = 205 + i * 245
        y = 155 + i * 110
        draw.rounded_rectangle((x, y, x + width, y + 145), radius=24, outline="#95b6ff", width=8)
        draw.rounded_rectangle((x + 22, y + 24, x + 100, y + 121), radius=13, fill="#527dda")
    image.save(output / "agent-resource-budget.webp", lossless=True)

    image = Image.new("RGB", (1200, 675), INK)
    draw = ImageDraw.Draw(image)
    for row in range(6):
        for col in range(12):
            x, y = 183 + 73 * col, 157 + 73 * row
            fill = "#f7b365" if col < 2 and row < 3 else "#527dda"
            draw.ellipse((x, y, x + 31, y + 31), fill=fill)
    image.save(output / "canary-exposure.webp", lossless=True)

    image = Image.new("RGB", (1200, 675), INK)
    draw = ImageDraw.Draw(image)
    draw.line([(180, 470), (455, 470), (455, 330), (1020, 330)], fill="#f7b365", width=14)
    draw.line([(455, 330), (735, 330), (735, 195), (1020, 195)], fill="#95b6ff", width=12)
    for x, y, color in ((455, 330, "#95b6ff"), (1020, 330, "#f7b365"), (1020, 195, "#95b6ff")):
        draw.ellipse((x - 17, y - 17, x + 17, y + 17), fill=color)
    image.save(output / "migration-rollback.webp", lossless=True)


if __name__ == "__main__":
    benchmark()
    exposure()
    migration()
    # Covers are generated only in the Hugo source tree.
    if HERE.parent.name == "downloads" and (HERE.parents[2] / "config.yml").exists():
        covers()
