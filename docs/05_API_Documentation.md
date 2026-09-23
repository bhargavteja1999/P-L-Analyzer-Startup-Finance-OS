# 05 — API Documentation

**Base:** `http://localhost:5000` (`js/app.js: API_BASE`) or Vercel `https://<deploy>/api`. No auth. All JSON, parameterized `?`.

**Implemented routes (35):**

| Endpoint | Method | Purpose | Req | Resp | Errors | Impl |
|----------|--------|---------|-----|------|--------|------|
| `/` | GET | Serve `pnl_analyzer/index.html` or JSON | — | html/json | — | `app.py:45` `_root` |
| `/api/health` | GET | Heartbeat | — | `{"status":"ok"}` | — | `app.py:64` |
| `/api/businesses` | GET | List businesses | — | `[{id,name,created_at}]` | — | `app.py:67` |
| `/api/months/<biz_id>` | GET | 12 months | `biz_id` int | `[{id,business_id,month_index,month_name,year}]` | 404 not found? 200 empty | `app.py:71` |
| `/api/revenue?business_id=&month_id=` | GET | List revenue | query | `[{id,business_id,month_id,source,amount}]` | — | `app.py:75` |
| `/api/revenue` | POST | Add revenue | `{business_id,month_id,source,amount}` | `201 {ok:true}` | 400 Negative | `app.py:75` |
| `/api/revenue/<id>` | DELETE | Delete | id | `200` | — | `app.py:85` |
| `/api/cogs` | GET/POST | Same as revenue | — | — | 400 | `app.py:89` |
| `/api/cogs/<id>` | DELETE | — | — | — | — | `app.py:99` |
| `/api/expenses` | GET/POST | category | — | — | 400 | `app.py:103` |
| `/api/expenses/<id>` | DELETE | — | — | — | — | `app.py:113` |
| `/api/pnl?business_id=&month_id=` | GET | P&L calc | both required int | `{pnl:{total_revenue,total_cogs,gross_profit,gross_margin,total_opex,operating_profit,net_profit,net_margin,status}, revenue[], cogs[], expenses[]}` | 400 missing/invalid | `app.py:117` |
| `/api/dashboard/<biz_id>` | GET | 12-month trend | biz_id | `{monthly:[{...pnl,month}], yearly:{annual_revenue,...}}` | — | `app.py:130` |
| `/api/forecast?start_customers=&growth=&price=&months=&cogs_pct=&opex_base=&opex_growth=` | GET | Forecast table | all optional defaults 1000/10/10/12/15/5000/4 | `[{month,customers,revenue,cogs,opex,profit,gross_margin,net_margin}]` | — | `app.py:142` |
| `/api/break-even?fixed=&revenue_per=&variable=` | GET | BE | defaults 5000/10/2 | `{contribution_margin,break_even_customers,break_even_revenue,error?}` | — | `app.py:147` |
| `/api/scenario` | POST | Save scenario | `{business_id,name,params_json}` | `200` | — | `app.py:152` |
| `/api/businesses` | POST | Create biz +12 months | `{name}` | `201 {id,name}` | 400 name required | `app.py:156` |
| `/api/businesses/<biz_id>` | DELETE | Delete cascade | biz_id | `200 {deleted_id,name}` | 404/400 last | `app.py:171` |
| `/api/users` | GET | List users | — | `[{email,name,role}]` | — | `app.py:217` |
| `/api/gst?amount=&rate=18` | GET | GST calc | amount, rate | `{base,gst_rate,gst_amount,total_with_gst}` | — | `app.py:218` |
| `/api/fy/<biz_id>` | GET | FY Apr-Mar | biz_id | `{fy, anomalies[{index,z,anomaly}], moving_avg_revenue[]}` | — | `app.py:222` |
| `/api/import` | POST | Bulk rows | `{business_id,month_id,rows:[{type,source/category,amount}]}` | `{imported:count}` | — | `app.py:236` |
| `/api/reset-demo` | POST | Reseed 12m | `{business_id}` | `200` | — | `app.py:259` |
| `/api/audit?business_id=` | GET | Audit 50 | optional biz | `[{...}]` | — | `app.py:289` |
| `/api/mongo/health` | GET | Mongo ping | — | `{status,available,db}` | 200 always | `app.py:321` |
| `/api/mongo/months/<biz_id>` | GET | Mongo months | biz_id string | — | 503 not reachable | `app.py:334` |
| `/api/mongo/pnl` | GET | Mongo P&L | `business_id,month_id` | same as /api/pnl | 503/400 | `app.py:354` |
| `/api/mongo/dashboard/<biz_id>` | GET | Mongo dash | — | — | 503 | `app.py:369` |
| `/api/mongo/reset-demo` | POST | Mongo reseed 30000 Sep | — | `200` | 503 | `app.py:383` |
| `/api/mongo/revenue` | GET/POST | — | — | — | 503/400 | `app.py:413` |
| `/api/mongo/revenue/<id>` | DELETE | — | id 24hex | — | 503 | `app.py:433` |
| `/api/mongo/cogs` | GET/POST | — | — | — | — | `app.py:444` |
| `/api/mongo/cogs/<id>` | DELETE | — | — | — | — | `app.py:463` |
| `/api/mongo/expenses` | GET/POST | — | — | — | — | `app.py:475` |
| `/api/mongo/expenses/<id>` | DELETE | — | — | — | — | `app.py:503` |
| `/<path:path>` | GET | Frontend fallback/SPA | any | html or json 404 if api/* | — | `app.py:517` |

**Validation:** `amount<0 =>400`, `month_id/business_id required` `400`, `ObjectId` 24 hex handling.

**Example:** `curl http://localhost:5000/api/pnl?business_id=1&month_id=9` → `{"pnl":{"net_profit":3500,...}}`
