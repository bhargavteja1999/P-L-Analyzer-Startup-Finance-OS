# 00 — Project Overview

## What This Is
**P&L Analyzer — Startup Finance OS** is a vanilla-JS + Flask SaaS for startup P&L management, plus a legacy **AI-Expense-Sales-Analyzer** data pipeline (Python/pandas, 11 SQL scripts, Streamlit/Power BI sketches) in the same repo.

**Implemented entry:** `pnl_analyzer/index.html:1` → `pnl_analyzer/backend/app.py:41` `app = Flask(__name__)`. **Legacy pipeline:** `python/` + `sql/` → `data/expense_sales.db`.

## Why It Exists
Founders need to track revenue, COGS, OPEX, margins, run forecasts, break-even, GST, FY summaries without spreadsheet errors. The repo bundles the SaaS with an earlier expense/sales analytics prototype.

## Target Users (Implemented)
- Finance user (browser) — manages business/months, revenue/COGS/expenses, views P&L, dashboard, forecast, break-even, simulator, reports.
- Roles `owner`/`accountant`/`viewer` exist in `users` table but **Not Applicable** — no auth, frontend `userSelect` is client-side display only.

## Major Capabilities (Implemented)
- Multi-business (12 months Jan-Dec 2026 auto-created) — `POST /api/businesses`, `DELETE /api/businesses/<id>` with cascade.
- Revenue/COGS/Expenses CRUD with `CHECK(amount>=0)` and `amount<0 =>400`.
- P&L per month + dashboard 12-month trend + yearly summary — `calculations.py:69` `calculate_pnl` (gross, net, margins, status).
- Forecast 12-month `calculate_forecast`, break-even `calculate_break_even`, GST `calculate_gst`, FY Apr-Mar `calculate_fy_summary`, anomaly `detect_anomalies` (z>2), moving avg.
- Data sources: `Local` (localStorage `pnl_v2`), `SQL` (SQLite `pnl_analyzer/backend/pnl.db` or `/tmp/pnl.db` on Vercel), `MongoDB` (Atlas or mongomock fallback).
- Import CSV, export CSV/PDF (jsPDF), simulator sliders, audit log (read-only).
- AI assistant `ai/ai_assistant.py` Gemini 2.5-flash with offline keyword router fallback.

## Technology Summary
| Layer | Tech | Evidence |
|-------|------|----------|
| Backend | Python 3.10+ (Vercel 3.12), Flask 3.0.0, Flask-Cors 4.0.0, pymongo 4.18.1, mongomock 4.3.0, pytz 2026.3.post1 | `pyproject.toml:6`, `pnl_analyzer/backend/requirements.txt:1` |
| Frontend | Vanilla JS, Chart.js 4.4.0, jsPDF 2.5.1, Inter font | `pnl_analyzer/index.html:11` |
| DB | SQLite `pnl.db` 8 tables + Mongo `pnl_analyzer` 5 cols, WAL | `models.py:11`, `mongo_models.py:1` |
| AI | google-genai `gemini-2.5-flash`, prompts in `ai/prompts.py` | `requirements.txt:10`, `ai/ai_assistant.py:42` |
| Deploy | Vercel `pyproject.toml:16` `pnl_analyzer.backend.app:app`, `vercel.json:3` rewrites | `vercel.json:3` |

## Current Implementation Status
- **Implemented:** All 35 Flask routes, 16 calc functions, 8 SQLite tables, 3 Mongo collections fallback, 10 frontend pages, CSV/PDF, simulator, AI offline router.
- **Partially Implemented:** `audit_log` table exists but never written to (`app.py` no INSERT); `scenarios` inserted but no UI list; Mongo `months` id handling has ObjectId fallback complexity.
- **Limitation:** No auth, CORS allow-all, SQLite ephemeral on Vercel, no migrations versioning, no CI/CD, 5 unit tests only 4 passing (needs run).
- **Frontend duplicate:** `pnl_analyzer/js/app.js` and `pnl_analyzer/frontend/js/app.js` identical plus `.bak/.tmp`.

## Important Limitations (before you start)
- Do not expose publicly without auth; `CORS(app)` allow-all.
- Do not rely on Vercel SQLite persistence; use `MONGO_URI`.
- `pnl_analyzer` underscore is required — hyphen breaks import.

## Repository Structure (verified)
```
P-L-Analyzer-Startup-Finance-OS/
├── pnl_analyzer/          # SaaS (deploy root)
│   ├── backend/           # Flask
│   ├── index.html, css/, js/, frontend/
│   ├── pyproject.toml, vercel.json, __init__.py
├── python/                # data pipeline
├── sql/                   # 11 scripts
├── ai/                    # assistant
├── data/                  # db + csv/xlsx
├── powerbi/ notebooks/ reports/
├── pyproject.toml, vercel.json (root, for Vercel default Root=.)
└── docs/                  # this system
```

## Quick-Start Path
1. `07_Local_Setup_Guide.md` (5 min local)
2. `05_API_Documentation.md` (curl health)
3. `03_System_Architecture.md` (diagram)
