-- 04_basic_analysis.sql
-- Basic Data Verification & KPI Summary Queries

-- Query 1: Total Volume and Revenue Summary
SELECT 
    COUNT(transaction_id) AS total_transactions,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(total_expense), 2) AS total_expenses,
    ROUND(SUM(net_profit), 2) AS net_profit,
    ROUND((SUM(net_profit) / SUM(revenue)) * 100, 2) AS overall_profit_margin_pct
FROM sales_fact;

-- Query 2: Minimum, Maximum, and Average Order Values
SELECT 
    ROUND(AVG(revenue), 2) AS avg_order_value,
    ROUND(MIN(revenue), 2) AS min_order_value,
    ROUND(MAX(revenue), 2) AS max_order_value,
    ROUND(AVG(net_profit), 2) AS avg_profit_per_order
FROM sales_fact;

-- Query 3: Transactions Count by Customer Segment
SELECT 
    customer_segment,
    COUNT(*) AS transaction_count,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_revenue
FROM sales_fact
GROUP BY customer_segment
ORDER BY total_revenue DESC;
