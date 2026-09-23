"""
Financial Calculation Engine - Pure functions, no side effects.
All formulas per spec section 2.
"""
from typing import List, Dict

def calculate_total_revenue(revenues: List[float]) -> float:
    return round(sum(revenues), 2)

def calculate_total_cogs(cogs: List[float]) -> float:
    return round(sum(cogs), 2)

def calculate_gross_profit(revenue: float, cogs: float) -> float:
    return round(revenue - cogs, 2)

def calculate_gross_margin(gross_profit: float, revenue: float) -> float:
    if revenue == 0:
        return 0.0
    return round((gross_profit / revenue) * 100, 2)

def calculate_total_opex(expenses: List[float]) -> float:
    return round(sum(expenses), 2)

def calculate_operating_profit(gross_profit: float, opex: float) -> float:
    return round(gross_profit - opex, 2)

def calculate_net_profit(operating_profit: float, other_income: float = 0, other_expenses: float = 0) -> float:
    return round(operating_profit - other_expenses + other_income, 2)

def calculate_net_margin(net_profit: float, revenue: float) -> float:
    if revenue == 0:
        return 0.0
    return round((net_profit / revenue) * 100, 2)

def calculate_break_even(fixed_costs: float, revenue_per_customer: float, variable_cost_per_customer: float) -> Dict:
    contribution = round(revenue_per_customer - variable_cost_per_customer, 2)
    if contribution <= 0:
        return {"contribution_margin": contribution, "break_even_customers": None, "break_even_revenue": None, "error": "Contribution margin must be > 0"}
    be_customers = round(fixed_costs / contribution, 2)
    be_revenue = round(be_customers * revenue_per_customer, 2)
    return {"contribution_margin": contribution, "break_even_customers": be_customers, "break_even_revenue": be_revenue}

def calculate_forecast(start_customers: int, growth_rate_pct: float, price: float, months: int, cogs_pct: float, opex_base: float, opex_growth_pct: float):
    """Generate 12-month forecast table"""
    rows = []
    customers = start_customers
    opex = opex_base
    for m in range(1, months+1):
        if m > 1:
            customers = round(customers * (1 + growth_rate_pct/100))
            opex = round(opex * (1 + opex_growth_pct/100), 2)
        revenue = round(customers * price, 2)
        cogs = round(revenue * cogs_pct/100, 2)
        gross = calculate_gross_profit(revenue, cogs)
        op_profit = calculate_operating_profit(gross, opex)
        net = calculate_net_profit(op_profit)
        rows.append({
            "month": m,
            "customers": customers,
            "revenue": revenue,
            "cogs": cogs,
            "opex": opex,
            "profit": net,
            "gross_margin": calculate_gross_margin(gross, revenue),
            "net_margin": calculate_net_margin(net, revenue)
        })
    return rows

def calculate_pnl(revenue_items: List[Dict], cogs_items: List[Dict], opex_items: List[Dict], other_income: float = 0, other_expenses: float = 0) -> Dict:
    rev = sum(x["amount"] for x in revenue_items)
    cogs = sum(x["amount"] for x in cogs_items)
    opex = sum(x["amount"] for x in opex_items)
    gross = calculate_gross_profit(rev, cogs)
    op = calculate_operating_profit(gross, opex)
    net = calculate_net_profit(op, other_income, other_expenses)
    return {
        "total_revenue": round(rev,2),
        "total_cogs": round(cogs,2),
        "gross_profit": gross,
        "gross_margin": calculate_gross_margin(gross, rev),
        "total_opex": round(opex,2),
        "operating_profit": op,
        "net_profit": net,
        "net_margin": calculate_net_margin(net, rev),
        "status": "Profit" if net > 0 else "Loss" if net < 0 else "Break-even"
    }

def yearly_summary(monthly_pnls: List[Dict]) -> Dict:
    rev = sum(m["total_revenue"] for m in monthly_pnls)
    cogs = sum(m["total_cogs"] for m in monthly_pnls)
    opex = sum(m["total_opex"] for m in monthly_pnls)
    gross = calculate_gross_profit(rev, cogs)
    op = calculate_operating_profit(gross, opex)
    net = calculate_net_profit(op)
    return {
        "annual_revenue": round(rev,2),
        "annual_cogs": round(cogs,2),
        "annual_gross_profit": gross,
        "annual_opex": round(opex,2),
        "annual_net_profit": net,
        "annual_gross_margin": calculate_gross_margin(gross, rev),
        "annual_net_margin": calculate_net_margin(net, rev)
    }

# --- v2 additions ---
def calculate_gst(amount: float, rate_pct: float = 18) -> Dict:
    gst = round(amount * rate_pct / 100, 2)
    total = round(amount + gst, 2)
    return {"base": round(amount,2), "gst_rate": rate_pct, "gst_amount": gst, "total_with_gst": total}

def calculate_fy_summary(monthly_pnls: List[Dict], fy_start_month: int = 4) -> Dict:
    """FY Apr-Mar (India). monthly_pnls assumed Jan-Dec order."""
    # reorder to FY
    fy = monthly_pnls[fy_start_month-1:] + monthly_pnls[:fy_start_month-1]
    return yearly_summary(fy)

def calculate_moving_average(values: List[float], window: int = 3) -> List[float]:
    out=[]
    for i in range(len(values)):
        w = values[max(0,i-window+1):i+1]
        out.append(round(sum(w)/len(w),2))
    return out

def detect_anomalies(values: List[float]) -> List[Dict]:
    if len(values) < 3:
        return []
    mean = sum(values)/len(values)
    var = sum((x-mean)**2 for x in values)/len(values)
    std = var**0.5
    res=[]
    for i,v in enumerate(values):
        z = (v-mean)/std if std else 0
        res.append({"index":i, "value":v, "z":round(z,2), "anomaly": abs(z) > 2})
    return res
