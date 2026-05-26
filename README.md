# Revenue Forecasting Dashboard

> An interactive Power BI dashboard that replaced a static monthly Excel report with forward-looking, regression-based revenue forecasts across multiple product lines.

---

## Overview

Static Excel reports tell you what already happened. This dashboard tells you what's coming — and lets stakeholders explore the data themselves without waiting for an analyst to run a new report.

Built in Power BI with regression-based forecasting, this dashboard gives finance and leadership teams a live view of projected revenue by product line, with drill-down capability and variance tracking against targets.

---

## Problem Statement

The team was working from a static monthly Excel file that showed historical revenue only. By the time it was circulated, it was already out of date. Leadership had no forward-looking visibility, and every ad-hoc question required a new analyst pull.

---

## Solution

An interactive Power BI dashboard with:
- **Regression-based revenue forecasting** across multiple product lines
- **Actual vs. forecast variance** tracking with period-over-period comparison
- **Drill-down filters** by product line, region, and time period
- **Auto-refresh** connected to source data — no manual updates required

---

## Methodology

### Forecasting Approach
- Built regression models (linear and polynomial where trend indicated) for each product line
- Incorporated seasonality adjustments based on historical patterns
- Generated confidence intervals to communicate forecast uncertainty to stakeholders

### DAX Measures (Key Examples)
```dax
// Rolling 3-month average
Rolling_3M_Avg = 
AVERAGEX(
    DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -3, MONTH),
    [Total Revenue]
)

// Forecast vs Actual Variance %
Variance_Pct = 
DIVIDE([Actual Revenue] - [Forecast Revenue], [Forecast Revenue], 0)
```

### Data Model
- Star schema: fact table (transactions) connected to dimension tables (date, product, region)
- DAX calculated columns for time intelligence (MTD, QTD, YTD)

---

## Key Features

| Feature | Description |
|---|---|
| Forecast Line | Regression-based projection for next 3 months |
| Confidence Band | Upper/lower bounds around the forecast |
| Variance Tracker | Actual vs. forecast, colour-coded by threshold |
| Product Drill-down | Filter any visual by product line |
| Period Comparison | YoY and MoM toggle |

---

## Stack

- **Power BI Desktop** — dashboard and data model
- **DAX** — calculated measures and time intelligence
- **Python (Pandas + NumPy)** — regression model development; forecast coefficients exported and loaded into Power BI
- **Excel / CSV** — source data format

---

## File Structure

```
revenue_forecasting_dashboard/
├── generate_data.py          # Generates synthetic revenue data
├── regression_modelling.py   # Builds and evaluates regression forecast models
└── README.md
```

---

## Impact

- Replaced a static monthly Excel report that required manual analyst effort to produce and distribute
- Enabled forward-looking financial planning — leadership could see projected revenue 3 months out, not just last month's actuals
- Reduced ad-hoc data requests by giving stakeholders self-serve drill-down capability

---

## How to Run
```
# Clone the repo
git clone https://github.com/simranksandhu0/revenue_forecasting_dashboard.git
cd revenue_forecasting_dashboard

# Generate synthetic data
python generate_data.py

# Run regression modelling
python regression_modelling.py
```

## Notes

The regression model outputs forecast coefficients designed to be loaded into a Power BI dashboard. The Python scripts here cover the data generation and modelling layer; the Power BI file is not included in this repo.
