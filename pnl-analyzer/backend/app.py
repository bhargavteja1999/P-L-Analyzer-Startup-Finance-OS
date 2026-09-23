"""
Flask API - Clean separation: routes call calculation engine.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from calculations import *
from models import init_db, get_db
import json
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except: pass
# Mongo optional (keep SQLite) — lazy init, never breaks if Mongo down
try:
    from mongo_models import get_mongo_db, init_mongo_db, is_mongo_available, mongo_id_str, MONGO_URI as MONGO_URI_MONGO
    HAS_MONGO = True
    MONGO_URI = MONGO_URI_MONGO
except ImportError:
    HAS_MONGO = False
    MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017")
    def is_mongo_available(): return False
    def get_mongo_db(): raise RuntimeError("mongo not available")
    def init_mongo_db(): return False

app = Flask(__name__)
CORS(app)
init_db()
# try init mongo in background — don't fail if offline (mongomock fallback ensures same data as SQLite even without real Mongo)
try:
    if HAS_MONGO:
        init_mongo_db()
        print("Mongo init done — mock fallback ensures same 12-month demo as SQLite")
except Exception as e:
    print("Mongo init skipped:", e)

def month_pnl(business_id, month_id):
    conn = get_db()
    rev = [dict(r) for r in conn.execute("SELECT * FROM revenue WHERE business_id=? AND month_id=?", (business_id, month_id))]
    cogs = [dict(r) for r in conn.execute("SELECT * FROM cogs WHERE business_id=? AND month_id=?", (business_id, month_id))]
    exps = [dict(r) for r in conn.execute("SELECT * FROM expenses WHERE business_id=? AND month_id=?", (business_id, month_id))]
    conn.close()
    return calculate_pnl(rev, cogs, exps), rev, cogs, exps

@app.route("/api/health")
def health(): return jsonify({"status":"ok"})

@app.route("/api/businesses")
def businesses():
    conn=get_db(); rows=[dict(r) for r in conn.execute("SELECT * FROM businesses")]; conn.close(); return jsonify(rows)

@app.route("/api/months/<int:biz_id>")
def months(biz_id):
    conn=get_db(); rows=[dict(r) for r in conn.execute("SELECT * FROM months WHERE business_id=? ORDER BY year, month_index", (biz_id,))]; conn.close(); return jsonify(rows)

@app.route("/api/revenue", methods=["GET","POST"])
def revenue_route():
    if request.method=="POST":
        d=request.json
        if d["amount"]<0: return jsonify({"error":"Negative not allowed"}),400
        conn=get_db(); conn.execute("INSERT INTO revenue (business_id, month_id, source, amount) VALUES (?,?,?,?)",(d["business_id"],d["month_id"],d["source"],d["amount"])); conn.commit(); conn.close()
        return jsonify({"ok":True}),201
    biz=request.args.get("business_id"); mid=request.args.get("month_id")
    conn=get_db(); rows=[dict(r) for r in conn.execute("SELECT * FROM revenue WHERE business_id=? AND month_id=?",(biz,mid))]; conn.close(); return jsonify(rows)

@app.route("/api/revenue/<int:id>", methods=["DELETE"])
def del_rev(id):
    conn=get_db(); conn.execute("DELETE FROM revenue WHERE id=?",(id,)); conn.commit(); conn.close(); return jsonify({"ok":True})

@app.route("/api/cogs", methods=["GET","POST"])
def cogs_route():
    if request.method=="POST":
        d=request.json
        if d["amount"]<0: return jsonify({"error":"Negative not allowed"}),400
        conn=get_db(); conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(d["business_id"],d["month_id"],d["source"],d["amount"])); conn.commit(); conn.close()
        return jsonify({"ok":True}),201
    biz=request.args.get("business_id"); mid=request.args.get("month_id")
    conn=get_db(); rows=[dict(r) for r in conn.execute("SELECT * FROM cogs WHERE business_id=? AND month_id=?",(biz,mid))]; conn.close(); return jsonify(rows)

@app.route("/api/cogs/<int:id>", methods=["DELETE"])
def del_cogs(id):
    conn=get_db(); conn.execute("DELETE FROM cogs WHERE id=?",(id,)); conn.commit(); conn.close(); return jsonify({"ok":True})

@app.route("/api/expenses", methods=["GET","POST"])
def exp_route():
    if request.method=="POST":
        d=request.json
        if d["amount"]<0: return jsonify({"error":"Negative not allowed"}),400
        conn=get_db(); conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(d["business_id"],d["month_id"],d["category"],d["amount"])); conn.commit(); conn.close()
        return jsonify({"ok":True}),201
    biz=request.args.get("business_id"); mid=request.args.get("month_id")
    conn=get_db(); rows=[dict(r) for r in conn.execute("SELECT * FROM expenses WHERE business_id=? AND month_id=?",(biz,mid))]; conn.close(); return jsonify(rows)

@app.route("/api/expenses/<int:id>", methods=["DELETE"])
def del_exp(id):
    conn=get_db(); conn.execute("DELETE FROM expenses WHERE id=?",(id,)); conn.commit(); conn.close(); return jsonify({"ok":True})

@app.route("/api/pnl")
def pnl():
    try:
        biz = request.args.get("business_id")
        mid = request.args.get("month_id")
        if not biz or not mid or mid == "undefined" or biz == "undefined":
            return jsonify({"error":"month_id and business_id required. Example: ?business_id=1&month_id=9 (Sept). Get valid ids from GET /api/months/1"}), 400
        biz=int(biz); mid=int(mid)
    except (ValueError, TypeError):
        return jsonify({"error":"month_id must be integer. Use GET /api/months/1 to get valid ids"}), 400
    data, rev, cogs, exps = month_pnl(biz, mid)
    return jsonify({"pnl":data, "revenue":rev, "cogs":cogs, "expenses":exps})

@app.route("/api/dashboard/<int:biz_id>")
def dashboard(biz_id):
    conn=get_db()
    months_rows=[dict(r) for r in conn.execute("SELECT * FROM months WHERE business_id=? ORDER BY year, month_index",(biz_id,))]
    conn.close()
    pnls=[]
    for m in months_rows:
        p,_,_,_=month_pnl(biz_id, m["id"])
        pnls.append({**p, "month":m["month_name"]})
    yearly = yearly_summary([{"total_revenue":p["total_revenue"],"total_cogs":p["total_cogs"],"total_opex":p["total_opex"]} for p in pnls])
    return jsonify({"monthly":pnls, "yearly":yearly})

@app.route("/api/forecast")
def forecast():
    sc=int(request.args.get("start_customers",1000)); gr=float(request.args.get("growth",10)); price=float(request.args.get("price",10)); mc=int(request.args.get("months",12)); cp=float(request.args.get("cogs_pct",15)); ob=float(request.args.get("opex_base",5000)); og=float(request.args.get("opex_growth",4))
    return jsonify(calculate_forecast(sc,gr,price,mc,cp,ob,og))

@app.route("/api/break-even")
def be():
    f=float(request.args.get("fixed",5000)); r=float(request.args.get("revenue_per",10)); v=float(request.args.get("variable",2))
    return jsonify(calculate_break_even(f,r,v))

@app.route("/api/scenario", methods=["POST"])
def scenario():
    d=request.json; conn=get_db(); conn.execute("INSERT INTO scenarios (business_id, name, params_json) VALUES (?,?,?)",(d.get("business_id",1), d.get("name","Scenario"), json.dumps(d))); conn.commit(); conn.close(); return jsonify({"ok":True})

@app.route("/api/businesses", methods=["POST"])
def create_business():
    d=request.json
    name=d.get("name","").strip()
    if not name: return jsonify({"error":"name required"}),400
    conn=get_db()
    conn.execute("INSERT INTO businesses (name) VALUES (?)",(name,))
    biz_id=conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    for i,m in enumerate(months,1):
        conn.execute("INSERT INTO months (business_id, month_index, month_name, year) VALUES (?,?,?,?)",(biz_id,i,m,2026))
    # seed minimal demo for new biz (copy from biz 1 if exists)
    conn.commit(); conn.close()
    return jsonify({"id":biz_id, "name":name}),201

@app.route("/api/businesses/<int:biz_id>", methods=["DELETE"])
def delete_business(biz_id):
    conn=get_db()
    exists=conn.execute("SELECT id, name FROM businesses WHERE id=?",(biz_id,)).fetchone()
    if not exists:
        conn.close(); return jsonify({"error":"Business not found"}),404
    cnt=conn.execute("SELECT COUNT(*) as c FROM businesses").fetchone()["c"]
    if cnt<=1:
        conn.close(); return jsonify({"error":"Cannot delete last business — at least one must remain"}),400
    # cascade delete months + financial data
    month_ids=[r["id"] for r in conn.execute("SELECT id FROM months WHERE business_id=?",(biz_id,))]
    for mid in month_ids:
        conn.execute("DELETE FROM revenue WHERE business_id=? AND month_id=?",(biz_id, mid))
        conn.execute("DELETE FROM cogs WHERE business_id=? AND month_id=?",(biz_id, mid))
        conn.execute("DELETE FROM expenses WHERE business_id=? AND month_id=?",(biz_id, mid))
    conn.execute("DELETE FROM months WHERE business_id=?",(biz_id,))
    conn.execute("DELETE FROM businesses WHERE id=?",(biz_id,))
    try: conn.execute("DELETE FROM scenarios WHERE business_id=?",(biz_id,))
    except: pass
    try: conn.execute("DELETE FROM audit_log WHERE business_id=?",(biz_id,))
    except: pass
    conn.commit(); conn.close()
    if HAS_MONGO and is_mongo_available():
        try:
            db=get_mongo_db()
            biz_str=str(biz_id)
            # delete mongo financial data (businesses in mongo use string ids)
            db.revenue.delete_many({"business_id": biz_str})
            db.cogs.delete_many({"business_id": biz_str})
            db.expenses.delete_many({"business_id": biz_str})
            db.months.delete_many({"business_id": biz_str})
            # try deleting business doc by int or string
            try:
                from bson import ObjectId
                # businesses collection may have _id as ObjectId or int — try both
                db.businesses.delete_many({"$or":[{"_id": biz_id},{"business_id": biz_str},{"biz_seq_id": biz_id}]})
            except:
                db.businesses.delete_many({"business_id": biz_str})
        except Exception as e:
            print("Mongo delete business skipped:", e)
    return jsonify({"ok":True, "deleted_id": biz_id, "name": exists["name"]})

@app.route("/api/users")
def users():
    conn=get_db(); rows=[dict(r) for r in conn.execute("SELECT * FROM users")]; conn.close(); return jsonify(rows)

@app.route("/api/gst")
def gst():
    amount=float(request.args.get("amount",0)); rate=float(request.args.get("rate",18))
    return jsonify(calculate_gst(amount, rate))

@app.route("/api/fy/<int:biz_id>")
def fy(biz_id):
    conn=get_db()
    months_rows=[dict(r) for r in conn.execute("SELECT * FROM months WHERE business_id=? ORDER BY year, month_index",(biz_id,))]
    conn.close()
    pnls=[]
    for m in months_rows:
        p,_,_,_=month_pnl(biz_id, m["id"])
        pnls.append({**p, "month":m["month_name"]})
    fy_sum = calculate_fy_summary(pnls, 4)
    anomalies = detect_anomalies([p["net_profit"] for p in pnls])
    ma = calculate_moving_average([p["total_revenue"] for p in pnls], 3)
    return jsonify({"fy":fy_sum, "anomalies":anomalies, "moving_avg_revenue":ma})

@app.route("/api/import", methods=["POST"])
def import_csv():
    d=request.json
    biz=int(d.get("business_id",1)); mid=int(d.get("month_id")); rows=d.get("rows",[])  # rows: [{type,revenue|cogs|expense, source, amount}]
    conn=get_db()
    count=0
    for r in rows:
        try:
            amt=float(r.get("amount",0))
            if amt<0: continue
            t=r.get("type","revenue")
            src=r.get("source") or r.get("category") or "Imported"
            if t=="revenue":
                conn.execute("INSERT INTO revenue (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz,mid,src,amt))
            elif t=="cogs":
                conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz,mid,src,amt))
            else:
                conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz,mid,src,amt))
            count+=1
        except: continue
    conn.commit(); conn.close()
    return jsonify({"imported":count})

@app.route("/api/reset-demo", methods=["POST"])
def reset_demo():
    """Reset demo data for a business — fixes Load Demo button in SQL mode"""
    d=request.json or {}
    biz_id=int(d.get("business_id",1))
    conn=get_db()
    # clear existing
    conn.execute("DELETE FROM revenue WHERE business_id=?", (biz_id,))
    conn.execute("DELETE FROM cogs WHERE business_id=?", (biz_id,))
    conn.execute("DELETE FROM expenses WHERE business_id=?", (biz_id,))
    # reseed 12 months demo (same as models.py)
    baseRev=[6000,7000,8000,9000,9500,10000,10500,11000,20000,11500,12000,13000]
    baseCogs=[900,1050,1200,1350,1425,1500,1575,1650,1500,1725,1800,1950]
    baseOpex=[4000,4200,4500,4700,4800,5000,5100,5200,5000,5400,5500,5800]
    for idx in range(12):
        mi=idx+1
        row=conn.execute("SELECT id FROM months WHERE business_id=? AND month_index=? AND year=2026",(biz_id, mi)).fetchone()
        if not row: continue
        mid=row["id"]
        conn.execute("INSERT INTO revenue (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid, "Subscription Revenue", baseRev[idx]))
        conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid, "Cloud Hosting", round(baseCogs[idx]*0.66)))
        conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid, "Database", round(baseCogs[idx]*0.20)))
        conn.execute("INSERT INTO cogs (business_id, month_id, source, amount) VALUES (?,?,?,?)",(biz_id, mid, "Payment Fees", round(baseCogs[idx]*0.14)))
        conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid, "Marketing", round(baseOpex[idx]*0.40)))
        conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid, "Salaries", round(baseOpex[idx]*0.40)))
        conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid, "Software", round(baseOpex[idx]*0.10)))
        conn.execute("INSERT INTO expenses (business_id, month_id, category, amount) VALUES (?,?,?,?)",(biz_id, mid, "Other", round(baseOpex[idx]*0.10)))
    conn.commit(); conn.close()
    return jsonify({"ok":True, "message":"Demo data reset for business "+str(biz_id)})

@app.route("/api/audit")
def audit():
    biz=request.args.get("business_id")
    conn=get_db()
    q="SELECT * FROM audit_log ORDER BY created_at DESC LIMIT 50"
    params=()
    if biz:
        q="SELECT * FROM audit_log WHERE business_id=? ORDER BY created_at DESC LIMIT 50"
        params=(biz,)
    rows=[dict(r) for r in conn.execute(q, params)]; conn.close(); return jsonify(rows)

# ========== MONGO API (keep SQLite) ==========
def mongo_month_pnl(business_id, month_id):
    """Calculate P&L from Mongo collections"""
    db = get_mongo_db()
    biz_str = str(business_id)
    # month_id in mongo is 1..12 (biz_seq)
    mid = int(month_id)
    rev_docs = list(db.revenue.find({"business_id": biz_str, "month_id": mid}))
    cogs_docs = list(db.cogs.find({"business_id": biz_str, "month_id": mid}))
    exp_docs = list(db.expenses.find({"business_id": biz_str, "month_id": mid}))
    # normalize for calculations.py
    rev = [{"amount": float(d["amount"])} for d in rev_docs]
    cogs = [{"amount": float(d["amount"])} for d in cogs_docs]
    exps = [{"amount": float(d["amount"])} for d in exp_docs]
    pnl = calculate_pnl(rev, cogs, exps)
    # add ids for frontend delete
    for d in rev_docs: d["_id"]=str(d["_id"]); d["id"]=d["_id"]; d["source"]=d.get("source","")
    for d in cogs_docs: d["_id"]=str(d["_id"]); d["id"]=d["_id"]; d["source"]=d.get("source","")
    for d in exp_docs: d["_id"]=str(d["_id"]); d["id"]=d["_id"]; d["category"]=d.get("category","")
    return pnl, rev_docs, cogs_docs, exp_docs

@app.route("/api/mongo/health")
def mongo_health():
    try:
        if not HAS_MONGO:
            return jsonify({"status":"pymongo not installed", "available": False}), 200
        ok = is_mongo_available()
        if not ok:
            return jsonify({"status":"mongo not reachable — set MONGO_URI (mongodb://localhost:27017 or Atlas) and ensure mongod running", "mongo_uri": MONGO_URI[:40], "available": False, "hint": "Frontend will work in Local/SQL mode. Mongo is optional."}), 200
        db = get_mongo_db()
        return jsonify({"status":"ok","db": db.name, "businesses": db.businesses.count_documents({}), "available": True})
    except Exception as e:
        return jsonify({"status":"error","error": str(e), "available": False}), 200

@app.route("/api/mongo/months/<biz_id>")
def mongo_months(biz_id):
    if not is_mongo_available():
        return jsonify({"error":"Mongo not reachable. Set MONGO_URI env and ensure mongod/Atlas running"}), 503
    db = get_mongo_db()
    rows = list(db.months.find({"business_id": str(biz_id)}).sort([("month_index",1)]) if db.months.find_one({"business_id": str(biz_id)}) else db.months.find({"biz_seq_id": {"$exists": True}}).sort([("month_index",1)]))
    # fallback: if business_id as string not found, use _id 1..12
    if not rows:
        rows = list(db.months.find().sort([("month_index",1)]))
        # map to expected shape
        for r in rows:
            r["id"] = r.get("_id") if isinstance(r.get("_id"), int) else r.get("biz_seq_id", 1)
            r["business_id"] = biz_id
    else:
        for r in rows:
            r["id"] = r.get("_id") if isinstance(r.get("_id"), int) else r.get("biz_seq_id")
            r["business_id"] = biz_id
            r["_id"] = str(r["_id"])
    # ensure 12 rows
    return jsonify(rows[:12])

@app.route("/api/mongo/pnl")
def mongo_pnl():
    if not is_mongo_available():
        return jsonify({"error":"Mongo not reachable"}), 503
    try:
        biz = request.args.get("business_id")
        mid = request.args.get("month_id")
        if not biz or not mid or mid=="undefined":
            return jsonify({"error":"business_id and month_id required"}),400
        biz=int(biz); mid=int(mid)
    except: return jsonify({"error":"invalid id"}),400
    pnl, rev, cogs, exps = mongo_month_pnl(biz, mid)
    return jsonify({"pnl": pnl, "revenue": rev, "cogs": cogs, "expenses": exps})

@app.route("/api/mongo/dashboard/<int:biz_id>")
def mongo_dashboard(biz_id):
    if not is_mongo_available():
        return jsonify({"error":"Mongo not reachable"}), 503
    db = get_mongo_db()
    months_rows = list(db.months.find().sort([("month_index",1)]))[:12]
    pnls=[]
    for m in months_rows:
        mid = m.get("_id") if isinstance(m.get("_id"), int) else m.get("biz_seq_id",1)
        p,_,_,_=mongo_month_pnl(biz_id, mid)
        pnls.append({**p, "month": m.get("month_name","M"+str(mid))})
    yearly = yearly_summary([{"total_revenue":p["total_revenue"],"total_cogs":p["total_cogs"],"total_opex":p["total_opex"]} for p in pnls])
    return jsonify({"monthly": pnls, "yearly": yearly})

@app.route("/api/mongo/reset-demo", methods=["POST"])
def mongo_reset_demo():
    if not is_mongo_available():
        return jsonify({"error":"Mongo not reachable. Set MONGO_URI"}), 503
    d=request.json or {}
    biz_id=str(d.get("business_id",1))
    db=get_mongo_db()
    # ensure business exists
    biz = db.businesses.find_one()
    if not biz:
        init_mongo_db()
        biz = db.businesses.find_one()
        biz_id = str(biz["_id"])
    db.revenue.delete_many({"business_id": biz_id})
    db.cogs.delete_many({"business_id": biz_id})
    db.expenses.delete_many({"business_id": biz_id})
    baseRev=[6000,7000,8000,9000,9500,10000,10500,11000,30000,11500,12000,13000]
    baseCogs=[900,1050,1200,1350,1425,1500,1575,1650,1500,1725,1800,1950]
    baseOpex=[4000,4200,4500,4700,4800,5000,5100,5200,5000,5400,5500,5800]
    for idx in range(12):
        mid=idx+1
        db.revenue.insert_one({"business_id": biz_id, "month_id": mid, "source": "Subscription Revenue", "amount": baseRev[idx]})
        db.cogs.insert_one({"business_id": biz_id, "month_id": mid, "source": "Cloud Hosting", "amount": round(baseCogs[idx]*0.66)})
        db.cogs.insert_one({"business_id": biz_id, "month_id": mid, "source": "Database", "amount": round(baseCogs[idx]*0.20)})
        db.cogs.insert_one({"business_id": biz_id, "month_id": mid, "source": "Payment Fees", "amount": round(baseCogs[idx]*0.14)})
        db.expenses.insert_one({"business_id": biz_id, "month_id": mid, "category": "Marketing", "amount": round(baseOpex[idx]*0.40)})
        db.expenses.insert_one({"business_id": biz_id, "month_id": mid, "category": "Salaries", "amount": round(baseOpex[idx]*0.40)})
        db.expenses.insert_one({"business_id": biz_id, "month_id": mid, "category": "Software", "amount": round(baseOpex[idx]*0.10)})
        db.expenses.insert_one({"business_id": biz_id, "month_id": mid, "category": "Other", "amount": round(baseOpex[idx]*0.10)})
    return jsonify({"ok":True})

@app.route("/api/mongo/revenue", methods=["GET","POST"])
def mongo_revenue():
    if not is_mongo_available():
        return jsonify({"error":"Mongo not reachable"}), 503
    db=get_mongo_db()
    if request.method=="POST":
        d=request.json or {}
        if float(d.get("amount",0))<0: return jsonify({"error":"Negative not allowed"}),400
        biz=str(d.get("business_id","1")); mid=int(d.get("month_id",1))
        doc={"business_id":biz,"month_id":mid,"source":d.get("source",""),"amount":float(d.get("amount",0))}
        res=db.revenue.insert_one(doc)
        return jsonify({"ok":True,"id":str(res.inserted_id)}),201
    biz=request.args.get("business_id","1"); mid=request.args.get("month_id")
    q={"business_id": str(biz)}
    if mid: q["month_id"]=int(mid)
    rows=list(db.revenue.find(q))
    for r in rows: r["_id"]=str(r["_id"]); r["id"]=r["_id"]
    return jsonify(rows)

@app.route("/api/mongo/revenue/<id>", methods=["DELETE"])
def mongo_del_revenue(id):
    if not is_mongo_available(): return jsonify({"error":"Mongo not reachable"}),503
    db=get_mongo_db()
    try:
        from bson import ObjectId
        oid=ObjectId(id) if len(id)==24 else id
    except: oid=id
    try: db.revenue.delete_one({"_id": oid})
    except: db.revenue.delete_one({"_id": id})
    return jsonify({"ok":True})

@app.route("/api/mongo/cogs", methods=["GET","POST"])
def mongo_cogs():
    if not is_mongo_available(): return jsonify({"error":"Mongo not reachable"}),503
    db=get_mongo_db()
    if request.method=="POST":
        d=request.json or {}
        if float(d.get("amount",0))<0: return jsonify({"error":"Negative not allowed"}),400
        biz=str(d.get("business_id","1")); mid=int(d.get("month_id",1))
        doc={"business_id":biz,"month_id":mid,"source":d.get("source",""),"amount":float(d.get("amount",0))}
        res=db.cogs.insert_one(doc)
        return jsonify({"ok":True,"id":str(res.inserted_id)}),201
    biz=request.args.get("business_id","1"); mid=request.args.get("month_id")
    q={"business_id": str(biz)}
    if mid: q["month_id"]=int(mid)
    rows=list(db.cogs.find(q))
    for r in rows: r["_id"]=str(r["_id"]); r["id"]=r["_id"]
    return jsonify(rows)

@app.route("/api/mongo/cogs/<id>", methods=["DELETE"])
def mongo_del_cogs(id):
    if not is_mongo_available(): return jsonify({"error":"Mongo not reachable"}),503
    db=get_mongo_db()
    try:
        from bson import ObjectId
        oid=ObjectId(id) if len(id)==24 else id
    except: oid=id
    try: db.cogs.delete_one({"_id": oid})
    except: db.cogs.delete_one({"_id": id})
    return jsonify({"ok":True})

@app.route("/api/mongo/expenses", methods=["GET","POST"])
def mongo_expenses():
    if not is_mongo_available(): return jsonify({"error":"Mongo not reachable"}),503
    db=get_mongo_db()
    if request.method=="POST":
        d=request.json or {}
        if float(d.get("amount",0))<0: return jsonify({"error":"Negative not allowed"}),400
        biz=str(d.get("business_id","1")); mid=int(d.get("month_id",1))
        doc={"business_id":biz,"month_id":mid,"category":d.get("category", d.get("source","")),"amount":float(d.get("amount",0))}
        res=db.expenses.insert_one(doc)
        return jsonify({"ok":True,"id":str(res.inserted_id)}),201
    biz=request.args.get("business_id","1"); mid=request.args.get("month_id")
    q={"business_id": str(biz)}
    if mid: q["month_id"]=int(mid)
    rows=list(db.expenses.find(q))
    for r in rows: r["_id"]=str(r["_id"]); r["id"]=r["_id"]
    return jsonify(rows)

@app.route("/api/mongo/expenses/<id>", methods=["DELETE"])
def mongo_del_expenses(id):
    if not is_mongo_available(): return jsonify({"error":"Mongo not reachable"}),503
    db=get_mongo_db()
    try:
        from bson import ObjectId
        oid=ObjectId(id) if len(id)==24 else id
    except: oid=id
    try: db.expenses.delete_one({"_id": oid})
    except: db.expenses.delete_one({"_id": id})
    return jsonify({"ok":True})

if __name__=="__main__":
    import os as _os
    _debug = _os.getenv("FLASK_DEBUG","0")=="1"
    app.run(debug=_debug, port=5000, use_reloader=_debug)
