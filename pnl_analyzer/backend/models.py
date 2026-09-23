"""
Database models - SQLite with multi-business support.
Tables: businesses, months, revenue, cogs, expenses
"""
import sqlite3
import json
import os
import shutil
import tempfile
from pathlib import Path

# Vercel serverless functions have read-only filesystem except /tmp.
# Use writable temp dir on Vercel, otherwise use repo-local pnl.db
_REPO_DB_PATH = Path(__file__).parent / "pnl.db"
# On Linux (Vercel) /tmp exists; on Windows tempfile.gettempdir() is needed for local simulation
_TMP_DIR = Path(tempfile.gettempdir()) if os.getenv("VERCEL") and not Path("/tmp").exists() else Path("/tmp")
_VERCEL_DB_PATH = _TMP_DIR / "pnl.db"
DB_PATH = _VERCEL_DB_PATH if os.getenv("VERCEL") else _REPO_DB_PATH

# Ensure /tmp DB exists on Vercel by copying seeded DB if needed
if os.getenv("VERCEL") and not _VERCEL_DB_PATH.exists() and _REPO_DB_PATH.exists():
    try:
        _VERCEL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_REPO_DB_PATH, _VERCEL_DB_PATH)
    except Exception:
        pass

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS businesses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS months (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  business_id INTEGER REFERENCES businesses(id),
  month_index INTEGER NOT NULL,
  month_name TEXT NOT NULL,
  year INTEGER NOT NULL,
  UNIQUE(business_id, month_index, year)
);
CREATE TABLE IF NOT EXISTS revenue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  business_id INTEGER REFERENCES businesses(id),
  month_id INTEGER REFERENCES months(id),
  source TEXT NOT NULL,
  amount REAL NOT NULL CHECK(amount >= 0)
);
CREATE TABLE IF NOT EXISTS cogs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  business_id INTEGER REFERENCES businesses(id),
  month_id INTEGER REFERENCES months(id),
  source TEXT NOT NULL,
  amount REAL NOT NULL CHECK(amount >= 0)
);
CREATE TABLE IF NOT EXISTS expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  business_id INTEGER REFERENCES businesses(id),
  month_id INTEGER REFERENCES months(id),
  category TEXT NOT NULL,
  amount REAL NOT NULL CHECK(amount >= 0),
  is_opex INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS scenarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  business_id INTEGER,
  name TEXT,
  params_json TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  role TEXT DEFAULT 'owner',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  business_id INTEGER,
  user_email TEXT,
  action TEXT,
  details TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

def get_db():
    # On Vercel, ensure DB file is in /tmp and handle read-only fallback
    db_path = DB_PATH
    try:
        conn = sqlite3.connect(str(db_path), timeout=30, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        # Fallback to in-memory DB if filesystem is read-only and /tmp also fails
        # This prevents FUNCTION_INVOCATION_FAILED on cold start
        try:
            conn = sqlite3.connect(":memory:", timeout=30, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception:
            raise e

def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    # seed default business if empty
    cur = conn.execute("SELECT COUNT(*) as c FROM businesses")
    if cur.fetchone()["c"] == 0:
        conn.execute("INSERT INTO businesses (name) VALUES (?)", ("AI SaaS Startup",))
        biz_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        for i,m in enumerate(months,1):
            conn.execute("INSERT INTO months (business_id, month_index, month_name, year) VALUES (?,?,?,?)", (biz_id, i, m, 2026))
        conn.commit()
        # seed demo data for September (month 9) - detailed
        mid = conn.execute("SELECT id FROM months WHERE month_index=9 AND year=2026").fetchone()["id"]
        conn.executemany("INSERT INTO revenue (business_id, month_id, source, amount) VALUES (?,?,?,?)", [
            (biz_id, mid, "Subscription Revenue", 10000),
        ])
        conn.executemany("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)", [
            (biz_id, mid, "Cloud Hosting", 1000),
            (biz_id, mid, "Database", 300),
            (biz_id, mid, "Payment Fees", 200),
        ])
        conn.executemany("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)", [
            (biz_id, mid, "Marketing", 2000),
            (biz_id, mid, "Salaries", 2000),
            (biz_id, mid, "Software", 500),
            (biz_id, mid, "Other", 500),
        ])
        # seed variation for other 11 months so SQL charts/yearly work full year
        baseRev=[6000,7000,8000,9000,9500,10000,10500,11000,20000,11500,12000,13000]
        baseCogs=[900,1050,1200,1350,1425,1500,1575,1650,1500,1725,1800,1950]
        baseOpex=[4000,4200,4500,4700,4800,5000,5100,5200,5000,5400,5500,5800]
        for idx in range(12):
            mi = idx+1
            if mi==9: continue
            mid2 = conn.execute("SELECT id FROM months WHERE month_index=? AND year=2026",(mi,)).fetchone()["id"]
            conn.execute("INSERT INTO revenue (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Subscription Revenue", baseRev[idx]))
            conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Cloud Hosting", round(baseCogs[idx]*0.66)))
            conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Database", round(baseCogs[idx]*0.20)))
            conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Payment Fees", round(baseCogs[idx]*0.14)))
            conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Marketing", round(baseOpex[idx]*0.40)))
            conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Salaries", round(baseOpex[idx]*0.40)))
            conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Software", round(baseOpex[idx]*0.10)))
            conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Other", round(baseOpex[idx]*0.10)))
        conn.commit()
    else:
        # ensure existing DB has 12 months data - backfill if only Sept existed
        cnt = conn.execute("SELECT COUNT(*) as c FROM revenue").fetchone()["c"]
        if cnt < 12:
            # clear and reseed if incomplete
            conn.execute("DELETE FROM revenue"); conn.execute("DELETE FROM cogs"); conn.execute("DELETE FROM expenses")
            biz_id = conn.execute("SELECT id FROM businesses LIMIT 1").fetchone()["id"]
            baseRev=[6000,7000,8000,9000,9500,10000,10500,11000,20000,11500,12000,13000]
            baseCogs=[900,1050,1200,1350,1425,1500,1575,1650,1500,1725,1800,1950]
            baseOpex=[4000,4200,4500,4700,4800,5000,5100,5200,5000,5400,5500,5800]
            for idx in range(12):
                mi=idx+1
                mid2 = conn.execute("SELECT id FROM months WHERE month_index=? AND year=2026",(mi,)).fetchone()["id"]
                conn.execute("INSERT INTO revenue (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Subscription Revenue", baseRev[idx]))
                conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Cloud Hosting", round(baseCogs[idx]*0.66)))
                conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Database", round(baseCogs[idx]*0.20)))
                conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Payment Fees", round(baseCogs[idx]*0.14)))
                conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Marketing", round(baseOpex[idx]*0.40)))
                conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Salaries", round(baseOpex[idx]*0.40)))
                conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Software", round(baseOpex[idx]*0.10)))
                conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid2, "Other", round(baseOpex[idx]*0.10)))
            conn.commit()
        # seed users for auth demo
        ucnt = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        if ucnt == 0:
            conn.executemany("INSERT INTO users (email, name, role) VALUES (?,?,?)", [
                ("owner@startup.in", "Owner", "owner"),
                ("accountant@startup.in", "Accountant", "accountant"),
                ("viewer@startup.in", "Viewer", "viewer"),
            ])
            conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized at", DB_PATH)
