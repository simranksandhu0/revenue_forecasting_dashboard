"""
regression_modelling.py
Fits a seasonality-adjusted linear regression model per product line
and generates a 3-month forward forecast with confidence intervals.
Exports forecast to outputs/revenue_forecast.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error


def load_and_validate(path: str = "data/revenue_data.csv") -> pd.DataFrame:
    """Load and validate revenue data."""
    if not Path(path).exists():
        raise FileNotFoundError(f"{path} not found. Run generate_data.py first.")

    df = pd.read_csv(path, parse_dates=["date"])

    required = {"date", "product_line", "revenue"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df["revenue"].lt(0).any():
        raise ValueError("Revenue column contains negative values.")

    if df["date"].isnull().any():
        raise ValueError("Null values found in date column.")

    print(f"Loaded {len(df):,} rows across {df['product_line'].nunique()} product lines.")
    return df


def build_features(df_product: pd.DataFrame) -> pd.DataFrame:
    """
    Add time index and Fourier terms for seasonality.
    One pair of sin/cos terms captures the dominant annual cycle.
    """
    df = df_product.copy().sort_values("date").reset_index(drop=True)
    df["t"] = np.arange(len(df))

    # Fourier terms for 12-month seasonality
    df["sin_12"] = np.sin(2 * np.pi * df["t"] / 12)
    df["cos_12"] = np.cos(2 * np.pi * df["t"] / 12)

    return df


def fit_forecast(df: pd.DataFrame, forecast_months: int = 3) -> pd.DataFrame:
    """
    Fit one regression model per product line.
    Appends forecast rows with confidence interval (±1.96 * residual std).

    Returns a combined DataFrame of actuals + forecast.
    """
    results = []
    feature_cols = ["t", "sin_12", "cos_12"]

    for product, group in df.groupby("product_line"):
        group = build_features(group)

        X = group[feature_cols].values
        y = group["revenue"].values

        model = LinearRegression()
        model.fit(X, y)

        y_pred_train = model.predict(X)
        mape = mean_absolute_percentage_error(y, y_pred_train)
        residual_std = np.std(y - y_pred_train)

        # Mark actuals
        group["type"] = "Actual"
        group["forecast"] = y_pred_train
        group["lower_ci"] = np.nan
        group["upper_ci"] = np.nan
        group["mape"] = mape

        # Build future rows
        last_t = group["t"].iloc[-1]
        last_date = group["date"].iloc[-1]
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=forecast_months,
            freq="MS",
        )
        future_t = np.arange(last_t + 1, last_t + 1 + forecast_months)
        future_sin = np.sin(2 * np.pi * future_t / 12)
        future_cos = np.cos(2 * np.pi * future_t / 12)
        X_future = np.column_stack([future_t, future_sin, future_cos])
        future_forecast = model.predict(X_future)

        z = 1.96  # 95% confidence interval
        future_df = pd.DataFrame({
            "date":         future_dates,
            "product_line": product,
            "revenue":      np.nan,
            "type":         "Forecast",
            "forecast":     future_forecast,
            "lower_ci":     future_forecast - z * residual_std,
            "upper_ci":     future_forecast + z * residual_std,
            "mape":         mape,
            "t":            future_t,
            "sin_12":       future_sin,
            "cos_12":       future_cos,
        })

        results.append(pd.concat([group, future_df], ignore_index=True))
        print(f"{product}: MAPE = {mape:.2%}")

    return pd.concat(results, ignore_index=True)


if __name__ == "__main__":
    Path("outputs").mkdir(exist_ok=True)
    df = load_and_validate()
    combined = fit_forecast(df, forecast_months=3)
    out_cols = ["date", "product_line", "revenue", "type", "forecast", "lower_ci", "upper_ci", "mape"]
    combined[out_cols].to_csv("outputs/revenue_forecast.csv", index=False)
    print(f"\nForecast saved to outputs/revenue_forecast.csv")
    print(f"Total rows (actuals + forecast): {len(combined):,}")
