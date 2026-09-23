# 📄 Data Analysis Report - AI Expense & Sales Analyzer

## Executive Summary
This report provides a comprehensive empirical analysis of transactional sales, operating expenses, cost of goods sold (COGS), profit margins, and regional dynamics for the **AI-Expense-Sales-Analyzer** project across 1,200 recorded transactions spanning 2024 to 2026.

---

## 1. Key Performance Highlights

| Financial Metric | Total Value ($ USD) | Metric Share / Notes |
| :--- | :--- | :--- |
| **Gross Revenue** | **$14,494,612.58** | 1,200 Total Transactions |
| **Total Expenses** | **$8,953,412.39** | Expense Ratio: **61.77%** |
| **COGS** | **$6,095,811.52** | 68.08% of Total Expenses |
| **Marketing Expense** | **$1,440,148.54** | 9.94% of Total Revenue |
| **Operating Overhead** | **$1,295,389.95** | 14.47% of Total Expenses |
| **Shipping Costs** | **$122,062.38** | 1.36% of Total Expenses |
| **Net Profit** | **$5,541,200.19** | **38.23% Net Profit Margin** |
| **Average Order Value**| **$12,078.84** | Median: $5,675.68 |

---

## 2. Product Category Performance

| Product Category | Revenue ($) | Total Expenses ($) | Net Profit ($) | Net Margin % | Units Sold |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Services** | $5,639,759.50 | $2,789,951.04 | $2,849,808.46 | **50.53%** | 3,923 |
| **Hardware** | $3,583,928.79 | $2,993,421.32 | $590,507.47 | 16.48% | 2,752 |
| **Software** | $2,583,618.91 | $1,045,392.18 | $1,538,226.73 | **59.54%** | 2,341 |
| **Electronics** | $1,805,420.88 | $1,349,602.85 | $455,818.03 | 25.25% | 2,860 |
| **Office Supplies**| $881,884.50 | $775,045.00 | $106,839.50 | 12.11% | 2,716 |

### Insights & Findings
- **Services** and **Software** are the primary growth drivers, yielding net profit margins exceeding **50%** due to lower direct COGS.
- **Hardware** generates significant top-line revenue ($3.58M) but incurs high COGS ($2.4M+), resulting in a compressed margin of **16.48%**.

---

## 3. Geographical & Regional Analysis

| Region | Revenue ($) | Expenses ($) | Net Profit ($) | Net Margin % | Transactions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **West** | $5,681,017.04 | $3,486,301.82 | $2,194,715.22 | **38.63%** | 468 |
| **East** | $3,803,115.10 | $2,388,485.40 | $1,414,629.70 | 37.20% | 314 |
| **South** | $2,764,980.12 | $1,710,502.90 | $1,054,477.22 | 38.14% | 231 |
| **Midwest** | $2,245,500.32 | $1,368,122.27 | $877,378.05 | 39.07% | 187 |

---

## 4. Financial Anomaly Audit
Using standard deviation thresholding (`Expense Ratio > Mean + 2 * Std`), **48 transactions** were flagged as high-cost anomalies, where expenses absorbed over 75% of transaction revenue. These anomalies are primarily concentrated in discounted hardware bundles and expedited shipping requests.
