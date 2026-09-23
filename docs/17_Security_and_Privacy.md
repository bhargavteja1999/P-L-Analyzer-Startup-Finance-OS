# 17 — Security and Privacy

## Implemented Controls
- **Parameterized queries:** All `conn.execute("SELECT ... WHERE business_id=?", (biz,))` in `app.py` — no SQL injection.
- **Input validation:** `amount<0 =>400`, `name required`, `business_id/mth_id` integer checks, `CHECK(amount>=0)` in SQLite.
- **Secrets via env:** `MONGO_URI` from `os.getenv` + `load_dotenv()` `app.py:19`, not hardcoded.
- **CORS:** `flask_cors.CORS(app)` enabled (but allow-all — see missing).
- **Mongo ObjectId handling:** 24-hex check before `ObjectId`.

## Missing / Recommended Controls (`Not Applicable` currently)
- **Authentication:** No JWT/session, `users` no passwords, frontend `userSelect` client-only.
- **Authorization:** No role check on `DELETE /api/businesses`, `POST /api/import`, etc.
- **CORS restriction:** Should be `CORS(app, origins=["https://<vercel-domain>"])` not allow-all.
- **Rate limiting:** No `Flask-Limiter`.
- **CSRF:** No token, but API is JSON, not cookie-based — low risk.
- **CSP/Helmet:** No headers.
- **Secrets in browser:** `MONGO_URI` not exposed to JS (good), but `API_BASE` hardcoded to `localhost:5000` leaks dev URL.
- **Sensitive data:** Financial amounts not encrypted at rest; SQLite file `pnl.db` committed with data (binary, contains 2 businesses).
- **File validation:** `Import CSV` accepts any JSON rows, no size limit.
- **Logging PII:** No PII, but `businesses` names logged via `print`.

## Privacy
- Data: Revenue/COGS/expenses per business, no user PII beyond `users` email seed.
- `localStorage pnl_v2` persists in browser, not cleared on logout (no logout).
- Mongo `mongomock` in-memory not persisted.

## Browser-Exposed Config
- `GOOGLE_API_KEY` **Not Applicable** — `ai_assistant.py` expects passed `api_key`, not env, but no frontend key exposure.
- `MONGO_URI` not leaked.

## Third-Party Security Dependencies
- `pymongo` + `dnspython` maintained, but `pytz==2026.3.post1` future version — **Assumption** safe.

## Known Gaps
- Exposed delete without auth is high risk if public.
