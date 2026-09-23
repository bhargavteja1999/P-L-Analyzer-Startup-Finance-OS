-- 08_monthly_analysis.sql
-- Time-Series & Monthly Trend Analysis Queries

-- Query 1: Monthly Revenue, Expense, and Profit Aggregations
SELECT 
    strftime('%Y-%m', transaction_date) AS year_month,
    COUNT(transaction_id) AS total_transactions,
    SUM(units_sold) AS units_sold,
    ROUND(SUM(revenue), 2) AS monthly_revenue,
    ROUND(SUM(total_expense), 2) AS monthly_expense,
    ROUND(SUM(net_profit), 2) AS monthly_net_profit,
    ROUND((SUM(net_profit) / SUM(revenue)) * 100, 2) AS net_margin_pct
FROM sales_fact
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY year_month ASC;

-- Query 2: Quarterly Aggregations & Seasonal Trends
SELECT 
    strftime('%Y', transaction_date) AS year,
    CASE 
        WHEN strftime('%m', transaction_date) IN ('01', '02', '03') THEN 'Q1'
        WHEN strftime('%m', transaction_date) IN ('04', '05', '06') THEN 'Q2'
        WHEN strftime('%m', transaction_date) IN ('07', '08', '09') THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    ROUND(SUM(revenue), 2) AS quarterly_revenue,
    ROUND(SUM(total_expense), 2) AS quarterly_expense,
    ROUND(SUM(net_profit), 2) AS quarterly_profit
FROM sales_fact
GROUP BY year, quarter
ORDER BY year ASC, quarter ASC;
