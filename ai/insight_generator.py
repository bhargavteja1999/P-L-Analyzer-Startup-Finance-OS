"""
Automated Insight Generator Module for AI-Expense-Sales-Analyzer.
Generates comprehensive narrative financial insights and executive reports.
"""

import os
import sys

# Add parent dir to sys path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.data_loader import load_processed_data
from python.eda import generate_eda_summary
from ai.ai_assistant import FinancialAIAssistant


def generate_executive_insights():
    """
    Generates structured executive insights formatted as Markdown.
    """
    df = load_processed_data()
    stats = generate_eda_summary(df)
    
    top_cat = stats['category_summary'][0]
    top_region = stats['region_summary'][0]
    highest_margin_cat = max(stats['category_summary'], key=lambda x: x['Profit_Margin_Pct'])
    lowest_margin_cat = min(stats['category_summary'], key=lambda x: x['Profit_Margin_Pct'])
    
    report = f"""# 📈 AI Executive Insight Report - Expense & Sales Analysis

## 1. Financial Health & High-Level KPIs
- **Total Revenue:** ${stats['total_revenue']:,.2f}
- **Total Expenses:** ${stats['total_expense']:,.2f} (Expense Ratio: {(stats['total_expense']/stats['total_revenue']*100):.2f}%)
- **Net Profit:** ${stats['total_net_profit']:,.2f} (**{stats['overall_profit_margin_pct']}%** Net Margin)
- **Total Transactions:** {stats['total_transactions']:,}
- **Average Order Value:** ${stats['avg_order_value']:,.2f}

---

## 2. Key Revenue Drivers & Growth Highlights
- **Top Product Category:** **{top_cat['Product_Category']}** led revenue generation at **${top_cat['Revenue']:,.2f}**, contributing **{(top_cat['Revenue']/stats['total_revenue']*100):.1f}%** of total sales.
- **Top Geographical Region:** **{top_region['Region']}** generated **${top_region['Revenue']:,.2f}** in revenue with a **{top_region['Profit_Margin_Pct']}%** profit margin.
- **Most Profitable Line:** **{highest_margin_cat['Product_Category']}** yielded the highest net margin percentage at **{highest_margin_cat['Profit_Margin_Pct']}%**.

---

## 3. Expense Analysis & Risk Warnings
- **COGS Share:** Cost of Goods Sold accounts for **${stats['total_cogs']:,.2f}** ({(stats['total_cogs']/stats['total_expense']*100):.1f}% of total expense).
- **Marketing Spend:** Total marketing expenditure reached **${stats['total_marketing']:,.2f}** ({(stats['total_marketing']/stats['total_revenue']*100):.2f}% of total revenue).
- **Underperforming Category:** **{lowest_margin_cat['Product_Category']}** experienced lower profit margins (**{lowest_margin_cat['Profit_Margin_Pct']}%**), requiring vendor cost negotiation or price recalibration.

---

## 4. Strategic Recommendations
1. **Reallocate Marketing Budget:** Shift 15% of marketing spend from low-margin items to **{highest_margin_cat['Product_Category']}**.
2. **Logistics Optimization:** Standardize shipping rates across regional distribution centers to reduce logistics costs.
3. **Enterprise Sales Expansion:** Focus sales reps on enterprise customer contracts to boost average order value.
"""
    return report


if __name__ == '__main__':
    insights = generate_executive_insights()
    print(insights)
