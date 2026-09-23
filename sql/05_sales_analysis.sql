-- 05_sales_analysis.sql
-- In-depth Sales Analytics Queries

-- Query 1: Sales Performance by Category
SELECT 
    p.product_category,
    COUNT(s.transaction_id) AS transaction_count,
    SUM(s.units_sold) AS total_units_sold,
    ROUND(SUM(s.revenue), 2) AS total_revenue,
    ROUND(AVG(s.revenue), 2) AS avg_transaction_value,
    ROUND((SUM(s.revenue) * 100.0 / (SELECT SUM(revenue) FROM sales_fact)), 2) AS revenue_share_pct
FROM sales_fact s
JOIN products_dim p ON s.product_name = p.product_name
GROUP BY p.product_category
ORDER BY total_revenue DESC;

-- Query 2: Sales Performance by Payment Method
SELECT 
    payment_method,
    COUNT(*) AS total_transactions,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_transaction_value
FROM sales_fact
GROUP BY payment_method
ORDER BY total_revenue DESC;

-- Query 3: Sales Rep Performance Leaderboard
SELECT 
    sales_rep,
    COUNT(transaction_id) AS deals_closed,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(net_profit), 2) AS total_profit_generated,
    ROUND((SUM(net_profit) / SUM(revenue)) * 100, 2) AS avg_rep_margin_pct
FROM sales_fact
GROUP BY sales_rep
ORDER BY total_revenue DESC;
