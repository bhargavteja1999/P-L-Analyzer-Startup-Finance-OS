-- 03_insert_data.sql
-- DML Population Script: Inserts dimension data and copies records from staging table sales_expenses.

-- Populate Products Dimension
INSERT OR IGNORE INTO products_dim (product_name, product_category, base_unit_price, base_unit_cost)
SELECT DISTINCT Product_Name, Product_Category, Unit_Price, Unit_Cost
FROM sales_expenses;

-- Populate Cities Dimension
INSERT OR IGNORE INTO cities_dim (city_name, region_name)
SELECT DISTINCT City, Region
FROM sales_expenses;

-- Populate Sales Reps Dimension
INSERT OR IGNORE INTO sales_reps_dim (rep_name)
SELECT DISTINCT Sales_Rep
FROM sales_expenses;

-- Populate Fact Table
INSERT OR REPLACE INTO sales_fact (
    transaction_id, transaction_date, product_name, city_name, customer_segment,
    payment_method, sales_rep, units_sold, unit_price, unit_cost, revenue,
    cogs, marketing_expense, shipping_expense, operating_expense, total_expense,
    net_profit, profit_margin_pct
)
SELECT 
    Transaction_ID, Date, Product_Name, City, Customer_Segment,
    Payment_Method, Sales_Rep, Units_Sold, Unit_Price, Unit_Cost, Revenue,
    COGS, Marketing_Expense, Shipping_Expense, Operating_Expense, Total_Expense,
    Net_Profit, Profit_Margin_Pct
FROM sales_expenses;

SELECT 
    (SELECT COUNT(*) FROM sales_fact) AS total_fact_rows,
    (SELECT COUNT(*) FROM products_dim) AS total_products,
    (SELECT COUNT(*) FROM cities_dim) AS total_cities;
