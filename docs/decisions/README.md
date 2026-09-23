# Decisions — Architecture Decision Records (lightweight)

## ADR 001 — Flask for SaaS API
- **Context:** Need CRUD + P&L calc, Vercel Python support.
- **Decision:** `Flask 3.0.0` with `CORS(app)` in `pnl_analyzer/backend/app.py:41`.
- **Consequences:** Simple, Vercel compatible, but `CORS allow-all`, no async. Alternative FastAPI not chosen (**Reason not confirmed**).
- **Evidence:** `pyproject.toml:8`, `app.py:41`.

## ADR 002 — Underscore Rename `pnl-analyzer` → `pnl_analyzer`
- **Context:** `pnl-analyzer` hyphen invalid for `import pnl-analyzer.backend.app` → Vercel `No python entrypoint found`.
- **Decision:** `git mv pnl-analyzer pnl_analyzer`, `entrypoint = "pnl_analyzer.backend.app:app"` (`pyproject.toml:16`).
- **Consequences:** Fixes import, requires updating docs/scripts referencing hyphen.
- **Evidence:** `git log d541ddf`, `pyproject.toml:16`, `pnl_analyzer/__init__.py`.

## ADR 003 — `/tmp/pnl.db` on Vercel
- **Context:** `FUNCTION_INVOCATION_FAILED` due to `DB_PATH = .../pnl.db` read-only FS on `VERCEL=1`.
- **Decision:** `models.py:13` use `Path("/tmp")/pnl.db` if `VERCEL`, copy seed via `shutil.copy2`, fallback `:memory:`.
- **Consequences:** Data ephemeral per cold start, but no 500; Mongo needed for persistence.
- **Evidence:** `models.py:11`, `app.py:43` try/except `init_db`.

## ADR 004 — Dual `pyproject.toml` for Root Handling
- **Context:** Vercel `Root Directory` can be `.` or `pnl_analyzer`.
- **Decision:** Keep `pyproject.toml` at root (`pnl_analyzer.backend.app:app`) and `pnl_analyzer/pyproject.toml` (`backend.app:app`) + both `vercel.json` rewrites.
- **Consequences:** Deployment works regardless of Root setting, but duplicate config needs sync.
- **Evidence:** `vercel.json:3`, `pnl_analyzer/vercel.json:3`.

## ADR 005 — Mongo + mongomock Fallback
- **Context:** Need optional persistence without mandating Atlas.
- **Decision:** `mongo_models.py:44` `mongomock.MongoClient()` fallback, `serverSelectionTimeoutMS=2000`.
- **Consequences:** Works offline, but Sept `baseRev 30000` vs SQLite `20000` divergence.
- **Evidence:** `mongo_models.py:1`, `requirements.txt:6`.

## ADR 006 — Vanilla JS SPA (no React/Vue)
- **Context:** Finance OS needs 10 pages, charts, but simple.
- **Decision:** `pnl_analyzer/index.html` + `js/app.js` vanilla, `localStorage`, CDNs `chart.js`, `jspdf`.
- **Consequences:** No build step, but duplicate `frontend/` vs `js/`.
- **Evidence:** `index.html:11`, `js/app.js:1`.

## ADR 007 — `requires-python >=3.10`
- **Context:** `dnspython==2.8.0` requires `>=3.10`, Vercel Python 3.12, `uv lock` failed on `>=3.9`.
- **Decision:** Bump `pyproject.toml:5` `requires-python = ">=3.10"` in both files.
- **Consequences:** Drops 3.9 support, fixes resolver.
- **Evidence:** `pip show dnspython`, `pyproject.toml:5`.

