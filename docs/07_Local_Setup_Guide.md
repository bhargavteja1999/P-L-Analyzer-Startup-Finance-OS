# 07 — Local Setup Guide

**Prerequisites:** Python 3.10+ (Vercel 3.12, local 3.14 tested), `pip`, `git`, browser. No Docker.

**Supported runtime:** `pyproject.toml:5` `requires-python = ">=3.10"`. Use 3.12 for Vercel parity.

## 1. Clone
```bash
git clone https://github.com/<user>/P-L-Analyzer-Startup-Finance-OS.git
cd P-L-Analyzer-Startup-Finance-OS
```

## 2. Backend deps
```bash
pip install -r pnl_analyzer/backend/requirements.txt
# contains flask==3.0.0 flask-cors==4.0.0 pymongo==4.18.1 dnspython==2.8.0 python-dotenv==1.2.3 mongomock==4.3.0 pytz==2026.3.post1
# also or via pyproject
pip install -e .
```

## 3. Env (optional Mongo)
```bash
cp pnl_analyzer/backend/.env.example pnl_analyzer/backend/.env
# edit MONGO_URI=mongodb://localhost:27017  or Atlas srv://
# If no .env, mongomock in-memory used automatically
```

## 4. DB setup
```bash
python pnl_analyzer/backend/models.py  # creates pnl_analyzer/backend/pnl.db with AI SaaS Startup + 12 months 2026
# Verify
python -c "import sqlite3; print(list(sqlite3.connect('pnl_analyzer/backend/pnl.db').execute('select count(*) from businesses')))"
```

## 5. Run SaaS (two terminals)
```bash
# Terminal 1: Flask :5000
python pnl_analyzer/backend/app.py
# health http://localhost:5000/api/health -> {"status":"ok"}

# Terminal 2: Frontend :8000 (any static server)
python -m http.server 8000 --directory pnl_analyzer
# open http://localhost:8000 → Dashboard
# Topbar monthSelect should populate, Dashboard KPIs show Sept 20000 revenue
```

**Alternative frontend:** `python -m http.server 8000 --directory pnl_analyzer/frontend` (duplicate copy).

## 6. Data pipeline (legacy, not needed for SaaS)
```bash
pip install -r requirements.txt  # pandas, numpy, etc.
python python/data_cleaning.py
python python/export_data.py  # populates data/expense_sales.db
```

## 7. AI assistant
```bash
python ai/ai_assistant.py
# requires GOOGLE_API_KEY env for Gemini 2.5-flash, else offline keyword router
```

## 8. Verification
```bash
curl http://localhost:5000/api/health
curl "http://localhost:5000/api/pnl?business_id=1&month_id=9"
python pnl_analyzer/backend/tests/test_calculations.py  # 5 tests
py -m pip check
```

## 9. Common missing pieces
- No `DATABASE_URL` needed — SQLite file path.
- No migrations command.
- No seed beyond `models.py`.

## 10. Troubleshooting setup
- `amount<0 =>400` test with `curl -X POST -H "Content-Type: application/json" -d '{"business_id":1,"month_id":9,"source":"X","amount":-1}' http://localhost:5000/api/revenue`
- `CORS` allow-all, no auth needed.
