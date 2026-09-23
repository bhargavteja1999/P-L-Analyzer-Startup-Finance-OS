# 19 — Error Handling and Resilience

## Strategy
- **Validation-first:** Backend `amount<0 =>400`, `name required =>400`, `business_id/mth_id` integer `400` with hint, `CHECK>=0` in DB.
- **No retries:** No retry for SQLite or Mongo; `is_mongo_available()` single ping `serverSelectionTimeoutMS=2000`, then `mongomock` fallback.
- **Fallbacks:** Mongo → `mongomock` in-memory (`mongo_models.py:44`); SQLite `/tmp` → `:memory:` (`models.py:92`); Gemini → offline keyword router (`ai_assistant.py:78`).
- **Timeouts:** Only Mongo 2s timeout; Flask default.

## Validation (user-facing)
- Frontend `js/app.js:42` `toNumber` + `attachIndianInputs` cleans `1L/1Cr`, `revenueError` red text, `400 Negative not allowed` JSON.
- SQLite `CHECK` prevents negative even if API bypassed.

## Failure States
- `GET /api/pnl?business_id=1&month_id=undefined` → `400 month_id and business_id required. Example...`
- `DELETE /api/businesses/<id>` last business → `400 Cannot delete last business`.
- `GET /api/mongo/*` when down → `503 Mongo not reachable. Set MONGO_URI` with hint.
- `Vercel` read-only → `init_db` try/except logs `SQLite init skipped` but continues via `/tmp`.

## User-Facing Errors
Frontend shows `alert("SQL Load Demo failed... ensure Flask running on :5000")` and `500 Internal Server Error` HTML for DB `no such table` (now fixed via `/tmp`).

## Logging
Only `print` statements: `Mongo init done`, `Mongo init skipped`, `SQLite init skipped`. No `logging` module, no Sentry.

## Recovery
- `POST /api/reset-demo` reseeds 12 months.
- `POST /api/mongo/reset-demo` reseeds Mongo.
- No transaction rollback beyond `conn.commit()`/`close()`.

## Weakness (honest)
- No retries, no circuit breaker, no timeout for Flask routes (slow `dashboard` loops 12 queries).
- `500` HTML for DB errors (should be JSON).
- No input max length beyond `1e12` frontend.
