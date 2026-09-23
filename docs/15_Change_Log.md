# 15 — Change Log

*Curated from `git log --oneline` + code diff.*

## Unreleased (docs handover 2026-09-23)
- **docs/**: Production handover system created (25 docs + ai/ + decisions/).

## 2026-09-23 — Vercel fixes
- **c5f8e43** `Updated the app.py file and models.py files` — Fix `500 FUNCTION_INVOCATION_FAILED` via `/tmp/pnl.db` (`models.py:15` `VERCEL` → `/tmp`, `shutil.copy2` seed, fallback `:memory:`, `app.py:43` try/except `init_db`).
- **9e5b448** `updated the pyproject.toml file` — Bump `requires-python = ">=3.9"` → `">=3.10"` in both `pyproject.toml` for `dnspython==2.8.0` `>=3.10` (`uv lock` fix for Python 3.12).
- **d541ddf** `Inspect the repository and implement the fix.` — Rename `pnl-analyzer` → `pnl_analyzer` (hyphen invalid for `pnl_analyzer.backend.app:app`), add `pnl_analyzer/__init__.py`, keep dual `pyproject.toml`/`vercel.json` for `Root=.` vs `Root=pnl_analyzer`.

## 2026-09-23 — Earlier Vercel attempts
- **aacea92** `vercel files are updated` — Added `CORS(app)` + `send_from_directory` fallback, `_root`/`_frontend_fallback`, `DB_PATH` `/tmp` initial.
- **54d7369** `For vercel deployment` — Renamed `pyproject.toml` → `pnl_analyzer/pyproject.toml`, `vercel.json` rewrites update (broke default Root).
- **7413691** `Add the pyproject.toml file` — First `pyproject.toml` with `pnl-analyzer.backend.app:app` (hyphen, broken).
- **c6e93b0** `Add the vercel.json file` — First `vercel.json` with `builds`/`routes` legacy.

## 2026-09-18 and earlier
- **f334fce** `Sending File to the github p&L Analyzer` — Initial P&L SaaS + legacy pipeline.
- **fdbf1a0** `Initial commit` — Repo init.

## No semantic versioning
`pyproject.toml:3` stays `1.0.0` since `f334fce`. No `git tag`.

**How to update:** Add entry here per `git log`, bump `pyproject.toml:3` if needed, `git tag vX.Y.Z`.
