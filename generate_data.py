"""
generate_data.py
Generates synthetic monthly revenue data across 4 product lines
with realistic seasonality, trend, and noise. Saves to data/revenue_data.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
START = "2021-01-01"
PERIODS = 48  # 4 years of monthly data

PRODUCT_LINES = {
    "Apparel":      {"base": 120_000, "trend": 800,  "season_amp": 0.20, "noise": 0.05},
    "Accessories":  {"base":  60_000, "trend": 400,  "season_amp": 0.15, "noise": 0.06},
    "Footwear":     {"base":  90_000, "trend": 600,  "season_amp": 0.25, "noise": 0.07},
    "Electronics":  {"base":  45_000, "trend": 1200, "season_amp": 0.30, "noise": 0.08},
}


def generate_revenue_data(seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start=START, periods=PERIODS, freq="MS")
    records = []

    for product, params in PRODUCT_LINES.items():
        base        = params["base"]
        trend       = params["trend"]
        season_amp  = params["season_amp"]
        noise_pct   = params["noise"]

        for i, date in enumerate(dates):
            # Linear trend
            trend_component = trend * i

            # Seasonality: peak in Nov/Dec, trough in Jan/Feb
            month_idx = date.month
            season = season_amp * base * np.sin(2 * np.pi * (month_idx - 3) / 12)

            # Random noise
            noise = rng.normal(0, noise_pct * base)

            revenue = max(0.0, base + trend_component + season + noise)

            records.append({
                "date":         date.strftime("%Y-%m-%d"),
                "product_line": product,
                "region":       rng.choice(["West", "East", "Central"]),
                "revenue":      round(revenue, 2),
                "units_sold":   max(1, int(revenue / rng.uniform(20, 80))),
            })

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)
    df = generate_revenue_data()
    df.to_csv("data/revenue_data.csv", index=False)
    print(f"Saved {len(df):,} rows to data/revenue_data.csv")
    print(df.groupby("product_line")["revenue"].describe().round(0))
