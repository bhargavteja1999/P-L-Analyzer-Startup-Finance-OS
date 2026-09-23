-- 07_profit_analysis.sql
-- Profitability & Margin Analysis Queries

-- Query 1: Overall Profit Metrics
SELECT 
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue - cogs), 2) AS gross_profit,
    ROUND(SUM(net_profit), 2) AS net_profit,
    ROUND((SUM(revenue - cogs) / SUM(revenue)) * 100, 2) AS gross_margin_pct,
    ROUND((SUM(net_profit) / SUM(revenue)) * 100, 2) AS net_margin_pct
FROM sales_fact;

-- Query 2: Net Profit Margin by Product Category
SELECT 
    p.product_category,
    ROUND(SUM(s.revenue), 2) AS total_revenue,
    ROUND(SUM(s.total_expense), 2) AS total_expense,
    ROUND(SUM(s.net_profit), 2) AS net_profit,
    ROUND((SUM(s.net_profit) / SUM(s.revenue)) * 100, 2) AS net_profit_margin_pct
FROM sales_fact s
JOIN products_dim p ON s.product_name = p.product_name
GROUP BY p.product_category
ORDER BY net_profit DESC;

-- Query 3: Loss-Making or Ultra-Low Margin Transactions (< 5% Margin)
SELECT 
    transaction_id,
    transaction_date,
    product_name,
    customer_segment,
    revenue,
    total_expense,
    net_profit,
    profit_margin_pct
FROM sales_fact
WHERE profit_margin_pct < 5.0
ORDER BY profit_margin_pct ASC;
