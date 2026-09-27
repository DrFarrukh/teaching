"""Lecture 1 live demonstration.

This script uses the prepared CSV files so class time stays focused on analytical
reasoning. Run prepare_data.py before using it.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
OUTPUT_DIR = HERE / "outputs"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    long_data = pd.read_csv(DATA_DIR / "passenger_cars_long.csv", parse_dates=["date"])
    annual_brand = pd.read_csv(DATA_DIR / "annual_brand_sales.csv")
    market_summary = pd.read_csv(DATA_DIR / "annual_market_summary.csv")
    return long_data, annual_brand, market_summary


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "axes.titlesize": 18,
            "axes.labelsize": 13,
            "axes.edgecolor": "#222222",
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "grid.color": "#D0D0D0",
            "grid.linewidth": 0.7,
            "grid.alpha": 0.7,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def finish_figure(fig: plt.Figure, filename: str) -> None:
    fig.text(
        0.01,
        0.01,
        "Source: Pakistan Automotive Manufacturers Association (PAMA) monthly production and sales workbook. Values describe records in the workbook.",
        ha="left",
        va="bottom",
        fontsize=8,
        color="#444444",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUTPUT_DIR / filename, dpi=180, bbox_inches="tight")


def plot_annual_sales(summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 6.75))
    x_positions = list(range(len(summary)))
    ax.plot(
        x_positions,
        summary["total_recorded_sales"],
        color="#111111",
        marker="o",
        linewidth=2.2,
        markersize=5,
    )
    ax.set_title("Recorded passenger car sales changed sharply across fiscal years", loc="left")
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Recorded sales")
    ax.set_xticks(x_positions, labels=summary["fiscal_year"], rotation=55)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_major_formatter(lambda value, _: f"{value / 1000:.0f}k")

    for fiscal_year in ["2019-20", "2021-22", "2022-23", "2025-26"]:
        row_index = summary.index[summary["fiscal_year"].eq(fiscal_year)][0]
        row = summary.loc[row_index]
        ax.annotate(
            f'{int(row["total_recorded_sales"]):,}',
            (row_index, row["total_recorded_sales"]),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )
    finish_figure(fig, "annual_total_sales.png")


def plot_big_three_share(summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 6.75))
    x_positions = list(range(len(summary)))
    percent = 100 * summary["big_three_recorded_share"]
    ax.plot(
        x_positions,
        percent,
        color="#111111",
        marker="s",
        linewidth=2.2,
        markersize=5,
    )
    ax.axhline(90, color="#666666", linestyle="--", linewidth=1)
    ax.set_title("The Big Three retain a very high share of recorded passenger car sales", loc="left")
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Combined recorded share")
    ax.set_ylim(0, 102)
    ax.set_yticks([0, 20, 40, 60, 80, 90, 100], labels=["0%", "20%", "40%", "60%", "80%", "90%", "100%"])
    ax.set_xticks(x_positions, labels=summary["fiscal_year"], rotation=55)
    ax.spines[["top", "right"]].set_visible(False)

    last = summary.iloc[-1]
    ax.annotate(
        f'{last["big_three_recorded_share"]:.1%}',
        (x_positions[-1], 100 * last["big_three_recorded_share"]),
        xytext=(-5, -24),
        textcoords="offset points",
        ha="right",
        fontsize=11,
        fontweight="bold",
    )
    finish_figure(fig, "big_three_share.png")


def plot_recorded_ev_sales(summary: pd.DataFrame) -> None:
    ev = summary.loc[summary["recorded_ev_sales"].gt(0)].copy()
    fig, ax = plt.subplots(figsize=(12, 6.75))
    x_positions = list(range(len(ev)))
    bars = ax.bar(
        x_positions,
        ev["recorded_ev_sales"],
        color=["#B8B8B8", "#333333"],
        edgecolor="#111111",
        width=0.55,
    )
    ax.set_title("The workbook begins reporting a separate electric car category", loc="left")
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Recorded Honri-Ve sales")
    ax.set_xticks(x_positions, labels=ev["fiscal_year"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", visible=False)

    for bar, (_, row) in zip(bars, ev.iterrows()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            f'{int(row["recorded_ev_sales"]):,}\n{row["recorded_ev_share"]:.2%} of recorded cars',
            ha="center",
            va="bottom",
            fontsize=11,
        )
    ax.set_ylim(0, max(ev["recorded_ev_sales"]) * 1.35)
    finish_figure(fig, "recorded_ev_sales.png")


def print_demo_outputs(
    long_data: pd.DataFrame,
    annual_brand: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    sales = long_data.loc[long_data["measure"].eq("Sales")]

    print("\n1. First five prepared records")
    print(sales.head().to_string(index=False))

    print("\n2. Data coverage")
    print(f"Fiscal years: {sales['fiscal_year'].nunique()}")
    print(f"First fiscal year: {sales['fiscal_year'].iloc[0]}")
    print(f"Last fiscal year: {sales['fiscal_year'].iloc[-1]}")
    print(f"Manufacturers after normalization: {annual_brand['manufacturer'].nunique()}")

    print("\n3. Annual market summary")
    display = summary.copy()
    display["big_three_recorded_share"] = display["big_three_recorded_share"].map(
        lambda value: f"{value:.1%}"
    )
    display["recorded_ev_share"] = display["recorded_ev_share"].map(
        lambda value: f"{value:.2%}"
    )
    print(display.to_string(index=False))

    previous = summary.loc[summary["fiscal_year"].eq("2021-22"), "total_recorded_sales"].iloc[0]
    current = summary.loc[summary["fiscal_year"].eq("2022-23"), "total_recorded_sales"].iloc[0]
    print("\n4. Descriptive change, not a causal explanation")
    print(f"2021-22 to 2022-23: {(current / previous - 1):+.1%}")

    last = summary.iloc[-1]
    print("\n5. Final evidence")
    print(f'Big Three recorded share in {last["fiscal_year"]}: {last["big_three_recorded_share"]:.1%}')
    print(f'Recorded electric car share in {last["fiscal_year"]}: {last["recorded_ev_share"]:.2%}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true", help="Display figures after saving them")
    args = parser.parse_args()

    required = [
        DATA_DIR / "passenger_cars_long.csv",
        DATA_DIR / "annual_brand_sales.csv",
        DATA_DIR / "annual_market_summary.csv",
    ]
    missing = [path.name for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing prepared files: {', '.join(missing)}. Run prepare_data.py first."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)
    setup_style()
    long_data, annual_brand, summary = load_data()
    print_demo_outputs(long_data, annual_brand, summary)
    plot_annual_sales(summary)
    plot_big_three_share(summary)
    plot_recorded_ev_sales(summary)

    print(f"\nSaved figures to {OUTPUT_DIR}")
    if args.show:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main()
