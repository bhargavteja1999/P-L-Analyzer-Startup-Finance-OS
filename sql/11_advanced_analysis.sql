-- 11_advanced_analysis.sql
-- Advanced Analytical Window Functions: MoM Growth Rate, Cumulative Revenue, and Rankings

-- Query 1: Month-over-Month (MoM) Revenue & Profit Growth Rate using LAG()
WITH MonthlyTotals AS (
    SELECT 
        strftime('%Y-%m', transaction_date) AS year_month,
        ROUND(SUM(revenue), 2) AS monthly_revenue,
        ROUND(SUM(net_profit), 2) AS monthly_net_profit
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
    ) AS mom_revenue_growth_pct,
    monthly_net_profit,
    SUM(monthly_revenue) OVER (ORDER BY year_month) AS cumulative_running_revenue
FROM MonthlyTotals
ORDER BY year_month ASC;

-- Query 2: Product Ranking within Category using DENSE_RANK()
SELECT 
    p.product_category,
    p.product_name,
    ROUND(SUM(s.revenue), 2) AS product_revenue,
    ROUND(SUM(s.net_profit), 2) AS product_net_profit,
    DENSE_RANK() OVER (
        PARTITION BY p.product_category 
        ORDER BY SUM(s.revenue) DESC
    ) AS category_revenue_rank
FROM sales_fact s
JOIN products_dim p ON s.product_name = p.product_name
GROUP BY p.product_category, p.product_name
ORDER BY p.product_category, category_revenue_rank;

-- Query 3: Customer Transaction Quartiles using NTILE(4)
SELECT 
    transaction_id,
    customer_segment,
    revenue,
    net_profit,
    NTILE(4) OVER (ORDER BY revenue DESC) AS revenue_quartile
FROM sales_fact;
