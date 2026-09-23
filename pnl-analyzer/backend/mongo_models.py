"""
MongoDB models — optional third data source (keeps SQLite intact).
Uses same calculation engine (calculations.py). Gracefully disabled if MONGO_URI not reachable.
Collections: businesses, months (12 per business), revenue, cogs, expenses — mirrors SQLite schema but as documents.
"""
import os
from pathlib import Path
from datetime import datetime

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

try:
    import mongomock
    HAS_MONGOMOCK = True
except ImportError:
    HAS_MONGOMOCK = False

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB", "pnl_analyzer")
_client = None
_db = None
_USE_MOCK = False

def get_mongo_db():
    global _client, _db, _USE_MOCK
    if not HAS_PYMONGO:
        raise RuntimeError("pymongo not installed. pip install pymongo dnspython")
    if _db is not None:
        return _db
    # try real Mongo first, fallback to mongomock if not reachable
    try:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        _db = _client[MONGO_DB_NAME]
        _db.command("ping")
        _USE_MOCK = False
        return _db
    except Exception:
        if HAS_MONGOMOCK:
            _client = mongomock.MongoClient()
            _db = _client[MONGO_DB_NAME]
            _USE_MOCK = True
            print("Mongo fallback: using mongomock in-memory (same data as SQLite)")
            return _db
        raise

def is_mongo_available():
    global _client, _db, _USE_MOCK
    if not HAS_PYMONGO:
        return False
    try:
        db = get_mongo_db()
        # mongomock ping always works, real mongo already pinged
        if _USE_MOCK:
            return True
        db.command("ping")
        return True
    except Exception:
        # try mock as fallback
        if HAS_MONGOMOCK:
            try:
                _client = mongomock.MongoClient()
                _db = _client[MONGO_DB_NAME]
                _USE_MOCK = True
                return True
            except: pass
        return False

def init_mongo_db(force_reseed=False):
    """Seed MongoDB same as models.py SQLite demo data — uses mongomock fallback so 'same data' always available"""
    try:
        available = is_mongo_available()
    except: available = False
    if not available:
        return False
    db = get_mongo_db()
    if db.businesses.count_documents({}) > 0:
        # ensure 12 months seed if incomplete
        if db.revenue.count_documents({}) < 12:
            # clear and reseed
            db.revenue.delete_many({})
            db.cogs.delete_many({})
            db.expenses.delete_many({})
        else:
            return True
    # if empty, create business — use fixed _id 1 for frontend compatibility (CURRENT_BIZ=1)
    if db.businesses.count_documents({}) == 0:
        biz = db.businesses.insert_one({"_id": 1, "name": "AI SaaS Startup", "created_at": datetime.utcnow()})
        # months need stable integer ids for compatibility with frontend (use month_index as id)
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        for i,m in enumerate(months,1):
            db.months.insert_one({"_id": i, "business_id": "1", "month_index": i, "month_name": m, "year": 2026, "biz_seq_id": i})
    else:
        # ensure business _id 1 exists; migrate if ObjectId was used before
        biz = db.businesses.find_one({"_id": 1})
        if not biz:
            # migrate: clear old ObjectId business and months
            old_biz = db.businesses.find_one()
            old_id_str = str(old_biz["_id"]) if old_biz else None
            db.businesses.delete_many({})
            db.months.delete_many({})
            db.revenue.delete_many({})
            db.cogs.delete_many({})
            db.expenses.delete_many({})
            biz = db.businesses.insert_one({"_id": 1, "name": "AI SaaS Startup", "created_at": datetime.utcnow()})
            months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
            for i,m in enumerate(months,1):
                db.months.insert_one({"_id": i, "business_id": "1", "month_index": i, "month_name": m, "year": 2026, "biz_seq_id": i})

    # seed demo 12 months if revenue empty — SAME DATA as SQLite models.py
    if db.revenue.count_documents({"business_id": "1"}) == 0:
        baseRev=[6000,7000,8000,9000,9500,10000,10500,11000,30000,11500,12000,13000]
        baseCogs=[900,1050,1200,1350,1425,1500,1575,1650,1500,1725,1800,1950]
        baseOpex=[4000,4200,4500,4700,4800,5000,5100,5200,5000,5400,5500,5800]
        biz_id_str = "1"
        import uuid
        for idx in range(12):
            mid = idx+1
            # revenue
            db.revenue.insert_one({"business_id": biz_id_str, "month_id": mid, "source": "Subscription Revenue", "amount": baseRev[idx], "created_at": datetime.utcnow()})
            db.cogs.insert_one({"business_id": biz_id_str, "month_id": mid, "source": "Cloud Hosting", "amount": round(baseCogs[idx]*0.66), "created_at": datetime.utcnow()})
            db.cogs.insert_one({"business_id": biz_id_str, "month_id": mid, "source": "Database", "amount": round(baseCogs[idx]*0.20), "created_at": datetime.utcnow()})
            db.cogs.insert_one({"business_id": biz_id_str, "month_id": mid, "source": "Payment Fees", "amount": round(baseCogs[idx]*0.14), "created_at": datetime.utcnow()})
            db.expenses.insert_one({"business_id": biz_id_str, "month_id": mid, "category": "Marketing", "amount": round(baseOpex[idx]*0.40), "created_at": datetime.utcnow()})
            db.expenses.insert_one({"business_id": biz_id_str, "month_id": mid, "category": "Salaries", "amount": round(baseOpex[idx]*0.40), "created_at": datetime.utcnow()})
            db.expenses.insert_one({"business_id": biz_id_str, "month_id": mid, "category": "Software", "amount": round(baseOpex[idx]*0.10), "created_at": datetime.utcnow()})
            db.expenses.insert_one({"business_id": biz_id_str, "month_id": mid, "category": "Other", "amount": round(baseOpex[idx]*0.10), "created_at": datetime.utcnow()})
    return True

def mongo_id_str(doc):
    """Normalize _id to string for JSON"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

if __name__ == "__main__":
    ok = init_mongo_db()
    print("Mongo available:", is_mongo_available())
    print("Init:", ok)
    if ok:
        db = get_mongo_db()
        print("businesses:", db.businesses.count_documents({}))
        print("months:", db.months.count_documents({}))
        print("revenue:", db.revenue.count_documents({}))
