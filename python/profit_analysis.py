"""
Profit Analysis Module for AI-Expense-Sales-Analyzer.
Evaluates Net Profit, Gross Margin, Profit Margins by dimension, profitability tiers, and loss-making items.
"""

import pandas as pd
import numpy as np
try:
    from python.data_loader import load_processed_data
except ModuleNotFoundError:
    from data_loader import load_processed_data


class ProfitAnalyzer:
    def __init__(self, df=None):
        self.df = df if df is not None else load_processed_data()

    def get_profit_overview(self):
        """Returns overall profit metrics."""
        total_rev = float(self.df['Revenue'].sum())
        gross_prof = float(self.df['Gross_Profit'].sum())
        net_prof = float(self.df['Net_Profit'].sum())
        
        return {
            'total_revenue': total_rev,
            'gross_profit': gross_prof,
            'net_profit': net_prof,
            'gross_margin_pct': round((gross_prof / total_rev) * 100, 2) if total_rev > 0 else 0,
            'net_margin_pct': round((net_prof / total_rev) * 100, 2) if total_rev > 0 else 0,
            'avg_profit_per_transaction': round(self.df['Net_Profit'].mean(), 2),
            'max_profit_transaction': float(self.df['Net_Profit'].max()),
            'min_profit_transaction': float(self.df['Net_Profit'].min())
        }

    def analyze_profit_by_category(self):
        """Calculates profit margins by product category."""
        grouped = self.df.groupby('Product_Category').agg(
            Total_Revenue=('Revenue', 'sum'),
            Gross_Profit=('Gross_Profit', 'sum'),
            Total_Expense=('Total_Expense', 'sum'),
            Net_Profit=('Net_Profit', 'sum')
        ).reset_index()
        
        grouped['Gross_Margin_%'] = (grouped['Gross_Profit'] / grouped['Total_Revenue'] * 100).round(2)
        grouped['Net_Margin_%'] = (grouped['Net_Profit'] / grouped['Total_Revenue'] * 100).round(2)
        return grouped.sort_values(by='Net_Profit', ascending=False)

    def analyze_profit_by_city(self):
        """Calculates profit margins by city and region."""
        grouped = self.df.groupby(['City', 'Region']).agg(
            Total_Revenue=('Revenue', 'sum'),
            Net_Profit=('Net_Profit', 'sum'),
            Transaction_Count=('Transaction_ID', 'count')
        ).reset_index()
        
        grouped['Net_Margin_%'] = (grouped['Net_Profit'] / grouped['Total_Revenue'] * 100).round(2)
        return grouped.sort_values(by='Net_Profit', ascending=False)

    def analyze_profitability_tiers(self):
        """Breakdown of transactions by profitability tier."""
        tier_df = self.df.groupby('Profitability_Tier').agg(
            Transaction_Count=('Transaction_ID', 'count'),
            Total_Revenue=('Revenue', 'sum'),
            Total_Net_Profit=('Net_Profit', 'sum')
        ).reset_index()
        tier_df['Transaction_Share_%'] = (tier_df['Transaction_Count'] / len(self.df) * 100).round(2)
        return tier_df

    def get_most_and_least_profitable_products(self, n=5):
        """Returns top N most profitable and bottom N least profitable products."""
        prod_df = self.df.groupby('Product_Name').agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Expense=('Total_Expense', 'sum'),
            Net_Profit=('Net_Profit', 'sum')
        ).reset_index()
        prod_df['Net_Margin_%'] = (prod_df['Net_Profit'] / prod_df['Total_Revenue'] * 100).round(2)
        
        top_n = prod_df.sort_values(by='Net_Profit', ascending=False).head(n)
        bottom_n = prod_df.sort_values(by='Net_Profit', ascending=True).head(n)
        return top_n, bottom_n


if __name__ == '__main__':
    analyzer = ProfitAnalyzer()
    print("Profit Overview:", analyzer.get_profit_overview())
