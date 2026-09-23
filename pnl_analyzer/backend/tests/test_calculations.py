import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from calculations import *

def test_gross():
    assert calculate_gross_profit(10000,1500)==8500
    assert calculate_gross_margin(8500,10000)==85.0

def test_net():
    assert calculate_operating_profit(8500,5000)==3500
    assert calculate_net_profit(3500,0,0)==3500
    assert calculate_net_margin(3500,10000)==35.0

def test_breakeven():
    r=calculate_break_even(5000,10,2)
    assert r["contribution_margin"]==8
    assert r["break_even_customers"]==625
    assert r["break_even_revenue"]==6250

def test_pnl():
    rev=[{"amount":10000}]; cogs=[{"amount":1000},{"amount":300},{"amount":200}]; opex=[{"amount":2000},{"amount":2000},{"amount":500},{"amount":500}]
    p=calculate_pnl(rev,cogs,opex)
    assert p["gross_profit"]==8500
    assert p["total_opex"]==5000
    assert p["net_profit"]==3500
    assert p["status"]=="Profit"

def test_forecast():
    f=calculate_forecast(1000,10,10,2,15,5000,4)
    assert len(f)==2
    assert f[0]["revenue"]==10000

if __name__=="__main__":
    test_gross(); test_net(); test_breakeven(); test_pnl(); test_forecast()
    print("All tests passed")
