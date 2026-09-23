# 24 — Release and Versioning

## Versioning
**Not Applicable:** No `SEMVER`, no `CHANGELOG.md`, no `git tag`. `pyproject.toml:3` `version = "1.0.0"` static since `f334fce`, not bumped.

## Changelog Process
No `CHANGELOG`. Git history is log: `git log --oneline` shows `Updated the app.py file and models.py files`, `updated the pyproject.toml file` etc. See `15_Change_Log.md` curated.

## Build
No build step (vanilla JS + Flask). Vercel runs `uv lock` + `pip install` from `pyproject.toml`. Local no `npm run build`.

## Release
- **Process:** `git push origin main` → Vercel auto-deploys `main`. No staging branch.
- **Verification:** `curl https://<deploy>/api/health` + browser `/` → Dashboard.

## Deployment Order
1. Push `pnl_analyzer/backend/*` + `pyproject.toml` → Vercel builds function.
2. Static `pnl_analyzer/index.html` via `outputDirectory` deployed together.

## Rollback
Vercel Dashboard → Deployments → previous → Promote to Production. No `vercel rollback` CLI needed. DB is ephemeral, no data rollback.

## No Formal Release
`Not Confirmed` formal release process — recommend adding `git tag v1.0.1` + `15_Change_Log.md` entry.
