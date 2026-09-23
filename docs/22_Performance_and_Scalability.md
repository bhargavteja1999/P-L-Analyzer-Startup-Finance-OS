# 22 — Performance and Scalability

**No measured benchmarks** (`Not Confirmed` — no `k6`, `locust`, or Vercel Analytics data).

## Observed / Potential Bottlenecks (code-inspected)

| Area | Cost | Evidence | Risk |
|------|------|----------|------|
| `GET /api/dashboard/<biz_id>` | Loops 12 `month_pnl` each 3 `SELECT` → 36 queries + `yearly_summary` | `app.py:130` | `Potential Risk` — sequential, no pagination, `biz_id` with 100 months would be 300 queries |
| `GET /api/fy/<biz_id>` | Same 12 loops + `detect_anomalies` O(n) + `moving_avg` | `app.py:222` | Same |
| `init_db()` at import | Seeds 12 months × up to 7 inserts = ~84 inserts on cold start | `models.py:108` | Vercel cold start latency ~1-2s extra if `/tmp` empty |
| Frontend charts | `chart.js` 4.4.0 renders 4 canvases per dashboard | `index.html:11` | `Potential Risk` — 100+ businesses/months would lag |
| `localStorage pnl_v2` | Single JSON 12 months, grows with businesses | `js/app.js:42` | Browser 5MB limit, no eviction |
| Mongo `find` without limit | `db.revenue.find({business_id})` loads all | `mongo_models.py` | 10k docs → memory blow |

## Caching
**Not Applicable:** No `Redis`, no `lru_cache`, no `Cache-Control` headers, no ETag.

## Concurrency
- Flask dev `app.run` single-threaded locally; Vercel serverless scales per request but SQLite is file-locked (`WAL` helps but `/tmp` per-instance, not shared). **Scalability Limitation:** SQLite not shared across Vercel instances — use Mongo for multi-instance.

## AI/Token Costs
- Gemini `gemini-2.5-flash` per query cost depends on prompt (~500 tokens context + query). No token limit in `ai_assistant.py` (no `max_tokens`).

## Frontend Performance
- Vanilla JS, no bundler, CDN fonts/charts add ~200ms.

## Measured vs Risk
All above are **Potential Risks** from code read, not profiled. No `Potential Risks` claimed as measured.
