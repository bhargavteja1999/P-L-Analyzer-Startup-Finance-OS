-- 06_expense_analysis.sql
-- Cost Structure & Expense Analysis Queries

-- Query 1: Overall Expense Category Breakdown & Share
SELECT 
    ROUND(SUM(cogs), 2) AS total_cogs,
    ROUND(SUM(marketing_expense), 2) AS total_marketing,
    ROUND(SUM(shipping_expense), 2) AS total_shipping,
    ROUND(SUM(operating_expense), 2) AS total_operating,
    ROUND(SUM(total_expense), 2) AS grand_total_expenses,
    ROUND((SUM(cogs) / SUM(total_expense)) * 100, 2) AS cogs_pct,
    ROUND((SUM(marketing_expense) / SUM(total_expense)) * 100, 2) AS marketing_pct,
    ROUND((SUM(shipping_expense) / SUM(total_expense)) * 100, 2) AS shipping_pct,
    ROUND((SUM(operating_expense) / SUM(total_expense)) * 100, 2) AS operating_pct
FROM sales_fact;

-- Query 2: Expense Ratios by Product Category
SELECT 
    p.product_category,
    ROUND(SUM(s.revenue), 2) AS revenue,
    ROUND(SUM(s.cogs), 2) AS cogs,
    ROUND(SUM(s.marketing_expense), 2) AS marketing,
    ROUND(SUM(s.shipping_expense), 2) AS shipping,
    ROUND(SUM(s.operating_expense), 2) AS operating,
    ROUND(SUM(s.total_expense), 2) AS total_expense,
    ROUND((SUM(s.total_expense) / SUM(s.revenue)) * 100, 2) AS expense_to_revenue_pct
FROM sales_fact s
JOIN products_dim p ON s.product_name = p.product_name
GROUP BY p.product_category
ORDER BY total_expense DESC;

-- Query 3: High Expense Ratio Anomaly Detection (> 75% of Revenue)
SELECT 
    transaction_id,
    transaction_date,
    product_name,
    city_name,
    revenue,
    total_expense,
    profit_margin_pct,
    ROUND((total_expense / revenue) * 100, 2) AS expense_ratio_pct
FROM sales_fact
WHERE (total_expense / revenue) > 0.75
ORDER BY expense_ratio_pct DESC;
