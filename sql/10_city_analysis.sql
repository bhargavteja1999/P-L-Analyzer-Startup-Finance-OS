-- 10_city_analysis.sql
-- Geographical Regional and City Performance Queries

-- Query 1: Regional Sales and Profitability Breakdown
SELECT 
    c.region_name,
    COUNT(s.transaction_id) AS total_orders,
    SUM(s.units_sold) AS total_units_sold,
    ROUND(SUM(s.revenue), 2) AS regional_revenue,
    ROUND(SUM(s.total_expense), 2) AS regional_expenses,
    ROUND(SUM(s.net_profit), 2) AS regional_net_profit,
    ROUND((SUM(s.net_profit) / SUM(s.revenue)) * 100, 2) AS regional_margin_pct
FROM sales_fact s
JOIN cities_dim c ON s.city_name = c.city_name
GROUP BY c.region_name
ORDER BY regional_revenue DESC;

-- Query 2: City Level Financial Performance Ranking
SELECT 
    c.city_name,
    c.region_name,
    COUNT(s.transaction_id) AS total_transactions,
    ROUND(SUM(s.revenue), 2) AS city_revenue,
    ROUND(SUM(s.shipping_expense), 2) AS total_shipping_cost,
    ROUND(SUM(s.net_profit), 2) AS city_net_profit,
    ROUND((SUM(s.net_profit) / SUM(s.revenue)) * 100, 2) AS city_margin_pct
FROM sales_fact s
JOIN cities_dim c ON s.city_name = c.city_name
GROUP BY c.city_name, c.region_name
ORDER BY city_revenue DESC;
