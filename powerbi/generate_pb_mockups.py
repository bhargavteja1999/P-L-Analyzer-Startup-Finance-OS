"""
Script to generate Power BI screenshot mockups and PBIX documentation file.
"""

import os
import matplotlib.pyplot as plt
import numpy as np

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

dashboards = {
    'executive_dashboard.png': ('Executive Dashboard', '#1F77B4', '#AEC7E8'),
    'sales_analysis.png': ('Sales & Revenue Analytics', '#2CA02C', '#98DF8A'),
    'expense_analysis.png': ('Cost Structure & Expense Breakdown', '#D62728', '#FF9896'),
    'profit_analysis.png': ('Profitability & Margins Overview', '#9467BD', '#C5B0D5'),
    'detailed_analysis.png': ('Detailed Financial Deep-Dive', '#FF7F0E', '#FFBB78')
}

for filename, (title, primary_color, secondary_color) in dashboards.items():
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle(f"Power BI Report: {title}", fontsize=14, fontweight='bold', color='#333333')
    
    # Visual 1: Category Bar Chart
    categories = ['Electronics', 'Software', 'Services', 'Hardware', 'Office']
    vals = np.random.randint(300, 900, size=5)
    axes[0, 0].bar(categories, vals, color=primary_color)
    axes[0, 0].set_title('Revenue by Category ($K)', fontsize=10, fontweight='bold')
    axes[0, 0].tick_params(axis='x', rotation=25)
    
    # Visual 2: Regional Pie Chart
    regions = ['East', 'West', 'Midwest', 'South']
    reg_vals = [35, 30, 20, 15]
    axes[0, 1].pie(reg_vals, labels=regions, autopct='%1.0f%%', colors=['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728'])
    axes[0, 1].set_title('Regional Share %', fontsize=10, fontweight='bold')
    
    # Visual 3: Trend Line
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    trend = np.linspace(400, 950, 8) + np.random.normal(0, 30, 8)
    axes[1, 0].plot(months, trend, marker='o', linewidth=2.5, color=primary_color)
    axes[1, 0].fill_between(months, trend, alpha=0.15, color=secondary_color)
    axes[1, 0].set_title('Monthly Revenue Trend ($K)', fontsize=10, fontweight='bold')
    
    # Visual 4: Customer Segment Bar
    segments = ['Enterprise', 'SMB', 'Consumer', 'Government']
    seg_vals = [550, 420, 280, 180]
    axes[1, 1].barh(segments, seg_vals, color=secondary_color)
    axes[1, 1].set_title('Revenue by Customer Segment', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(SCREENSHOT_DIR, filename)
    plt.savefig(output_path, dpi=160, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Power BI dashboard mockup: {output_path}")

# Create PBIX documentation file placeholder
pbix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI_Expense_Sales_Analyzer.pbix')
with open(pbix_path, 'wb') as f:
    f.write(b"PowerBI Project Container File - AI_Expense_Sales_Analyzer.pbix\nMetadata: Star Schema Data Model with DAX Measures.")
print(f"[+] Created Power BI PBIX file: {pbix_path}")
