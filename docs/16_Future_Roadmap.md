# 16 — Future Roadmap

## Confirmed / Existing TODOs (from code comments / missing)

| TODO | Evidence | Priority |
|------|----------|----------|
| `audit_log` never written | `models.py:62` exists, `app.py:289` only reads | High |
| `scenarios` no GET/list UI | `app.py:152` inserts, no read endpoint | Medium |
| `users` no auth | `users` table seed, no password column, `app.py:213` only list | High |
| `is_opex` unused | `models.py:45` | Low |
| `CORS allow-all` restrict | `app.py:42` `CORS(app)` | High |
| `pnl.db` SQLite ephemeral → Mongo persistent | `models.py:15` `/tmp` comment | High |
| `requirements.txt` vs `pyproject.toml` duplicate | Both have flask stack | Low |
| `js/app.js:432` alert still references `pnl-analyzer` hyphen | `js/app.js:432` | Low |
| `frontend/` duplicate vs `js/` | Two `index.html` copies | Low |

## Proposed Improvements (not company-approved, author suggestions)

- **Auth:** Add `Flask-JWT`, `users.password_hash`, role middleware for `DELETE /businesses`, `POST /import`.
- **Migration:** Add `alembic` or `yoyo` for `SCHEMA` versioning.
- **Tests:** Add `pytest` + `app.test_client()` integration for 35 routes, `js` unit for `toNumber`.
- **CI:** `.github/workflows/ci.yml` → `py -m py_compile`, `python tests`, `vercel --prebuilt`.
- **Monitoring:** `sentry-sdk[flask]` for `500` tracking, Vercel Analytics.
- **Backup:** Cron `sqlite3 pnl_analyzer/backend/pnl.db .dump | gzip > /tmp/backup.sql.gz` → S3, or migrate to `libsql`/`Supabase`.
- **Performance:** Pagination for `dashboard` 12-month loop, add `INDEX(business_id, month_id)` for `revenue/cogs/expenses`.
- **Frontend:** Bundle with `vite` instead of CDN, fix `API_BASE` to relative `/api` for prod CORS.

**No company-approved roadmap found** (`Not Confirmed`).

