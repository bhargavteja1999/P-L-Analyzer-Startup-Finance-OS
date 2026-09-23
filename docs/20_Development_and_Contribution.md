# 20 — Development and Contribution Guide

## Workflow (discoverable)
- `main` branch only (see `git log --oneline` no `develop`). No `CONTRIBUTING.md`, no `CODEOWNERS`.
- Commit: `git add` `__pycache__` should be ignored (now fixed to `/tmp`), `git commit -m "fix(vercel): ..."` then `git push origin main` auto-deploys Vercel.
- No PR template, no branch naming convention **Not Confirmed**.

## Local Process
- `07_Local_Setup` → `python pnl_analyzer/backend/app.py` + `http.server`.
- Change `calculations.py` → `python pnl_analyzer/backend/tests/test_calculations.py`.
- Change `js/app.js` → hard refresh browser, check `localStorage`.

## Coding Conventions (observed, not enforced)
- Python: snake_case `calculate_pnl`, Flask `app = Flask(__name__)`, `CORS(app)`.
- JS: `const MONTHS`, `camelCase` `renderDashboard`, `API_BASE`.
- No `black`/`flake8`/`eslint` (**Not Applicable**).

## Naming
- Business `name` required, months `January-December` 2026 fixed.
- Collections `revenue/cogs/expenses` match SQLite tables.

## Test Expectations
- No CI gate; run `python pnl_analyzer/backend/tests/test_calculations.py` before push manually.

## Build Validation
- `py -m py_compile pnl_analyzer/backend/*.py`
- `py -m pip check`

## Safe Areas to Modify
- `calculations.py` (pure), `ai/prompts.py`, `python/*.py`, `sql/*.sql`, `pnl_analyzer/js/app.js` `TOOLTIP_DEFS`.

## Dangerous / High-Risk Changes
- `models.py` `SCHEMA` + `DB_PATH` `/tmp` logic — no migrations, risk data loss.
- `app.py` `CORS` + `init_db` import-time side effects — break Vercel cold start.
- `pnl_analyzer/backend/app.py` `_frontend_fallback` + `vercel.json` rewrites — 404 vs 500.
- `pyproject.toml` `requires-python`/`entrypoint` — breaks Vercel build if hyphen.
- `js/app.js` `API_BASE` hardcoded `localhost:5000` — breaks prod if changed to relative `/api` without CORS fix.

## Review
No formal review found; recommend at least one reviewer for `models.py`/`app.py`.

## AI Changes
- Do not commit `GOOGLE_API_KEY`; keep `ai_assistant.py` offline fallback.

