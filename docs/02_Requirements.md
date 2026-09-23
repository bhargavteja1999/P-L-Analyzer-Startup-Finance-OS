# 02 — Requirements

## Functional Requirements (Implemented → evidence)

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| F1 | Multi-business with 12 months 2026 | Implemented | `POST /api/businesses` `app.py:152`, `models.py:86` |
| F2 | Revenue CRUD (source, amount) | Implemented | `revenue` table, `/api/revenue` GET/POST/DELETE |
| F3 | COGS CRUD | Implemented | `cogs` table, `/api/cogs` |
| F4 | Expenses CRUD | Implemented | `expenses` table, `/api/expenses` |
| F5 | P&L per month (gross/net/margins/status) | Implemented | `calculate_pnl` `calculations.py:69`, `/api/pnl` |
| F6 | Dashboard 12-month trend + yearly | Implemented | `/api/dashboard/<biz_id>`, `yearly_summary` |
| F7 | Forecast 12-month | Implemented | `calculate_forecast`, `/api/forecast` |
| F8 | Break-even | Implemented | `calculate_break_even`, `/api/break-even` |
| F9 | GST 18% | Implemented | `calculate_gst`, `/api/gst` |
| F10 | FY Apr-Mar + anomaly + mov avg | Implemented | `calculate_fy_summary`, `detect_anomalies`, `/api/fy` |
| F11 | CSV import bulk rows | Implemented | `/api/import` |
| F12 | Reset demo reseed | Implemented | `/api/reset-demo` SQLite, `/api/mongo/reset-demo` |
| F13 | CSV export / PDF export | Implemented | Frontend `exportCsv`/`exportPdf` jsPDF, `renderPnlTable` Rs. fix |
| F14 | Simulator sliders (what-if) | Implemented | `simulator` page, no DB write |
| F15 | MongoDB optional third source | Partially Implemented | `mongo_models.py` mongomock fallback, `baseRev[8]=30000` divergence |
| F16 | Audit log read | Partially | `audit_log` table exists, `GET /api/audit` reads, but never written |
| F17 | Users/roles | Not Applicable | `users` table exists, `GET /api/users` reads, no auth |
| F18 | AI assistant Gemini + offline | Implemented | `ai/ai_assistant.py` Gemini 2.5-flash, keyword fallback |
| F19 | Power BI dashboard | Implemented (legacy) | `powerbi/*.pbix` + screenshots |

## Non-Functional Requirements

| NFR | Status | Evidence |
|-----|--------|----------|
| CORS allow-all | Implemented | `CORS(app)` |
| Vercel deploy Python 3.12 | Implemented | `vercel.json` rewrites, `pyproject.toml` `>=3.10` |
| SQLite WAL | Implemented | `SCHEMA PRAGMA journal_mode=WAL` |
| Input validation | Partially | `amount>=0` CHECK + frontend `toNumber` + 400 errors |
| No auth | Limitation | No JWT/session middleware |
| No rate limiting | Not Applicable | Not found |
| No logs/monitoring | Not Applicable | Only `print` |
| Performance <500ms | Not Confirmed | No benchmarks |

## User Roles

| Role | Intended | Implemented |
|------|----------|-------------|
| owner | full | No enforcement, client-side dropdown `userSelect` |
| accountant | edit | Same |
| viewer | read-only | Same |

## Validations & Constraints
- `amount REAL CHECK(amount>=0)` in SQLite; backend `if d["amount"]<0: 400`; frontend `toNumber` + `1e12` max.
- `businesses` `name required`; `months` `UNIQUE(business_id,month_index,year)`.
- `business_id/mth_id` must be integer else 400 with hint `GET /api/months/1`.
- Mongo `ObjectId` length 24 fallback.

## Missing vs. Intended
- Auth missing vs `users` table intended? **Intended vs Current:** Intended possibly auth, current is seed only.
- `audit_log` intended to track changes, current never written.
