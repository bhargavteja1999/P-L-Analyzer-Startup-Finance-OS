# 📊 AI-Expense-Sales-Analyzer

An end-to-end Financial Intelligence, Data Engineering, SQL Analytics, Streamlit Web Dashboard, and AI Assistant system for analyzing sales revenues, operating expenses, cost structures, net profit margins, and predictive business insights.

---

## 📁 Repository Directory Structure

```
AI-Expense-Sales-Analyzer/
│
├── data/
│   ├── raw/
│   │   ├── sales_expense_data.csv          # Raw multi-year sales & expense dataset
│   │   └── sales_expense_data.xlsx         # Multi-sheet Excel workbook
│   │
│   ├── processed/
│   │   ├── cleaned_sales_data.csv       # Processed dataset with engineered financial features
│   │   └── summary_metrics.json          # Pre-computed EDA & summary stats JSON
│   │
│   └── expense_sales.db                    # Relational SQLite database
│
├── python/
│   ├── data_loader.py                      # Data ingestion & synthetic dataset generator
│   ├── data_cleaning.py                    # Data cleaning, feature engineering & ratios
│   ├── eda.py                              # Exploratory data analysis & stats engine
│   ├── sales_analysis.py                   # Category, product, sales rep & regional analytics
│   ├── expense_analysis.py                 # Cost structure, ratio analysis & anomaly detection
│   ├── profit_analysis.py                  # Margin analytics, tiers & top/bottom products
│   └── export_data.py                      # SQLite database sync & JSON exporter
│
├── sql/
│   ├── 01_create_database.sql              # Database initialization & PRAGMA setup
│   ├── 02_create_tables.sql                # Star-Schema DDL (fact & dimension tables)
│   ├── 03_insert_data.sql                  # DML population script
│   ├── 04_basic_analysis.sql               # Baseline count & KPI aggregations
│   ├── 05_sales_analysis.sql               # Sales revenue & rep leaderboard queries
│   ├── 06_expense_analysis.sql             # Expense components & anomaly queries
│   ├── 07_profit_analysis.sql              # Gross & Net margin SQL queries
│   ├── 08_monthly_analysis.sql             # Time-series & quarterly trend queries
│   ├── 09_product_analysis.sql             # Product volume vs revenue analysis
│   ├── 10_city_analysis.sql                # Geographical region & city performance queries
│   └── 11_advanced_analysis.sql            # Window functions (MoM growth, DENSE_RANK, NTILE)
│
├── powerbi/
│   ├── AI_Expense_Sales_Analyzer.pbix      # Power BI project file
│   │
│   └── screenshots/
│       ├── executive_dashboard.png         # Executive dashboard mockup screenshot
│       ├── sales_analysis.png              # Sales analytics mockup screenshot
│       ├── expense_analysis.png            # Expense breakdown mockup screenshot
│       ├── profit_analysis.png             # Profitability mockup screenshot
│       └── detailed_analysis.png           # Detailed matrix deep-dive screenshot
│
├── notebooks/
│   └── exploratory_data_analysis.ipynb     # Interactive Jupyter Notebook for EDA
│
├── ai/
│   ├── ai_assistant.py                     # Financial AI Assistant (Gemini API + Offline engine)
│   ├── prompts.py                          # Structured financial analyst prompts
│   └── insight_generator.py                # Automated executive report generator
│
├── app/
│   └── dashboard.py                        # Multi-tab Streamlit Web Application
│
├── reports/
│   ├── data_analysis_report.md             # Comprehensive data analysis report
│   ├── sql_analysis.md                     # SQL database schema & query documentation
│   ├── powerbi_analysis.md                 # Power BI model & DAX formula guide
│   └── business_insights.md                # Strategic business recommendations
│
├── requirements.txt                        # Python dependencies
├── README.md                               # Project documentation
├── .gitignore                              # Git ignore rules
└── LICENSE                                 # MIT License
```

---

## ⚡ Key Features

1. **Automated Data Engineering Pipeline**: Synthetic multi-year data generator, schema validator, financial feature engineering (Expense Ratio %, Net Profit Margin %, COGS share, Unit metrics).
2. **Relational SQL Analytics**: 11 production-grade SQL scripts featuring Star-Schema layout, DDL/DML, index optimizations, and advanced window functions (`LAG()`, `DENSE_RANK()`, `NTILE()`).
3. **Interactive Streamlit Web Dashboard**:
   - **Executive Overview**: Dynamic KPI cards, monthly revenue/expense area charts, category bars, and regional donut maps.
   - **Sales Analytics**: Top 10 product ranking, sales rep leaderboard, customer segment share.
   - **Expense Breakdown**: Cost component pie charts, category expense ratios, high-cost anomaly table.
   - **Profitability & Margins**: Margin waterfall, profitability tiers, top/bottom product tables.
   - **AI Financial Assistant**: Conversational natural language Q&A and instant executive report generator.
4. **AI Assistant (Dual Engine)**: Supports Google Gemini API / OpenAI API when an API key is present, with an intelligent offline statistical NLP engine when offline.
5. **Power BI Visual Integration**: Power BI report model, DAX measures guide, and 5 high-resolution dashboard screenshots.

---

## 📚 Full Handover Documentation

**New developer? Start here:** [`docs/README.md`](docs/README.md) — command center with audience-based navigation (non-technical → `00_Project_Overview.md`, developer → `03_System_Architecture.md` → `07_Local_Setup_Guide.md`).

Also see: `docs/00_Project_Overview.md` (what it does), `docs/07_Local_Setup_Guide.md` (reproducible setup), `docs/05_API_Documentation.md` (Flask routes), `docs/ai/` (Gemini pipeline), `docs/decisions/` (ADRs).

> **Recent handover changes (2026-09-22):** P&L SaaS now supports `Local`/`SQL`/`MongoDB` (mongomock fallback), Sept revenue `SQL 20000` / `Mongo 30000`, `Load Demo Data` fixed for all modes, Streamlit title `P&L Analyzer | Startup Finance OS v2.0` on `:80`. See `docs/15_Change_Log.md`.

## 🛠️ Quick Start & Execution Guide

### 1. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
pip install -r pnl-analyzer/backend/requirements.txt
```

### 2. Run Data Pipeline & Populate SQLite Database
```bash
python python/data_cleaning.py
python python/export_data.py
```

### 3. Launch the Streamlit Interactive Dashboard
```bash
streamlit run app/dashboard.py --server.port 80
# or default 8501
streamlit run app/dashboard.py
```

### 3b. Launch P&L SaaS (keeps SQLite, optional MongoDB)
```bash
python pnl-analyzer/backend/app.py          # Flask :5000 (health http://localhost:5000/api/health)
python -m http.server 8000 --directory pnl-analyzer/frontend  # Frontend http://localhost:8000
# Data Source dropdown: Local (localStorage) / SQL (pnl.db) / MongoDB (mongomock or MONGO_URI)
# Mongo same demo as SQL: Sept 20000→30000 (see docs/04_Data_Model.md)
```

### 4. Run AI Assistant in CLI
```bash
python ai/ai_assistant.py
```

### 5. Execute SQL Queries
You can run any of the 11 SQL scripts using SQLite:
```bash
python -c "import sqlite3; conn = sqlite3.connect('data/expense_sales.db'); print(conn.executescript(open('sql/11_advanced_analysis.sql').read()).fetchall())"
```

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
