# 25 — Documentation Maintenance

## How to Keep Accurate
- **Source of truth:** `pnl_analyzer/backend/app.py` routes, `models.py` schema, `pyproject.toml` deps, `vercel.json` rewrites. Update docs when those change.
- **When to update:**
  - New route → `05_API_Documentation.md` + `03_System_Architecture.md` flow.
  - New env var → `08_Environment_Configuration.md`.
  - Schema change → `04_Data_Model.md` ERD + `models.py:11` + `sql/` if legacy.
  - Deploy change → `09_Deployment_Guide.md` + `vercel.json` snippet.

## Review Checklist (per change)
- [ ] Did `pyproject.toml:16` entrypoint change? Update `09`, `06`, `README`.
- [ ] Did `requires-python` change? Update `07`, `09`.
- [ ] Did `amount` validation change? Update `02`, `05`, `11`.
- [ ] Did `DB_PATH` change? Update `04`, `11`, `23`.
- [ ] Run `py -m py_compile pnl_analyzer/backend/*.py` and `python pnl_analyzer/backend/tests/test_calculations.py` before docs claim pass.

## Ownership
- **Docs owner:** Future maintainer (see `20_Development`).
- **Location:** `docs/` committed to `main`. No external wiki.
- **Format:** Markdown, Mermaid for diagrams (tested via `mermaid.live`).

## Stale Detection
- Grep `pnl-analyzer` hyphen every release — should be 0 in `pyproject`/`vercel.json` (allow in `README` history).
- Compare `05_API` route table vs `grep -n "@app.route" pnl_analyzer/backend/app.py`.

## No Auto-Generation
Docs are hand-maintained; no `mkdocs` build. Keep `docs/README.md` Handover Checklist updated.

## Last Audited
2026-09-23 — verified against `main@c5f8e43` + `pyproject.toml >=3.10` + `models.py /tmp`.
