# 01 — Product and Business Overview

*Readable by non-technical stakeholders. No implementation detail beyond what clarifies value.*

## What the Product Does
A browser SaaS where a startup tracks **Revenue** (multiple sources), **COGS** (direct costs), **Operating Expenses** (salaries, marketing, software, etc.) per month, then instantly sees **Gross Profit, Margins, Operating/Net Profit**, plus yearly summaries, GST (18% default), FY Apr-Mar, and forward-looking **12-month forecast** and **break-even** analysis. A **What-If Simulator** lets founders slide customers/price and see profit without changing real data. Data can be **imported via CSV** and **exported as CSV/PDF**.

A secondary **AI Assistant** answers finance questions (“What drove profit?”) using Gemini or offline keyword answers.

## Why It Exists
Spreadsheets are error-prone for P&L and do not provide interactive forecasts, break-even, or anomaly detection.

## Who Uses It
- **Founder/Owner** — creates businesses, views dashboard, runs simulator.
- **Finance Manager/Accountant** — enters revenue/COGS/expenses, runs reports.
- **Viewer** — read-only (currently enforced only visually; no backend check — see `Not Applicable`).

> `Not Confirmed`: Whether viewer restriction is intended to be backend-enforced — implementation has no auth (`users` table exists but no passwords).

## Major User Journeys
1. **Monthly close:** Select business + month → add revenue sources → add COGS → add expenses → view `P&L Statement` table → check Dashboard KPIs.
2. **Planning:** Use `Forecast` (starting customers, growth %, price) → see 12-month profit table/chart.
3. **Break-even check:** Enter fixed costs, revenue/variable per customer → see contribution margin + customers/revenue to break even.
4. **Clean-up:** `Load Demo Data` → 12 months 2026 seeded; `Reset Demo` clears and reseeds; `Import CSV` bulk adds rows.
5. **Multi-business:** `+ New Business` auto-creates 12 months 2026; `Remove Business` cascades deletes.

## Business Rules (Implemented)
- Amount must be `>=0`; negative returns `400 Negative not allowed` (`app.py:75`).
- Cannot delete last business (`400 Cannot delete last business`).
- Business creation always 2026 Jan-Dec months.
- Gross margin = `(revenue-cogs)/revenue*100` (0 if revenue 0) — `calculations.py:16`.
- Net margin similarly.
- FY summary reorders Jan-Dec to Apr-Mar (`fy_start_month=4`).
- Anomaly = z-score `abs(z)>2`.

## Expected Value
`Not Confirmed` quantitative outcomes (e.g., “saves X hours”) — repo has no metrics/SLAs. Value is qualitative: faster close, scenario planning.

## Current Limitations (user-visible)
- No login; anyone with URL can edit data.
- Data lost on Vercel unless MongoDB configured; local SQLite file persists but not backed up.
- No real backup/recovery.
- 3 demo users only, no permissions.

## Roadmap vs. Intent
See `16_Future_Roadmap.md`. No hidden business outcomes claimed.
