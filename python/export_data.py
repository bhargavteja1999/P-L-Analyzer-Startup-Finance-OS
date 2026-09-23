"""
Export & Database Sync Module for AI-Expense-Sales-Analyzer.
Populates SQLite database tables and exports JSON summary statistics.
"""

import os
import json
import sqlite3
import pandas as pd
try:
    from python.data_loader import load_processed_data, get_sqlite_connection, BASE_DIR
    from python.eda import generate_eda_summary
except ModuleNotFoundError:
    from data_loader import load_processed_data, get_sqlite_connection, BASE_DIR
    from eda import generate_eda_summary


def export_to_sqlite(df=None):
    """
    Exports cleaned dataset to SQLite database tables.
    """
    if df is None:
        df = load_processed_data()
        
    conn = get_sqlite_connection()
    
    # 1. Main transactions table
    df.to_sql('sales_expenses', conn, if_exists='replace', index=False)
    
    # 2. Product dimension
    products_df = df[['Product_Name', 'Product_Category', 'Unit_Price', 'Unit_Cost']].drop_duplicates().reset_index(drop=True)
    products_df.to_sql('products_dim', conn, if_exists='replace', index=False)
    
    # 3. City & Region dimension
    cities_df = df[['City', 'Region']].drop_duplicates().reset_index(drop=True)
    cities_df.to_sql('cities_dim', conn, if_exists='replace', index=False)
    
    # 4. Monthly Aggregates (real P&L)
    agg_cols = {
        'Revenue': 'sum',
        'Net_Revenue': 'sum',
        'COGS': 'sum',
        'Gross_Profit': 'sum',
        'Total_Operating_Expense': 'sum',
        'EBITDA': 'sum',
        'Depreciation': 'sum',
        'EBIT': 'sum',
        'Interest_Expense': 'sum',
        'EBT': 'sum',
        'Tax_Amount': 'sum',
        'PAT': 'sum',
        'Net_Profit': 'sum',
        'Total_Expense': 'sum',
        'Units_Sold': 'sum',
        'Transaction_ID': 'count'
    }
    # Only include cols that exist
    agg_available = {k: v for k, v in agg_cols.items() if k in df.columns}
    monthly_df = df.groupby('Year_Month').agg(agg_available).reset_index()
    monthly_df.to_sql('monthly_summary', conn, if_exists='replace', index=False)

    # 5. P&L Summary view (for PowerBI/SQL)
    try:
        pnl_df = df.agg({
            'Revenue': 'sum',
            'Discount_Amount': 'sum',
            'Net_Revenue': 'sum',
            'COGS': 'sum',
            'Gross_Profit': 'sum',
            'Marketing_Expense': 'sum',
            'Shipping_Expense': 'sum',
            'Employee_Cost': 'sum',
            'Rent_Admin_Cost': 'sum',
            'Total_Operating_Expense': 'sum',
            'EBITDA': 'sum',
            'Depreciation': 'sum',
            'EBIT': 'sum',
            'Interest_Expense': 'sum',
            'Other_Income': 'sum',
            'EBT': 'sum',
            'Tax_Amount': 'sum',
            'PAT': 'sum'
        }).to_frame(name='Total').reset_index().rename(columns={'index':'Line_Item'})
        pnl_df.to_sql('pnl_summary', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"[!] pnl_summary skipped: {e}")
    
    conn.commit()
    conn.close()
    print("[+] Successfully exported data to SQLite database tables.")


def export_summary_json():
    """
    Exports high-level EDA and financial summary stats to a JSON file.
    """
    stats = generate_eda_summary()
    json_path = os.path.join(BASE_DIR, 'data', 'processed', 'summary_metrics.json')
    
    with open(json_path, 'w') as f:
        json.dump(stats, f, indent=4)
        
    print(f"[+] Successfully exported summary metrics to: {json_path}")


if __name__ == '__main__':
    export_to_sqlite()
    export_summary_json()
