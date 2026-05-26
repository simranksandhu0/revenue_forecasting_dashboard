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
revenue-forecasting-dashboard/
├── dashboard/
│   └── revenue_forecast.pbix       # Power BI file
├── data/
│   └── sample_revenue_data.csv     # Anonymised sample data
├── notebooks/
│   └── regression_modelling.ipynb  # Forecast model development
├── screenshots/
│   ├── overview.png
│   └── drilldown_view.png
└── README.md
```

---

## Impact

- Replaced a static monthly Excel report that required manual analyst effort to produce and distribute
- Enabled forward-looking financial planning — leadership could see projected revenue 3 months out, not just last month's actuals
- Reduced ad-hoc data requests by giving stakeholders self-serve drill-down capability

---

## How to Open

1. Download `dashboard/revenue_forecast.pbix`
2. Open in Power BI Desktop (free download from Microsoft)
3. Connect to `data/sample_revenue_data.csv` if prompted to refresh the data source

---

## Screenshots

*(Add screenshots of the dashboard here once published)*
