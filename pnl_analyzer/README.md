# P&L Financial Analyzer — SaaS Dashboard for Startups

Professional Profit & Loss analyzer with KPI cards, P&L statement, charts, forecast, break-even, and what-if simulator.

## Project Structure
```
pnl-analyzer/
├── index.html              # Entry (copy of frontend/index.html)
├── backend/
│   ├── app.py              # Flask API (routes separate from logic)
│   ├── calculations.py     # Pure financial engine
│   ├── models.py           # SQLite schema (businesses, months, revenue, cogs, expenses, scenarios) + seed demo data
│   ├── requirements.txt
│   └── tests/test_calculations.py
└── frontend/
    ├── index.html          # Single-page SaaS app (10 pages via nav)
    ├── css/style.css       # Responsive SaaS theme
    └── js/app.js           # State (localStorage), rendering, charts, export
```

## P&L Calculation (backend/calculations.py and frontend/js/app.js)
- Total Revenue = Σ revenue items
- Total COGS = Σ cogs items
- Gross Profit = Revenue − COGS
- Gross Margin = Gross/Rev ×100
- Total OPEX = Σ expenses
- Operating Profit = Gross − OPEX
- Net Profit = Operating − OtherExpenses + OtherIncome → Profit if >0 else Loss
- Net Margin = Net/Rev ×100
- Break-even: contribution = revPer − varCost; BE customers = fixed/contribution; BE revenue = BE×revPer
- Yearly summary aggregates 12 monthly P&Ls; Forecast projects revenue = customers×price, COGS = rev×cogs%, OPEX growing % per month

## How to Start

### Frontend only (no backend needed — uses localStorage)
```bash
# open directly:
start pnl-analyzer/frontend/index.html
# or via python http:
python -m http.server 8000 --directory pnl-analyzer/frontend
# then http://localhost:8000
```

### Backend (Flask + SQLite)
```bash
pip install -r pnl-analyzer/backend/requirements.txt
python pnl-analyzer/backend/models.py  # init DB + seed AI SaaS Startup demo data
python pnl-analyzer/backend/app.py     # runs on http://localhost:5000
# API examples:
# GET  /api/pnl?business_id=1&month_id=9
# GET  /api/dashboard/1
# GET  /api/forecast?start_customers=1000&growth=10&price=10&cogs_pct=15&opex_base=5000&opex_growth=4
# GET  /api/break-even?fixed=5000&revenue_per=10&variable=2
```

## How to Add Financial Data
1. Select month in top bar (Jan–Dec 2026)
2. Go to Revenue / COGS / Expenses pages → enter source + amount → Add
3. All KPIs, P&L table, charts, health, forecast update automatically
4. Validation: negative amounts and empty sources rejected
5. Click “Load Demo Data” to restore AI SaaS Startup: Revenue $10k, COGS $1.5k, OPEX $5k, Gross $8.5k, Net $3.5k, 35% margin

## Database
SQLite `backend/pnl.db` — multi-business ready. Tables: businesses, months(12 per business per year), revenue, cogs, expenses, scenarios. Frontend mirrors this in localStorage (`pnl_v2`) for offline demo.

## Testing
```bash
python pnl-analyzer/backend/tests/test_calculations.py
# checks gross, net, break-even, P&L, forecast
```

## Export & Responsive
- P&L CSV/PDF (jsPDF) per month, Annual CSV; charts resize; sidebar collapses on mobile; tables scroll horizontally.
