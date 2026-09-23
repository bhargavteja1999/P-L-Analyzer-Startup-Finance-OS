# 08 — Environment Configuration

**Where consumed:** `ai/ai_assistant.py:12`, `pnl_analyzer/backend/mongo_models.py:23`, `pnl_analyzer/backend/app.py:19`.

| Variable | Purpose | Required | Where | Example | Source |
|----------|---------|----------|-------|---------|--------|
| `MONGO_URI` | Mongo connection (Atlas or local) | Optional | `mongo_models.py:23` `MONGO_URI=mongodb://localhost:27017` | `mongodb://localhost:27017` or `mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true` | `pnl_analyzer/backend/.env.example:1` |
| `MONGO_DB` | DB name | Optional | `mongo_models.py:24` | `pnl_analyzer` | `.env.example:2` |
| `GOOGLE_API_KEY` or `api_key` param | Gemini auth | Optional | `ai/ai_assistant.py:14` `FinancialAIAssistant(api_key)` | `AIza...` | Not in `.env.example` — **Not Confirmed** env name |
| `FLASK_DEBUG` | Run debug | Optional | `app.py:516` `FLASK_DEBUG=="1"` | `0` or `1` | — |
| `VERCEL` | Auto-set by Vercel (`1`) | Auto | `models.py:15` switches DB to `/tmp/pnl.db` | `1` | Vercel |

**`.env` files:** Only `pnl_analyzer/backend/.env.example` exists. No root `.env.example`. Create `pnl_analyzer/backend/.env` from example for local Mongo.

**Browser-exposed:** None. `MONGO_URI` is server-only, not leaked to `js/app.js` (which uses `API_BASE=http://localhost:5000` hardcoded).

**Secrets handling:** No secrets committed; `load_dotenv()` in `app.py:20` and `ai_assistant.py` loads `.env`. Vercel env vars set via Dashboard → Settings → Environment Variables.

**Safe example `.env`:**
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=pnl_analyzer
# GOOGLE_API_KEY=AIza...
```

**Missing:** No `DATABASE_URL`, `SECRET_KEY`, `PORT` (hardcoded 5000).
