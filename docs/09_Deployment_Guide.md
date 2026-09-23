# 09 — Deployment Guide

## Build Process
No build step for SaaS (vanilla JS + Flask). Vercel runs `uv lock --python 3.12` + `pip install` from `pyproject.toml:6` (7 deps). Frontend is static `pnl_analyzer/index.html` via `outputDirectory`.

## Vercel (Production)
- **Platform:** Vercel serverless Python 3.12 (from `pyproject.toml:5` `requires-python >=3.10`).
- **Entrypoint:** `pyproject.toml:16` `pnl_analyzer.backend.app:app` when Vercel `Root Directory=.` (default). Alternative `pnl_analyzer/pyproject.toml:16` `backend.app:app` when `Root Directory=pnl_analyzer` — both kept for compatibility.
- **Config:** `vercel.json:3` `{"rewrites":[{"source":"/api/(.*)","destination":"pnl_analyzer/backend/app.py"}],"outputDirectory":"pnl_analyzer"}` + nested `pnl_analyzer/vercel.json` `{"rewrites":[{"source":"/api/(.*)","destination":"backend/app.py"}]}`. No `builds` duplicate.
- **Steps:**
 1. `git push origin main`
 2. Vercel auto-build → `Using Python 3.12` → `Installing from pyproject.toml` → `pytz 2026.3.post1` etc.
 3. Verify `https://<deploy>/api/health` → `{"status":"ok"}`
 4. Verify `https://<deploy>/` → Dashboard (static) and `https://<deploy>/api/pnl?business_id=1&month_id=9`
 5. Health check: Flask `/_root` serves `index.html` fallback if rewrite misses.

- **Env vars on Vercel:** Dashboard → Settings → Environment Variables → `MONGO_URI` (if Atlas), else mongomock fallback works.
- **DB:** `models.py:15` uses `/tmp/pnl.db` on `VERCEL=1`, copied from committed `pnl_analyzer/backend/pnl.db` on cold start, else `:memory:` fallback. **Ephemeral** — writes lost on redeploy.
- **Rollback:** Vercel Dashboard → Deployments → previous → Promote to Production. No DB rollback (ephemeral).

## Local (as prod parity)
```bash
python pnl_analyzer/backend/app.py # :5000
python -m http.server 8000 --directory pnl_analyzer
```

## Common Deployment Failures
| Symptom | Cause | Fix |
|---------|-------|-----|
| `No python entrypoint found` | `Root` mismatch | Keep both `pyproject.toml`; set `Root=.` (default) |
| `No solution found python_full_version == '3.9.*'` | `requires-python >=3.9` vs `dnspython>=3.10` | Fixed to `>=3.10` |
| `500 FUNCTION_INVOCATION_FAILED` | SQLite write to read-only `pnl.db` | Fixed via `/tmp` + try/except `init_db` |
| `404 Not Found /` | No Flask `/` route | Fixed `app.py:45` `_root` + `/_frontend_fallback` serves `index.html` |

## Secrets
Set via Vercel env, not committed. No `SECRET_KEY`.

## Verification
`curl https://<deploy>/api/health` and browser `/` → Dashboard KPIs.

## No Docker/CI
No `Dockerfile`, no `.github/workflows` (**Not Applicable**).
