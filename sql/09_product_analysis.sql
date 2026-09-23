-- 09_product_analysis.sql
-- Granular Product Performance Analysis Queries

-- Query 1: Product Level Profitability Ranking
SELECT 
    p.product_name,
    p.product_category,
    COUNT(s.transaction_id) AS total_orders,
    SUM(s.units_sold) AS total_units_sold,
    ROUND(SUM(s.revenue), 2) AS total_revenue,
    ROUND(SUM(s.total_expense), 2) AS total_expense,
    ROUND(SUM(s.net_profit), 2) AS total_net_profit,
    ROUND((SUM(s.net_profit) / SUM(s.revenue)) * 100, 2) AS product_margin_pct
FROM sales_fact s
JOIN products_dim p ON s.product_name = p.product_name
GROUP BY p.product_name, p.product_category
ORDER BY total_net_profit DESC;

-- Query 2: Product Volume vs Revenue Comparison
SELECT 
    product_name,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    ROUND(AVG(unit_cost), 2) AS avg_unit_cost,
    SUM(units_sold) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(revenue) / SUM(units_sold), 2) AS effective_price_per_unit
FROM sales_fact
GROUP BY product_name
ORDER BY units_sold DESC;
