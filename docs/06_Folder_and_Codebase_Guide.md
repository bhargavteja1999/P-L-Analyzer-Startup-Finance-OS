# 06 — Folder and Codebase Guide

## Root
- `pyproject.toml:1` — Root Vercel entry `pnl_analyzer.backend.app:app`, `requires-python >=3.10`, 7 deps. **Safe to modify** for deps.
- `vercel.json:1` — Root rewrites API → `pnl_analyzer/backend/app.py`, `outputDirectory pnl_analyzer`. **Safe** for routing.
- `requirements.txt:1` — Legacy data pipeline deps (pandas, numpy...). **Not used by Vercel**.
- `README.md:1` — Outdated AI-Expense title; see `docs/`.
- `LICENSE:1` — MIT 2026.

## `pnl_analyzer/` — SaaS (deploy artifact)
- `__init__.py:1` — marker for `pnl_analyzer` package.
- `pyproject.toml:1` — Nested entry `backend.app:app` when Vercel `Root Directory=pnl_analyzer`.
- `vercel.json:1` — Nested rewrites `backend/app.py`.
- `index.html:1` — Entry SPA 10 pages, loads `css/style.css`, `js/app.js`, CDNs.
- `css/style.css:1` — Variables, grid, cards.
- `js/app.js:1` — 800+ lines vanilla JS, `API_BASE`, `STORAGE_KEY`, `renderAll`, charts. **High-risk** — business logic mirror.
- `frontend/` — Duplicate of `index.html`+`css`+`js` (identical, plus `.bak/.tmp`). **Not Confirmed** which is canonical — `index.html` at `pnl_analyzer/` is `outputDirectory`.

## `pnl_analyzer/backend/` — Flask
- `__init__.py:1` — marker for `backend`.
- `app.py:41` — 518 lines, 35 routes, CORS, `/tmp` fallback. **High-risk** — all API.
- `calculations.py:1` — 16 pure funcs, no side effects. **Safe** to unit test.
- `models.py:11` — SQLite schema + `DB_PATH` `/tmp` logic. **High-risk** if schema change (no migrations).
- `mongo_models.py:1` — pymongo + mongomock fallback, `MONGO_URI`. **Safe** optional.
- `requirements.txt:1` — Flask stack.
- `.env.example:1` — `MONGO_URI`, `MONGO_DB`.
- `pnl.db:1` — SQLite file (binary, committed, 2 businesses currently).
- `tests/test_calculations.py:1` — 5 tests.
- `__pycache__/` — ignored.

## `python/` — Data pipeline
- `data_loader.py:1` — `generate_synthetic_data`, paths.
- `data_cleaning.py`, `eda.py`, `sales_analysis.py`, `expense_analysis.py`, `profit_analysis.py`, `export_data.py` — each <200 lines, class per domain. **Safe** isolated from SaaS.

## `sql/` — 11 scripts
- `01_create_database.sql` WAL, `02_create_tables.sql` star schema, `03_insert_data.sql` `INSERT OR IGNORE`, `04-11` analytics `LAG`, `DENSE_RANK`. **Not Confirmed** executed order.

## `ai/`
- `ai_assistant.py:1` `FinancialAIAssistant`, `prompts.py:1` templates, `insight_generator.py:1` markdown report. **Safe** but `google-genai` key required.

## `data/` — `expense_sales.db` (separate from `pnl.db`), `raw/*.csv/xlsx`, `processed/*`, **No .gitignore** — binary committed.

## `powerbi/` `notebooks/` `reports/` `sql/`
- Legacy artifacts, not needed for SaaS run.

## Safe vs Dangerous
- **Safe:** `calculations.py`, `python/*.py`, `ai/prompts.py`, `docs/`.
- **Dangerous:** `app.py` routing, `models.py` schema, `js/app.js` `API_BASE`/`DATA_MODE`, `pyproject.toml` `requires-python`, `vercel.json` rewrites.
