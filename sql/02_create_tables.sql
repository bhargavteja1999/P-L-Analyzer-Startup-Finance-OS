-- 02_create_tables.sql
-- DDL Script to create star-schema relational tables:
-- Dimension Tables: products_dim, cities_dim, sales_reps_dim
-- Fact Table: sales_fact

DROP TABLE IF EXISTS sales_fact;
DROP TABLE IF EXISTS products_dim;
DROP TABLE IF EXISTS cities_dim;
DROP TABLE IF EXISTS sales_reps_dim;

-- Product Dimension
CREATE TABLE products_dim (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT UNIQUE NOT NULL,
    product_category TEXT NOT NULL,
    base_unit_price REAL NOT NULL,
    base_unit_cost REAL NOT NULL
);

-- City & Region Dimension
CREATE TABLE cities_dim (
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT UNIQUE NOT NULL,
    region_name TEXT NOT NULL
);

-- Sales Rep Dimension
CREATE TABLE sales_reps_dim (
    rep_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rep_name TEXT UNIQUE NOT NULL
);

-- Fact Table for Transactions
CREATE TABLE sales_fact (
    transaction_id TEXT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    product_name TEXT NOT NULL,
    city_name TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    sales_rep TEXT NOT NULL,
    units_sold INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    unit_cost REAL NOT NULL,
    revenue REAL NOT NULL,
    cogs REAL NOT NULL,
    marketing_expense REAL NOT NULL,
    shipping_expense REAL NOT NULL,
    operating_expense REAL NOT NULL,
    total_expense REAL NOT NULL,
    net_profit REAL NOT NULL,
    profit_margin_pct REAL NOT NULL,
    FOREIGN KEY (product_name) REFERENCES products_dim(product_name),
    FOREIGN KEY (city_name) REFERENCES cities_dim(city_name)
);

-- Create Indexes for Analytical Performance
CREATE INDEX idx_sales_date ON sales_fact(transaction_date);
CREATE INDEX idx_sales_product ON sales_fact(product_name);
CREATE INDEX idx_sales_city ON sales_fact(city_name);
CREATE INDEX idx_sales_rep ON sales_fact(sales_rep);
