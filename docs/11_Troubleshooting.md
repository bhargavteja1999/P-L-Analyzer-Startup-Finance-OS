# 11 — Troubleshooting

### 1. `No python entrypoint found but found pnl_analyzer/backend/app.py`

**Problem:** Vercel build fails, suggests `pnl-analyzer.backend.app:app`.
**Cause:** Hyphen invalid, or `pyproject.toml` not at Vercel `Root`.
**Diagnose:** `cat pyproject.toml | grep entrypoint` — should be `pnl_analyzer.backend.app:app` at root.
**Solution:** `git mv pnl-analyzer pnl_analyzer` already done; ensure both `pyproject.toml` exist. Set Vercel Dashboard `Root Directory=.` (default) or `pnl_analyzer` if nested.
**Verify:** `py -c "import pnl_analyzer.backend.app; print(pnl_analyzer.backend.app.app)"`

### 2. `No solution found python_full_version == '3.9.*' dnspython>=3.10`

**Problem:** `uv lock` fails.
**Cause:** `requires-python = ">=3.9"` includes 3.9, but `dnspython==2.8.0` needs `>=3.10`.
**Diagnose:** `pip show dnspython | grep Requires-Python`
**Solution:** Changed to `requires-python = ">=3.10"` in both `pyproject.toml`.
**Verify:** `py --version` + `py -m pip check`

### 3. `500 FUNCTION_INVOCATION_FAILED bom1::...`

**Problem:** Page 500 on Vercel.
**Cause:** `models.py:9` `DB_PATH = .../pnl.db` write to read-only FS at import `init_db()`.
**Diagnose:** `VERCEL=1 py -c "import pnl_analyzer.backend.app"` → `sqlite3.OperationalError: attempt to write a readonly database`
**Solution:** `models.py:15` uses `/tmp/pnl.db` when `VERCEL=1`, copies seed, fallback `:memory:`, `app.py:43` try/except `init_db`.
**Verify:** `VERCEL=1 py -c "import pnl_analyzer.backend.app; print('ok')"`

### 4. `404 The requested URL was not found on the server.`

**Problem:** `GET /` returns Flask 404 HTML (not Vercel 404).
**Cause:** Flask had no `@app.route("/")`; Vercel rewrote `/` to Flask.
**Diagnose:** `curl http://localhost:5000/` → 404
**Solution:** Added `app.py:45` `_root` serving `pnl_analyzer/index.html` via `send_from_directory` + catch-all `/_frontend_fallback`.
**Verify:** `curl http://localhost:5000/` → 200 html

### 5. `month_id and business_id required` 400 on `/api/pnl`

**Problem:** Frontend shows error.
**Cause:** `curMonthId` null or stale `monthSelect`.
**Diagnose:** Check `GET /api/months/1` returns `[{id:1..12}]`, browser `localStorage pnl_v2` vs `sql` mode mismatch.
**Solution:** `Reset Demo Data` or `Sync Local → SQL` in Settings, or reload `monthSelect`.

### 6. `Mongo not reachable` 503 on `/api/mongo/*`

**Problem:** All mongo routes 503.
**Cause:** No `MONGO_URI` or Atlas not reachable, `mongomock` fallback not configured? Actually fallback exists but `is_mongo_available` checks ping.
**Diagnose:** `curl http://localhost:5000/api/mongo/health`
**Solution:** Set `MONGO_URI` in `.env` or use `SQL`/`Local` mode. `Local` works offline.

### 7. `Negative not allowed` 400 on revenue add

**Problem:** Form error `revenueError` red.
**Cause:** `amount<0` check `app.py:75`.
**Diagnose:** Frontend `toNumber` parsing lakh/cr (e.g., `1L` → 100000) may produce negative if `-1`.
**Solution:** Enter `>=0`, use `1L` / `1Cr` buttons.

### 8. Charts not rendering / `Chart is not defined`

**Problem:** Dashboard blank.
**Cause:** CDN `chart.js@4.4.0` not loaded (offline) or `js/app.js:1` `API_BASE=http://localhost:5000` not reachable.
**Diagnose:** Browser console → Network, check `http://localhost:5000/api/dashboard/1` 200.
**Solution:** Ensure Flask running on `:5000` before opening frontend.

