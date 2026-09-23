# 13 — User Guide

*For non-technical finance user. Plain language.*

## Getting Started
Open `https://<vercel-deploy>/` → Dashboard shows `AI SaaS Startup` KPIs.

**Sidebar:** Click page names: Dashboard, Revenue, COGS, Expenses, P&L Statement, Forecast, Break-even, What-If Simulator, Yearly Report, Settings.

**Topbar:** Select month `January-Dec 2026` via `monthSelect`; toggle `GST 18%`, `₹ Lakh/Full`.

## 1. Manage Revenue
Go `Revenue` → enter `Revenue Source` (e.g., Subscription) + `Amount (₹)` (type `10000` or `1L` for 1,00,000) → `+ Add Revenue` → table shows total. Amount `<0` rejected.

## 2. Manage COGS
`COGS` → source `Cloud Hosting` + amount → `+ Add COGS` → see `Gross Profit`/`Gross Margin` cards.

## 3. Manage Expenses
`Expenses` → `Category` dropdown (Marketing, Salaries…) → amount → `+ Add Expense` → `Total OPEX`.

## 4. View P&L
`P&L Statement` → table for selected month: Revenue, COGS, Gross, OPEX, Operating, Net, margins, status Profit/Loss.

## 5. Dashboard
`Dashboard — Sept` → KPIs, `Revenue vs Expenses` chart, `Profit Trend`, `Expense Breakdown` donut, `Business Health`, `Yearly Summary 2026`. `Export Annual CSV / FY`.

## 6. Forecast
`12-Month Forecast` → adjust `Starting Customers`, `Monthly Growth %`, `Price`, `Expense Growth %` → table `Month Customers Revenue COGS OPEX Profit` + chart.

## 7. Break-Even
`Break-Even Analysis` → `Fixed Costs`, `Avg Revenue / Customer`, `Variable Cost` → see `Contribution Margin`, `Break-Even Customers/Revenue`.

## 8. Simulator
`What-If Simulator` → slide `Customers 0-5000`, `Price`, edit `Marketing, Salaries, Cloud, Other` → instant `simResult` profit/margin/break-even, not saved to DB.

## 9. Reports
`Yearly Report 2026` → `yearlyCards2`, `fyCards` (FY Apr-Mar), `auditLog` (read-only).

## 10. Settings
- `Business Name` input
- `Data Source`: `Local` (fast demo), `SQL` (SQLite Flask :5000), `MongoDB` (needs `MONGO_URI`). Buttons `Sync Local→SQL`, `Sync Local→Mongo`, `Reset Current Month`, `↻ Test Connection`.
- Bottom dark box shows example `fetch /api/pnl` snippet with `▶ Run this query live`.

## 11. Multi-Business
Sidebar `+ New Business` → creates 12 months 2026; `🗑 Remove Business` deletes all months/data (cannot delete last).

## 12. Import/Export
- `📤 Import CSV` (choose csv) → adds rows via `/api/import`.
- `⬇ Export CSV` / `📄 Export PDF` → download P&L (PDF uses Rs. for Helvetica fix).
- `GST Toggle` 18% on display.

## Common Mistakes
- Forgetting to select month → `month_id required` error.
- Using negative amount → `Negative not allowed`.
- In `SQL` mode, Flask not running on `:5000` → `SQL Load Demo failed` alert.
