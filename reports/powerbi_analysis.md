# 📊 Power BI Dashboard & DAX Analysis Guide

## Overview
This report documents the Power BI dataset model architecture, calculated DAX measures, visual layouts, and screenshot assets for **AI_Expense_Sales_Analyzer.pbix**.

---

## 1. Data Model Architecture (Star Schema)

The Power BI data model connects the central `sales_fact` table to dimension tables using 1-to-Many (`1:*`) single-direction relationships:

- **`products_dim` [product_name]** `1` ─── `*` **`sales_fact` [product_name]**
- **`cities_dim` [city_name]** `1` ─── `*` **`sales_fact` [city_name]**
- **`sales_reps_dim` [rep_name]** `1` ─── `*` **`sales_fact` [sales_rep]**

---

## 2. Essential DAX Measures

### Total Revenue
```dax
Total Revenue = SUM(sales_fact[revenue])
```

### Total Expenses
```dax
Total Expenses = SUM(sales_fact[total_expense])
```

### Net Profit
```dax
Net Profit = [Total Revenue] - [Total Expenses]
```

### Net Profit Margin %
```dax
Net Profit Margin % = 
DIVIDE([Net Profit], [Total Revenue], 0) * 100
```

### Expense-to-Revenue Ratio %
```dax
Expense Ratio % = 
DIVIDE([Total Expenses], [Total Revenue], 0) * 100
```

### Month-over-Month Revenue Growth %
```dax
MoM Revenue Growth % = 
VAR CurrentMonthRev = [Total Revenue]
VAR PrevMonthRev = CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))
RETURN
DIVIDE(CurrentMonthRev - PrevMonthRev, PrevMonthRev, 0) * 100
```

---

## 3. Power BI Visual Mockups Summary

| Dashboard View | File Asset | Visual Elements |
| :--- | :--- | :--- |
| **Executive Overview** | `powerbi/screenshots/executive_dashboard.png` | KPI cards, Monthly trend, Category bar, Region Donut |
| **Sales Analysis** | `powerbi/screenshots/sales_analysis.png` | Top 10 products, Sales Rep matrix, Segment breakdown |
| **Expense Analysis** | `powerbi/screenshots/expense_analysis.png` | Cost category donut, Expense ratio bar, Anomaly table |
| **Profitability Analysis**| `powerbi/screenshots/profit_analysis.png` | Margin waterfall, Tier breakdown, Top/Bottom products |
| **Detailed Deep-Dive** | `powerbi/screenshots/detailed_analysis.png` | Matrix drilldown, City margin heatmap, Payment distribution |
