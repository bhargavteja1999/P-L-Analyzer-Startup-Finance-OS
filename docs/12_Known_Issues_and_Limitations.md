# 12 — Known Issues and Limitations

**Honest risks to surface before handover.**

## Known Bugs
- **Sept divergence:** SQLite `baseRev[8]=20000` vs Mongo `30000` (`mongo_models.py:116` vs `models.py:106`). Intentional but confusing for QA.
- **Frontend duplicate:** `pnl_analyzer/js/app.js` and `pnl_analyzer/frontend/js/app.js` plus `.bak/.tmp` identical — which is deployed unclear.
- **`pnl_analyzer/__pycache__` committed** in history (now removed).

## Incomplete Features
- **`audit_log` never written:** Table exists `models.py:62`, `GET /api/audit` reads, but `app.py` never `INSERT` audit rows.
- **`scenarios` no read UI:** `POST /api/scenario` inserts, but no `GET /api/scenarios` list nor frontend display.
- **`is_opex` column unused** in `expenses`.

## Technical Debt
- **No auth:** `users` table with 3 seeded users, but no passwords, JWT, middleware; frontend `userSelect` client-only.
- **CORS allow-all** `CORS(app)` — should restrict to Vercel domain.
- **No migration versioning:** `CREATE TABLE IF NOT EXISTS` only; schema changes require manual handling.
- **Hyphen rename debt:** Docs/README still reference `pnl-analyzer` hyphen in comments/`js/app.js:432` alert messages.
- **Indian formatting patch:** `formatWithRupeeLakh` + `attachIndianInputs` added for Lakh/Cr but complex focus/blur logic fragile.

## Fragile Areas
- **SQLite ephemeral on Vercel:** `/tmp` wiped, data lost per cold start; `models.py:14` copy is best-effort.
- **WAL journal:** `PRAGMA journal_mode=WAL` may fail on `/tmp` if fallback to `:memory:` loses data.
- **Top-level `try: from calculations import *` fallback to `from .calculations`** — works but hides import errors.

## Missing Infrastructure
- **No CI/CD:** No `.github/workflows`, no lint, no tests in pipeline.
- **No monitoring:** Only `print` logs, no Datadog/Sentry, no health check beyond `/api/health`.
- **No backup/recovery:** See `23_Data_Lifecycle...` — No verified backup.
- **No rate limiting, CSP, helmet.**

## Scalability Limitations
- SQLite single file, no connection pooling `check_same_thread=False` but no `g` context.
- All `GET /api/dashboard/<biz_id>` loops 12 `month_pnl` queries sequentially — N+1, no pagination.

## Security Limitations
- `MONGO_URI` via env, but no secret rotation.
- `amount` validation only `>=0`, no max beyond `1e12` frontend.
- No CSRF.

## Test Limitations
- 5 unit tests, 0 integration/E2E, no coverage report.

## Documentation Debt
- Root `README.md` title `AI-Expense-Sales-Analyzer` outdated vs P&L SaaS.
