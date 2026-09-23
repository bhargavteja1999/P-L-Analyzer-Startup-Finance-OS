"""
Data Cleaning & Transformation Module for AI-Expense-Sales-Analyzer.
Processes raw dataset, performs validation, feature engineering, and exports cleaned dataset.
"""

import os
import pandas as pd
import numpy as np
try:
    from python.data_loader import load_raw_data, PROCESSED_CSV_PATH, ensure_directories
except ModuleNotFoundError:
    from data_loader import load_raw_data, PROCESSED_CSV_PATH, ensure_directories


def clean_and_transform_data(df=None):
    """
    Cleans raw DataFrame, handles missing values, casts data types,
    and performs feature engineering.
    
    Args:
        df (pd.DataFrame, optional): Raw data. If None, loads from raw CSV.
    Returns:
        pd.DataFrame: Cleaned & transformed DataFrame
    """
    if df is None:
        df = load_raw_data('csv')
        
    print("[*] Starting Data Cleaning and Transformation Pipeline...")
    
    # 1. Deduplication
    initial_rows = len(df)
    df = df.drop_duplicates(subset=['Transaction_ID'])
    dedup_count = initial_rows - len(df)
    if dedup_count > 0:
        print(f"    - Removed {dedup_count} duplicate rows.")
        
    # 2. Date parsing & temporal features
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%b')
    df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
    df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
    df['Day_of_Week'] = df['Date'].dt.day_name()
    
    # 3. Numeric type validation & cleaning
    numeric_cols = [
        'Units_Sold', 'Unit_Price', 'Unit_Cost', 'Revenue', 'COGS',
        'Marketing_Expense', 'Shipping_Expense', 'Operating_Expense',
        'Total_Expense', 'Net_Profit', 'Profit_Margin_Pct'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    # String columns clean
    str_cols = ['Product_Category', 'Product_Name', 'City', 'Region', 'Customer_Segment', 'Payment_Method', 'Sales_Rep']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    # 4. Feature Engineering — REAL COMPANY P&L (Schedule III / Ind AS style) in USD base (converted to ₹ in dashboard ×83)
    # Base Sales
    df['Revenue'] = (df['Units_Sold'] * df['Unit_Price']).round(2)  # Gross Sales (Net of GST in base)
    df['COGS'] = (df['Units_Sold'] * df['Unit_Cost']).round(2)
    df['Gross_Profit'] = (df['Revenue'] - df['COGS']).round(2)

    # --- Real expense split (if Operating_Expense exists, split; else generate) ---
    # Keep Marketing/Shipping as is, split Operating into Employee + Rent/Admin, add Depreciation & Interest
    # Employee Benefits (salaries) ~ 8-12% of Revenue
    np.random.seed(42)
    if 'Employee_Cost' not in df.columns or df['Employee_Cost'].isna().all() if 'Employee_Cost' in df.columns else True:
        df['Employee_Cost'] = np.where(df['Revenue']>0, (df['Revenue'] * np.random.uniform(0.07, 0.12, len(df))).round(2), 0.0)
    if 'Rent_Admin_Cost' not in df.columns or df['Rent_Admin_Cost'].isna().all() if 'Rent_Admin_Cost' in df.columns else True:
        # Use existing Operating_Expense as base if present, else 4-7% of Revenue
        base_op = df['Operating_Expense'] if 'Operating_Expense' in df.columns else df['Revenue']*0.08
        df['Rent_Admin_Cost'] = np.where(df['Revenue']>0, (np.maximum(base_op*0.4, df['Revenue']*0.03)).round(2), 0.0)
        # Adjust Operating to be Rent part only for transparency (keep original for backward compat)
        # df['Operating_Expense'] remains as Rent/Admin portion for legacy charts
        df['Operating_Expense'] = df['Rent_Admin_Cost']

    # Discount / Sales Return ~ 1-3% (reduces Net Revenue)
    df['Discount_Amount'] = (df['Revenue'] * np.random.uniform(0.01, 0.03, len(df))).round(2)
    df['Net_Revenue'] = (df['Revenue'] - df['Discount_Amount']).round(2)

    # GST collected (18% typical; shown separately, not subtracted from P&L Net_Revenue which is ex-GST)
    df['GST_Rate_Pct'] = 18.0
    df['GST_Amount'] = (df['Net_Revenue'] * 0.18).round(2)

    # Depreciation (SLM ~ 1.5-2.5% of Revenue as proxy for asset base) + Interest (1-2% of Revenue)
    df['Depreciation'] = (df['Revenue'] * np.random.uniform(0.015, 0.025, len(df))).round(2)
    df['Interest_Expense'] = (df['Revenue'] * np.random.uniform(0.01, 0.02, len(df))).round(2)
    df['Other_Income'] = (df['Revenue'] * np.random.uniform(0.002, 0.008, len(df))).round(2)

    # Legacy Total_Expense (for backward charts) = COGS + Marketing + Shipping + Rent/Admin
    df['Total_Expense'] = (df['COGS'] + df['Marketing_Expense'] + df['Shipping_Expense'] + df['Rent_Admin_Cost']).round(2)
    # Real Operating Expense = Marketing + Shipping + Employee + Rent/Admin
    df['Total_Operating_Expense'] = (df['Marketing_Expense'] + df['Shipping_Expense'] + df['Employee_Cost'] + df['Rent_Admin_Cost']).round(2)

    # Real P&L chain
    df['EBITDA'] = (df['Gross_Profit'] - df['Total_Operating_Expense']).round(2)  # Gross - Operating
    df['EBIT'] = (df['EBITDA'] - df['Depreciation']).round(2)
    df['EBT'] = (df['EBIT'] - df['Interest_Expense'] + df['Other_Income']).round(2)
    # Indian Corporate Tax: 22% new regime (if EBT >0), else 0 + 4% cess approx included
    df['Tax_Rate_Pct'] = 22.0
    df['Tax_Amount'] = np.where(df['EBT'] > 0, (df['EBT'] * 0.22).round(2), 0.0)
    df['PAT'] = (df['EBT'] - df['Tax_Amount']).round(2)  # Profit After Tax — real bottom line
    # Keep Net_Profit as PAT for backward compat (old Net_Profit = EBT-like, now PAT is correct)
    df['Net_Profit'] = df['PAT']

    # Correct Gross uses Net_Revenue
    df['Gross_Profit'] = (df['Net_Revenue'] - df['COGS']).round(2)
    # Recompute EBITDA/EBIT/EBT with corrected Gross
    df['EBITDA'] = (df['Gross_Profit'] - df['Total_Operating_Expense']).round(2)
    df['EBIT'] = (df['EBITDA'] - df['Depreciation']).round(2)
    df['EBT'] = (df['EBIT'] - df['Interest_Expense'] + df['Other_Income']).round(2)
    df['Tax_Amount'] = np.where(df['EBT'] > 0, (df['EBT'] * 0.22).round(2), 0.0)
    df['PAT'] = (df['EBT'] - df['Tax_Amount']).round(2)
    df['Net_Profit'] = df['PAT']

    # Profit Margin & Ratios (now on Net_Revenue and PAT)
    df['Profit_Margin_Pct'] = np.where(df['Net_Revenue'] > 0, (df['PAT'] / df['Net_Revenue']) * 100, 0.0).round(2)
    df['PAT_Margin_Pct'] = df['Profit_Margin_Pct']
    df['EBITDA_Margin_Pct'] = np.where(df['Net_Revenue'] > 0, (df['EBITDA'] / df['Net_Revenue']) * 100, 0.0).round(2)
    df['EBIT_Margin_Pct'] = np.where(df['Net_Revenue'] > 0, (df['EBIT'] / df['Net_Revenue']) * 100, 0.0).round(2)
    df['EBT_Margin_Pct'] = np.where(df['Net_Revenue'] > 0, (df['EBT'] / df['Net_Revenue']) * 100, 0.0).round(2)
    df['Gross_Margin_Pct'] = np.where(df['Net_Revenue'] > 0, (df['Gross_Profit'] / df['Net_Revenue']) * 100, 0.0).round(2)
    df['Expense_Ratio_Pct'] = np.where(df['Revenue'] > 0, (df['Total_Expense'] / df['Revenue']) * 100, 0.0).round(2)
    df['Marketing_Ratio_Pct'] = np.where(df['Revenue'] > 0, (df['Marketing_Expense'] / df['Revenue']) * 100, 0.0).round(2)
    
    # Unit level metrics (on Net_Revenue / PAT)
    df['Revenue_Per_Unit'] = np.where(df['Units_Sold'] > 0, df['Net_Revenue'] / df['Units_Sold'], 0.0).round(2)
    df['Expense_Per_Unit'] = np.where(df['Units_Sold'] > 0, df['Total_Expense'] / df['Units_Sold'], 0.0).round(2)
    df['Profit_Per_Unit'] = np.where(df['Units_Sold'] > 0, df['PAT'] / df['Units_Sold'], 0.0).round(2)
    
    # Performance Categorization
    conditions = [
        (df['Profit_Margin_Pct'] >= 20.0),
        (df['Profit_Margin_Pct'] >= 5.0) & (df['Profit_Margin_Pct'] < 20.0),
        (df['Profit_Margin_Pct'] >= 0.0) & (df['Profit_Margin_Pct'] < 5.0),
        (df['Profit_Margin_Pct'] < 0.0)
    ]
    choices = ['High Margin (>=20%)', 'Moderate Margin (5-20%)', 'Low Margin (0-5%)', 'Loss Making (<0%)']
    df['Profitability_Tier'] = np.select(conditions, choices, default='Unknown')
    
    # Sort chronologically
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    # Save cleaned data
    ensure_directories()
    df.to_csv(PROCESSED_CSV_PATH, index=False)
    print(f"[+] Cleaned dataset saved successfully ({len(df)} rows) to: {PROCESSED_CSV_PATH}")
    
    return df


if __name__ == '__main__':
    cleaned_df = clean_and_transform_data()
    print("Cleaned Data Summary:")
    print(cleaned_df.info())
