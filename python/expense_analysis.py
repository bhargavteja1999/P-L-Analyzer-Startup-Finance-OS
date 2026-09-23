"""
Expense Analysis Module for AI-Expense-Sales-Analyzer.
Evaluates cost structures, expense breakdowns (COGS, Marketing, Shipping, Operating), ratios, and anomaly flags.
"""

import pandas as pd
import numpy as np
try:
    from python.data_loader import load_processed_data
except ModuleNotFoundError:
    from data_loader import load_processed_data


class ExpenseAnalyzer:
    def __init__(self, df=None):
        self.df = df if df is not None else load_processed_data()

    def get_expense_breakdown(self):
        """Returns overall expense component metrics."""
        total_revenue = float(self.df['Revenue'].sum())
        cogs = float(self.df['COGS'].sum())
        marketing = float(self.df['Marketing_Expense'].sum())
        shipping = float(self.df['Shipping_Expense'].sum())
        operating = float(self.df['Operating_Expense'].sum())
        total_expense = float(self.df['Total_Expense'].sum())
        
        return {
            'total_expense': total_expense,
            'cogs': cogs,
            'marketing_expense': marketing,
            'shipping_expense': shipping,
            'operating_expense': operating,
            'cogs_share_pct': round((cogs / total_expense) * 100, 2) if total_expense > 0 else 0,
            'marketing_share_pct': round((marketing / total_expense) * 100, 2) if total_expense > 0 else 0,
            'shipping_share_pct': round((shipping / total_expense) * 100, 2) if total_expense > 0 else 0,
            'operating_share_pct': round((operating / total_expense) * 100, 2) if total_expense > 0 else 0,
            'expense_to_revenue_ratio_pct': round((total_expense / total_revenue) * 100, 2) if total_revenue > 0 else 0
        }

    def analyze_expenses_by_category(self):
        """Aggregates expenses across product categories."""
        grouped = self.df.groupby('Product_Category').agg(
            Total_Revenue=('Revenue', 'sum'),
            COGS=('COGS', 'sum'),
            Marketing_Expense=('Marketing_Expense', 'sum'),
            Shipping_Expense=('Shipping_Expense', 'sum'),
            Operating_Expense=('Operating_Expense', 'sum'),
            Total_Expense=('Total_Expense', 'sum')
        ).reset_index()
        
        grouped['Expense_Ratio_%'] = (grouped['Total_Expense'] / grouped['Total_Revenue'] * 100).round(2)
        grouped['Marketing_Ratio_%'] = (grouped['Marketing_Expense'] / grouped['Total_Revenue'] * 100).round(2)
        return grouped.sort_values(by='Total_Expense', ascending=False)

    def analyze_expenses_by_region(self):
        """Aggregates expenses across geographical regions."""
        grouped = self.df.groupby('Region').agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Expense=('Total_Expense', 'sum'),
            Marketing_Expense=('Marketing_Expense', 'sum'),
            Shipping_Expense=('Shipping_Expense', 'sum'),
            Operating_Expense=('Operating_Expense', 'sum')
        ).reset_index()
        
        grouped['Expense_Ratio_%'] = (grouped['Total_Expense'] / grouped['Total_Revenue'] * 100).round(2)
        return grouped.sort_values(by='Total_Expense', ascending=False)

    def detect_expense_anomalies(self, threshold_std=2.0):
        """
        Identifies transactions where Expense Ratio % exceeds mean + threshold * std.
        Returns:
            pd.DataFrame: High expense ratio transactions
        """
        mean_ratio = self.df['Expense_Ratio_Pct'].mean()
        std_ratio = self.df['Expense_Ratio_Pct'].std()
        cutoff = mean_ratio + (threshold_std * std_ratio)
        
        anomalies = self.df[self.df['Expense_Ratio_Pct'] > cutoff].copy()
        anomalies['Anomaly_Reason'] = f"Expense Ratio > {cutoff:.2f}% (Mean: {mean_ratio:.2f}%)"
        return anomalies[['Transaction_ID', 'Date', 'Product_Name', 'City', 'Revenue', 'Total_Expense', 'Expense_Ratio_Pct', 'Net_Profit', 'Anomaly_Reason']].sort_values(by='Expense_Ratio_Pct', ascending=False)


if __name__ == '__main__':
    analyzer = ExpenseAnalyzer()
    print("Expense Breakdown:", analyzer.get_expense_breakdown())
