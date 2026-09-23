"""
Sales Analysis Module for AI-Expense-Sales-Analyzer.
Performs in-depth analysis of sales performance, revenue trends, top products, sales reps, and customer segments.
"""

import pandas as pd
import numpy as np
try:
    from python.data_loader import load_processed_data
except ModuleNotFoundError:
    from data_loader import load_processed_data


class SalesAnalyzer:
    def __init__(self, df=None):
        self.df = df if df is not None else load_processed_data()

    def get_sales_overview(self):
        """Returns overall sales metrics."""
        return {
            'total_revenue': float(self.df['Revenue'].sum()),
            'total_units_sold': int(self.df['Units_Sold'].sum()),
            'total_transactions': int(len(self.df)),
            'avg_transaction_value': float(round(self.df['Revenue'].mean(), 2)),
            'max_transaction_value': float(self.df['Revenue'].max()),
            'min_transaction_value': float(self.df['Revenue'].min())
        }

    def analyze_sales_by_category(self):
        """Aggregates sales performance by product category."""
        grouped = self.df.groupby('Product_Category').agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Units=('Units_Sold', 'sum'),
            Transaction_Count=('Transaction_ID', 'count'),
            Avg_Unit_Price=('Unit_Price', 'mean'),
            Avg_Order_Value=('Revenue', 'mean')
        ).reset_index()
        
        grouped['Revenue_Share_%'] = (grouped['Total_Revenue'] / grouped['Total_Revenue'].sum() * 100).round(2)
        return grouped.sort_values(by='Total_Revenue', ascending=False)

    def analyze_top_products(self, top_n=10):
        """Returns top N products by revenue."""
        grouped = self.df.groupby(['Product_Name', 'Product_Category']).agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Units=('Units_Sold', 'sum'),
            Avg_Price=('Unit_Price', 'mean')
        ).reset_index()
        return grouped.sort_values(by='Total_Revenue', ascending=False).head(top_n)

    def analyze_sales_by_region(self):
        """Aggregates sales performance by region and city."""
        region_df = self.df.groupby('Region').agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Units=('Units_Sold', 'sum'),
            Transaction_Count=('Transaction_ID', 'count')
        ).reset_index()
        region_df['Revenue_Share_%'] = (region_df['Total_Revenue'] / region_df['Total_Revenue'].sum() * 100).round(2)
        
        city_df = self.df.groupby(['City', 'Region']).agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Units=('Units_Sold', 'sum')
        ).reset_index().sort_values(by='Total_Revenue', ascending=False)
        
        return region_df.sort_values(by='Total_Revenue', ascending=False), city_df

    def analyze_sales_by_sales_rep(self):
        """Analyzes sales performance across sales representatives."""
        rep_df = self.df.groupby('Sales_Rep').agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Units=('Units_Sold', 'sum'),
            Deals_Closed=('Transaction_ID', 'count'),
            Avg_Deal_Size=('Revenue', 'mean'),
            Net_Profit=('Net_Profit', 'sum')
        ).reset_index()
        rep_df['Profit_Margin_%'] = (rep_df['Net_Profit'] / rep_df['Total_Revenue'] * 100).round(2)
        return rep_df.sort_values(by='Total_Revenue', ascending=False)

    def analyze_monthly_trends(self):
        """Computes month-over-month sales growth rates."""
        monthly = self.df.groupby('Year_Month').agg(
            Monthly_Revenue=('Revenue', 'sum'),
            Monthly_Units=('Units_Sold', 'sum'),
            Transaction_Count=('Transaction_ID', 'count')
        ).reset_index()
        
        monthly['MoM_Revenue_Growth_%'] = monthly['Monthly_Revenue'].pct_change().fillna(0).round(4) * 100
        monthly['Cumulative_Revenue'] = monthly['Monthly_Revenue'].cumsum()
        return monthly

    def analyze_customer_segment(self):
        """Aggregates sales by customer segment."""
        segment_df = self.df.groupby('Customer_Segment').agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Units=('Units_Sold', 'sum'),
            Transaction_Count=('Transaction_ID', 'count'),
            Avg_Order_Value=('Revenue', 'mean')
        ).reset_index()
        segment_df['Share_%'] = (segment_df['Total_Revenue'] / segment_df['Total_Revenue'].sum() * 100).round(2)
        return segment_df.sort_values(by='Total_Revenue', ascending=False)


if __name__ == '__main__':
    analyzer = SalesAnalyzer()
    print("Sales Overview:", analyzer.get_sales_overview())
