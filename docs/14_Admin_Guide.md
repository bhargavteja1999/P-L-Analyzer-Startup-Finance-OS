# 14 — Admin Guide

**Status: Limited — No real admin functionality implemented.**

## What Exists
- **Business management:** `POST /api/businesses` (create), `DELETE /api/businesses/<id>` (cascades, prevents last delete). No edit.
- **User list read:** `GET /api/users` returns `owner@startup.in` etc. No create/update/delete, no passwords.
- **Settings:** `Data Source` switch, `Sync`, `Reset` — available to any user (no role check).
- **Audit log read:** `GET /api/audit?business_id=` reads `audit_log` LIMIT 50, but table never written — so empty.

## What Does NOT Exist (`Not Applicable`)
- Admin dashboard, user CRUD, role assignment, permissions, password reset, invite.
- No admin env vars.
- No maintenance scripts beyond `models.py` `if __name__=="__main__": init_db()`.

## Operational Tasks (manual)
- **Add business:** Via UI `+ New Business` or `curl -X POST -H "Content-Type: application/json" -d '{"name":"NewCo"}' http://localhost:5000/api/businesses`.
- **Delete business:** UI `🗑` or `curl -X DELETE http://localhost:5000/api/businesses/2`.
- **Reset demo:** `POST /api/reset-demo` with `{"business_id":1}` reseeds 12 months.
- **Check health:** `GET /api/health` and `/api/mongo/health`.

## Security Note
All above callable without auth — do not expose admin-like deletes publicly.

## Roadmap
If admin needed, add JWT, `role` check middleware, and `users` password column (see `16_Future_Roadmap`).
