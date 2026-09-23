# 23 — Data Lifecycle, Backup and Recovery

## Creation
- **SaaS:** User `POST /api/revenue` → `INSERT` with `source,amount` → `SELECT` via `GET /api/pnl` → `calculate_pnl`.
- **Legacy pipeline:** `python/data_loader.py` `generate_synthetic_data(1000,42)` → `data/processed/cleaned_sales_data.csv` (489k) → `python/export_data.py` → `data/expense_sales.db` + `sql/03_insert_data.sql` → `data/raw/sales_expense_data.csv` (210k) → `sql` star schema.

## Transformation
- `data_cleaning.py` dedup + feature engineering (expense ratio, margins).
- `eda.py` `generate_eda_summary` → `data/processed/summary_metrics.json` (14494612 revenue etc.).
- `calculations.py` pure functions no persistence.

## Storage
- **SaaS SQLite:** `pnl_analyzer/backend/pnl.db` (committed binary) or `/tmp/pnl.db` on `VERCEL=1` (ephemeral, per-instance). No encryption.
- **SaaS Mongo:** `pnl_analyzer` DB 5 cols via `MONGO_URI`.
- **Browser:** `localStorage pnl_v2` (no expiry).
- **Legacy:** `data/expense_sales.db` (1200 transactions) + `data/processed/*.csv`.

## Retention
**Not Applicable:** No retention policy; data kept until `DELETE` via `DELETE /api/revenue/<id>` or `DELETE /api/businesses/<id>` cascade or `POST /api/reset-demo` truncate.

## Deletion
- Row delete: `DELETE FROM revenue WHERE id=?`
- Business delete: cascades `revenue/cogs/expenses/months/scenarios/audit_log` + Mongo `delete_many`.

## Backups
**No verified backup/recovery mechanism found.**

- SQLite file committed in git is only “backup” — not automated, not offsite, not tested restore.
- `VERCEL` `/tmp` is wiped per cold start, no snapshot.
- Mongo Atlas has own backup if configured, otherwise mongomock in-memory lost.
- `data/` CSVs committed, but no `pg_dump` equivalent for `pnl.db`.

## Restore / Recovery
**Not Applicable:** No `restore` script. Manual: `git checkout HEAD -- pnl_analyzer/backend/pnl.db` or re-run `python pnl_analyzer/backend/models.py`.

## Rollback
App code via Vercel promote previous deploy; data rollback via `POST /api/reset-demo` reseeds demo (destructive).

## Recommendations (Roadmap, not implemented)
- Cron `sqlite3 pnl.db .dump > backup.sql` to S3, or use Mongo persistent.
