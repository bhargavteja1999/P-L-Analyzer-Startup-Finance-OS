# 21 — Operations and Monitoring

## What Exists
- **Logs:** `print` to stdout in `app.py:47` `Mongo init done`, `models.py` `print` on seed. Vercel captures stdout in Function logs (Dashboard → Logs).
- **Health checks:** `GET /api/health` → `{"status":"ok"}` and `GET /api/mongo/health` → `{available, db}`. No liveness/readiness probe beyond that.
- **Operational commands:** See `07_Local_Setup` curl checks.

## What Does NOT Exist (`Not Applicable` / `Missing`)
- **No APM:** No Datadog, New Relic, Sentry, PagerDuty.
- **No metrics:** No Prometheus, no `pnl.db` size alert.
- **No alerting:** Vercel email on deploy failure only.
- **No error tracking:** Flask `500` HTML, not JSON, not sent to tracker.
- **No rollback script:** Vercel Dashboard → Promote previous deployment is manual.
- **No runbook:** Beyond `11_Troubleshooting.md`.

## Incident Response (current)
1. Check Vercel Function logs for `SQLite init skipped` or `Mongo init skipped`.
2. `curl https://<deploy>/api/health` → 200.
3. `curl https://<deploy>/api/mongo/health` → `available` true/false.
4. If `500`, check `VERCEL=1` + `/tmp` DB per `models.py:15`.
5. Redeploy via `git push`.

## Rollback
Vercel → Deployments → Latest failed → Previous → Promote. DB is ephemeral, so data lost — no DB rollback.

## Missing Operationally Important
- Log retention, rotation, structured JSON logs — **Not Applicable**.
