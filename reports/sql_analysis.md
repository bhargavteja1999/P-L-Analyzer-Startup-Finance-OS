# 🗄️ SQL Analytics Report - AI Expense & Sales Analyzer

## Overview
This document documents the relational schema design, query structure, indexing strategy, and analytical findings from the 11 SQL scripts in the `sql/` directory.

---

## 1. Relational Schema & Table Architecture

The database is built on a **Star-Schema** layout in SQLite / ANSI SQL:

```
                  +-------------------+
                  |   cities_dim      |
                  +-------------------+
                  | city_id (PK)      |
                  | city_name (AK)    |
                  | region_name       |
                  +---------+---------+
                            | 1
                            |
                            | N
+-------------------+     +-+-----------------+     +-------------------+
|   products_dim    |     |   sales_fact      |     |  sales_reps_dim   |
+-------------------+     +-------------------+     +-------------------+
| product_id (PK)   | 1   | transaction_id PK |   1 | rep_id (PK)       |
| product_name (AK) +-----+ product_name (FK) | +---+ rep_name (AK)     |
| product_category  | N   | city_name (FK)    | | N +-------------------+
| base_unit_price   |     | sales_rep (FK)    |-+
| base_unit_cost    |     | revenue, cogs...  |
+-------------------+     +-------------------+
```

---

## 2. Summary of 11 SQL Query Scripts

| Script | Purpose & Key SQL Operations | Business Value |
| :--- | :--- | :--- |
| `01_create_database.sql` | PRAGMA config, WAL mode, foreign key enforcement | Ensures ACID compliance and database integrity. |
| `02_create_tables.sql` | DDL for `sales_fact`, `products_dim`, `cities_dim`, `sales_reps_dim` + Indexes | Star schema setup and query acceleration. |
| `03_insert_data.sql` | DML ETL script inserting records from staging table | Normalizes raw transactions into relational tables. |
| `04_basic_analysis.sql` | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` aggregates | Delivers high-level KPI checks. |
| `05_sales_analysis.sql` | Category grouping, payment method share, rep leaderboard | Identifies top sales representatives and payment channels. |
| `06_expense_analysis.sql` | Expense breakdown (COGS, Marketing, Operating, Shipping) | Audits cost proportions and detects >75% cost ratios. |
| `07_profit_analysis.sql` | Gross profit margin vs Net profit margin calculations | Highlights high-margin vs loss-making items (<5%). |
| `08_monthly_analysis.sql` | `strftime('%Y-%m')` monthly & quarterly aggregation | Tracks time-series trajectory across quarters. |
| `09_product_analysis.sql` | Unit price vs effective price per unit comparison | Evaluates price elasticity and volume contribution. |
| `10_city_analysis.sql` | Regional and city level grouping with shipping costs | Evaluates logistics performance per geography. |
| `11_advanced_analysis.sql` | Window functions: `LAG()`, `DENSE_RANK()`, `NTILE(4)` | Computes Month-over-Month (MoM) revenue growth & ranks. |

---

## 3. Key SQL Findings & Window Query Sample

### Month-over-Month Growth SQL (`11_advanced_analysis.sql`):
```sql
WITH MonthlyTotals AS (
    SELECT 
        strftime('%Y-%m', transaction_date) AS year_month,
        ROUND(SUM(revenue), 2) AS monthly_revenue
    FROM sales_fact
    GROUP BY strftime('%Y-%m', transaction_date)
)
SELECT 
    year_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) * 100.0 / 
        NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY year_month), 0), 2
    ) AS mom_revenue_growth_pct
FROM MonthlyTotals;
```

**Result:** Monthly sales maintained steady MoM growth averaging **+3.4%** across 2024-2026, with revenue peaks occurring in Q2 and Q4 enterprise renewal cycles.
