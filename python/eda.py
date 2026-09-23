"""
Exploratory Data Analysis (EDA) Module for AI-Expense-Sales-Analyzer.
Generates comprehensive statistical summaries, distribution metrics, correlation matrices, and data insights.
"""

import pandas as pd
import numpy as np
try:
    from python.data_loader import load_processed_data
except ModuleNotFoundError:
    from data_loader import load_processed_data


def generate_eda_summary(df=None):
    """
    Computes statistical metrics and descriptive insights for the dataset.
    
    Args:
        df (pd.DataFrame, optional): Processed dataset.
    Returns:
        dict: High-level EDA statistics dictionary.
    """
    if df is None:
        df = load_processed_data()
        
    stats = {}
    
    # 1. Dataset Overview
    stats['total_transactions'] = int(len(df))
    stats['date_min'] = str(df['Date'].min().strftime('%Y-%m-%d'))
    stats['date_max'] = str(df['Date'].max().strftime('%Y-%m-%d'))
    stats['total_revenue'] = float(df['Revenue'].sum())
    stats['total_expense'] = float(df['Total_Expense'].sum())
    stats['total_cogs'] = float(df['COGS'].sum())
    stats['total_marketing'] = float(df['Marketing_Expense'].sum())
    stats['total_shipping'] = float(df['Shipping_Expense'].sum())
    stats['total_operating'] = float(df['Operating_Expense'].sum())
    stats['total_net_profit'] = float(df['Net_Profit'].sum())
    stats['overall_profit_margin_pct'] = float(round((stats['total_net_profit'] / stats['total_revenue']) * 100, 2))
    
    # 2. Key Averages & Distributions
    stats['avg_order_value'] = float(round(df['Revenue'].mean(), 2))
    stats['median_order_value'] = float(round(df['Revenue'].median(), 2))
    stats['avg_profit_per_order'] = float(round(df['Net_Profit'].mean(), 2))
    stats['total_units_sold'] = int(df['Units_Sold'].sum())
    
    # 3. Category Breakdown
    cat_summary = df.groupby('Product_Category').agg({
        'Revenue': 'sum',
        'Total_Expense': 'sum',
        'Net_Profit': 'sum',
        'Units_Sold': 'sum'
    }).reset_index()
    cat_summary['Profit_Margin_Pct'] = (cat_summary['Net_Profit'] / cat_summary['Revenue'] * 100).round(2)
    stats['category_summary'] = cat_summary.sort_values(by='Revenue', ascending=False).to_dict(orient='records')
    
    # 4. Regional Breakdown
    region_summary = df.groupby('Region').agg({
        'Revenue': 'sum',
        'Total_Expense': 'sum',
        'Net_Profit': 'sum',
        'Transaction_ID': 'count'
    }).rename(columns={'Transaction_ID': 'Transaction_Count'}).reset_index()
    region_summary['Profit_Margin_Pct'] = (region_summary['Net_Profit'] / region_summary['Revenue'] * 100).round(2)
    stats['region_summary'] = region_summary.sort_values(by='Revenue', ascending=False).to_dict(orient='records')
    
    # 5. Customer Segment Summary
    segment_summary = df.groupby('Customer_Segment').agg({
        'Revenue': 'sum',
        'Net_Profit': 'sum',
        'Units_Sold': 'sum'
    }).reset_index()
    stats['segment_summary'] = segment_summary.to_dict(orient='records')
    
    # 6. Monthly Growth & Dynamics
    monthly = df.groupby('Year_Month').agg({
        'Revenue': 'sum',
        'Total_Expense': 'sum',
        'Net_Profit': 'sum'
    }).reset_index()
    monthly['MoM_Revenue_Growth_%'] = monthly['Revenue'].pct_change().fillna(0).round(4) * 100
    stats['monthly_summary'] = monthly.to_dict(orient='records')
    
    # 7. Correlation matrix
    numeric_df = df[['Revenue', 'COGS', 'Marketing_Expense', 'Shipping_Expense', 'Operating_Expense', 'Total_Expense', 'Net_Profit', 'Units_Sold']]
    stats['correlation_matrix'] = numeric_df.corr().round(3).to_dict()
    
    return stats


def print_eda_report():
    """Prints formatted EDA summary to console."""
    stats = generate_eda_summary()
    print("=" * 60)
    print("           EXPLORATORY DATA ANALYSIS REPORT           ")
    print("=" * 60)
    print(f"Total Transactions: {stats['total_transactions']:,}")
    print(f"Date Range        : {stats['date_min']} to {stats['date_max']}")
    print(f"Total Revenue     : ${stats['total_revenue']:,.2f}")
    print(f"Total Expenses    : ${stats['total_expense']:,.2f}")
    print(f"Net Profit        : ${stats['total_net_profit']:,.2f}")
    print(f"Overall Margin    : {stats['overall_profit_margin_pct']}%")
    print(f"Average Order Val : ${stats['avg_order_value']:,.2f}")
    print("-" * 60)
    print("\n[+] Category Summary:")
    for cat in stats['category_summary']:
        print(f"  - {cat['Product_Category']:<18}: Rev=${cat['Revenue']:>10,.2f} | Exp=${cat['Total_Expense']:>10,.2f} | Margin={cat['Profit_Margin_Pct']:>6.2f}%")
    print("\n[+] Regional Summary:")
    for reg in stats['region_summary']:
        print(f"  - {reg['Region']:<10}: Rev=${reg['Revenue']:>10,.2f} | Net=${reg['Net_Profit']:>10,.2f} | Margin={reg['Profit_Margin_Pct']:>6.2f}%")
    print("=" * 60)


if __name__ == '__main__':
    print_eda_report()
