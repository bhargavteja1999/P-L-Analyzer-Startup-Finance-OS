"""
Data Loader Module for AI-Expense-Sales-Analyzer.
Handles loading raw data (CSV/Excel), saving generated data, and providing database connectivity.
"""

import os
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta

# Configuration paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DB_PATH = os.path.join(BASE_DIR, 'data', 'expense_sales.db')

RAW_CSV_PATH = os.path.join(RAW_DATA_DIR, 'sales_expense_data.csv')
RAW_EXCEL_PATH = os.path.join(RAW_DATA_DIR, 'sales_expense_data.xlsx')
PROCESSED_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, 'cleaned_sales_data.csv')


def ensure_directories():
    """Ensure data directories exist."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def generate_synthetic_data(num_records=1000, seed=42):
    """
    Generates a realistic multi-year synthetic Sales & Expense dataset.
    
    Returns:
        pd.DataFrame: Clean raw dataset DataFrame
    """
    np.random.seed(seed)
    ensure_directories()
    
    categories_products = {
        'Electronics': [
            ('Laptop Pro 15', 1200.0, 750.0),
            ('Smart Display 10', 350.0, 200.0),
            ('Wireless Noise-Canceling Headset', 250.0, 120.0),
            ('Ultra-Wide Monitor 34', 650.0, 380.0)
        ],
        'Software': [
            ('Enterprise ERP License', 2500.0, 500.0),
            ('Cloud Storage Annual', 400.0, 80.0),
            ('Data Analytics Suite', 1500.0, 300.0),
            ('Security Firewall Pro', 850.0, 220.0)
        ],
        'Office Supplies': [
            ('Ergonomic Executive Desk', 850.0, 450.0),
            ('Mesh Office Chair', 320.0, 160.0),
            ('Standing Desk Converter', 280.0, 140.0),
            ('High-Speed Paper Shredder', 180.0, 90.0)
        ],
        'Hardware': [
            ('Rack Server Blade X', 3200.0, 2100.0),
            ('Gigabit Switch 24-Port', 450.0, 260.0),
            ('NAS Storage Enclosure', 780.0, 480.0)
        ],
        'Services': [
            ('Annual IT Maintenance Plan', 1800.0, 600.0),
            ('Cloud Migration Consulting', 3500.0, 1200.0),
            ('Cybersecurity Audit', 2200.0, 800.0)
        ]
    }
    
    cities_regions = [
        ('New York', 'East'),
        ('Boston', 'East'),
        ('Miami', 'East'),
        ('Chicago', 'Midwest'),
        ('Houston', 'South'),
        ('Austin', 'South'),
        ('Phoenix', 'West'),
        ('Los Angeles', 'West'),
        ('San Francisco', 'West'),
        ('Seattle', 'West')
    ]
    
    customer_segments = ['Enterprise', 'SMB', 'Consumer', 'Government']
    payment_methods = ['Credit Card', 'Wire Transfer', 'PayPal', 'Direct Invoice']
    sales_reps = ['Alice Smith', 'Bob Jones', 'Charlie Davis', 'Diana Prince', 'Evan Wright', 'Fiona Gallagher']
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 30)
    days_range = (end_date - start_date).days
    
    records = []
    
    for i in range(1, num_records + 1):
        txn_id = f"TXN-{1000 + i}"
        random_days = np.random.randint(0, days_range)
        date = start_date + timedelta(days=int(random_days))
        
        category = np.random.choice(list(categories_products.keys()))
        prod_tuple = categories_products[category][np.random.randint(0, len(categories_products[category]))]
        product_name, base_price, base_cost = prod_tuple
        
        city, region = cities_regions[np.random.randint(0, len(cities_regions))]
        customer_segment = np.random.choice(customer_segments, p=[0.35, 0.40, 0.15, 0.10])
        payment_method = np.random.choice(payment_methods)
        sales_rep = np.random.choice(sales_reps)
        
        # Quantity based on segment
        if customer_segment == 'Enterprise':
            units = np.random.randint(5, 30)
        elif customer_segment == 'Government':
            units = np.random.randint(10, 40)
        else:
            units = np.random.randint(1, 8)
            
        unit_price = round(base_price * np.random.uniform(0.92, 1.08), 2)
        unit_cost = round(base_cost * np.random.uniform(0.95, 1.05), 2)
        
        revenue = round(units * unit_price, 2)
        cogs = round(units * unit_cost, 2)
        
        # Calculate expense components
        marketing_expense = round(revenue * np.random.uniform(0.06, 0.14), 2)
        shipping_expense = round(units * np.random.uniform(5.0, 15.0), 2)
        operating_expense = round(revenue * np.random.uniform(0.05, 0.12) + np.random.uniform(20.0, 80.0), 2)
        
        total_expense = round(cogs + marketing_expense + shipping_expense + operating_expense, 2)
        net_profit = round(revenue - total_expense, 2)
        profit_margin_pct = round((net_profit / revenue) * 100, 2) if revenue > 0 else 0.0
        
        records.append({
            'Transaction_ID': txn_id,
            'Date': date.strftime('%Y-%m-%d'),
            'Product_Category': category,
            'Product_Name': product_name,
            'City': city,
            'Region': region,
            'Customer_Segment': customer_segment,
            'Payment_Method': payment_method,
            'Sales_Rep': sales_rep,
            'Units_Sold': units,
            'Unit_Price': unit_price,
            'Unit_Cost': unit_cost,
            'Revenue': revenue,
            'COGS': cogs,
            'Marketing_Expense': marketing_expense,
            'Shipping_Expense': shipping_expense,
            'Operating_Expense': operating_expense,
            'Total_Expense': total_expense,
            'Net_Profit': net_profit,
            'Profit_Margin_Pct': profit_margin_pct
        })
        
    df = pd.DataFrame(records)
    
    # Save raw CSV
    df.to_csv(RAW_CSV_PATH, index=False)
    print(f"[+] Saved raw CSV dataset ({len(df)} rows) to: {RAW_CSV_PATH}")
    
    # Save raw Excel
    with pd.ExcelWriter(RAW_EXCEL_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sales_Expense_Data', index=False)
        
        # Summary Sheet
        summary_df = df.groupby('Product_Category').agg({
            'Revenue': 'sum',
            'Total_Expense': 'sum',
            'Net_Profit': 'sum',
            'Units_Sold': 'sum'
        }).reset_index()
        summary_df['Profit_Margin_%'] = (summary_df['Net_Profit'] / summary_df['Revenue'] * 100).round(2)
        summary_df.to_excel(writer, sheet_name='Category_Summary', index=False)
        
    print(f"[+] Saved raw Excel dataset with multiple sheets to: {RAW_EXCEL_PATH}")
    return df


def load_raw_data(format_type='csv'):
    """
    Load raw dataset from CSV or Excel file. If files don't exist, generates them.
    
    Args:
        format_type (str): 'csv' or 'excel'
    Returns:
        pd.DataFrame
    """
    ensure_directories()
    if format_type == 'excel':
        if not os.path.exists(RAW_EXCEL_PATH):
            generate_synthetic_data()
        return pd.read_excel(RAW_EXCEL_PATH, sheet_name='Sales_Expense_Data')
    else:
        if not os.path.exists(RAW_CSV_PATH):
            generate_synthetic_data()
        return pd.read_csv(RAW_CSV_PATH)


def load_processed_data():
    """
    Load processed clean dataset.
    Returns:
        pd.DataFrame
    """
    if os.path.exists(PROCESSED_CSV_PATH):
        df = pd.read_csv(PROCESSED_CSV_PATH)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        # Fallback to cleaning raw data
        from data_cleaning import clean_and_transform_data
        raw_df = load_raw_data('csv')
        return clean_and_transform_data(raw_df)


def get_sqlite_connection():
    """
    Get SQLite database connection.
    Returns:
        sqlite3.Connection
    """
    ensure_directories()
    conn = sqlite3.connect(DB_PATH)
    return conn


if __name__ == '__main__':
    print("Generating raw datasets...")
    df = generate_synthetic_data(num_records=1200)
    print(df.head())
