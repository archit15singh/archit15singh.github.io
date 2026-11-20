"""Reproduce article 05's illustrative per-GPU-equivalent financial model.

Run with Python 3.9+. Default stdout is CSV. Monetary inputs are scenarios.
"""
from argparse import ArgumentParser
import csv
import sys

HOURS_PER_YEAR = 8_760


def cash_flows(hourly_price, price_decline, billable_share, annual_cost, years):
    """Return operating cash for periods 1 to years, with no salvage."""
    billable_hours = HOURS_PER_YEAR * billable_share
    return [
        hourly_price * (1 - price_decline) ** (year - 1) * billable_hours - annual_cost
        for year in range(1, years + 1)
    ]


def discounted_cash(cash_flows_by_year, discount_rate):
    return sum(
        cash / (1 + discount_rate) ** year
        for year, cash in enumerate(cash_flows_by_year, start=1)
    )


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--capital", type=float, default=35_000)
    parser.add_argument("--hourly-price", type=float, default=3.20)
    parser.add_argument("--billable-share", type=float, default=0.72)
    parser.add_argument("--annual-cost", type=float, default=4_200)
    parser.add_argument("--discount-rate", type=float, default=0.10)
    parser.add_argument("--declines", nargs="+", type=float, default=[0, 0.15, 0.30])
    args = parser.parse_args()

    assumptions_valid = (
        args.capital >= 0
        and args.hourly_price >= 0
        and 0 < args.billable_share <= 1
        and args.annual_cost >= 0
        and args.discount_rate >= 0
        and all(0 <= decline <= 1 for decline in args.declines)
    )
    if not assumptions_valid:
        parser.error("Expected nonnegative costs, price and discount rate. Billable share must be in (0, 1] and declines in [0, 1].")

    output = csv.writer(sys.stdout, lineterminator="\n")
    output.writerow([
        "annual_price_decline", "initial_capital_usd", "year_1_rate_usd",
        "billable_share", "annual_cash_cost_usd", "discount_rate",
        "year_1_cash_usd", "year_2_cash_usd", "year_3_cash_usd",
        "year_4_cash_usd", "year_5_cash_usd", "npv_3_year_usd",
        "npv_5_year_usd", "break_even_year_1_price_3_year_usd",
        "break_even_year_1_price_5_year_usd",
    ])
    for decline in args.declines:
        cash = cash_flows(args.hourly_price, decline, args.billable_share, args.annual_cost, 5)
        revenue_at_one_dollar = cash_flows(1, decline, args.billable_share, 0, 5)

        def break_even_rate(years):
            cost_pv = args.capital + discounted_cash([args.annual_cost] * years, args.discount_rate)
            billable_revenue_factor = discounted_cash(revenue_at_one_dollar[:years], args.discount_rate)
            return cost_pv / billable_revenue_factor

        output.writerow([
            f"{decline:.2f}", f"{args.capital:.2f}", f"{args.hourly_price:.2f}",
            f"{args.billable_share:.2f}", f"{args.annual_cost:.2f}", f"{args.discount_rate:.2f}",
            *[f"{value:.2f}" for value in cash],
            f"{discounted_cash(cash[:3], args.discount_rate) - args.capital:.2f}",
            f"{discounted_cash(cash, args.discount_rate) - args.capital:.2f}",
            f"{break_even_rate(3):.4f}", f"{break_even_rate(5):.4f}",
        ])


if __name__ == "__main__":
    main()
