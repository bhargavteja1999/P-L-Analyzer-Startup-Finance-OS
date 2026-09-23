# 18 — External Integrations

| Service | Purpose | Integration Point | Auth | Config | Data Sent/Received | Failure | Risk |
|---------|---------|-------------------|------|--------|-------------------|---------|------|
| **MongoDB** (Atlas or local) | Optional third data source, same calcs | `pnl_analyzer/backend/mongo_models.py:1` `get_mongo_db()` `MONGO_URI`, `MONGO_DB` | URI string | `MONGO_URI=mongodb://localhost:27017` or `srv://...` in `.env` + Vercel env | Send: `business_id, month_id, source/amount`; Receive: docs for P&L | `is_mongo_available()` ping 2s, falls back to `mongomock` in-memory (`_USE_MOCK`) → same 12-month demo but `baseRev[8]=30000` vs SQLite 20000; `503` if truly unreachable | Atlas downtime → local `mongomock` still works, but data not persisted |
| **Google Gemini** | AI finance Q&A | `ai/ai_assistant.py:42` `google.genai.Client(api_key).models.generate_content('gemini-2.5-flash', ...)` | `api_key` passed to `FinancialAIAssistant` | `GOOGLE_API_KEY` env (Not in `.env.example`, **Assumption** name) | Send: `FINANCIAL_ANALYST_SYSTEM_PROMPT` + `_format_context` (totals, category_summary) + user query; Receive: markdown text | Catch `Exception` → `_offline_response` keyword router (revenue/expense/profit) → static bullets | Key missing/cost → offline fallback always works |
| **Chart.js CDN** | Dashboard charts | `pnl_analyzer/index.html:11` `cdn.jsdelivr.net/npm/chart.js@4.4.0` | none | URL | Data: monthly revenue/profit arrays → charts | Offline → charts blank, app still works |
| **jsPDF CDN** | PDF export | `index.html:12` `cdnjs jspdf 2.5.1` | none | URL | P&L table → PDF (uses `Rs.` not `₹` for Helvetica) | Offline → PDF button fails |
| **Google Fonts** | Inter font | `index.html:8` `fonts.googleapis.com` | none | URL | — | Offline → fallback system font |
| **Vercel** | Hosting serverless Python + static | `pyproject.toml:16` `entrypoint`, `vercel.json:3` | git push | `Root` `.` or `pnl_analyzer`, env `MONGO_URI` | Code + deps → serverless | Build fails if `requires-python` mismatch (fixed to `>=3.10`) |

**No integrations:** Payments, email, webhooks, auth providers, analytics, storage (S3), vector DB (**Not Applicable**).

**Evidence:** `ai/prompts.py:1` templates, `python/data_loader.py` no external, `requirements.txt:10` `google-genai`.
