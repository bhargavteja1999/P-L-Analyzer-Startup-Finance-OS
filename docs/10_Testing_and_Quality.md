# 10 — Testing and Quality

## Test Framework
- **Implemented:** Plain `python` asserts in `pnl_analyzer/backend/tests/test_calculations.py:1` (no `pytest`/`unittest` runner, no `package.json` test script).
- **Not Applicable:** No `pytest.ini`, `jest`, `playwright`, `cypress`.

## Test Commands
```bash
python pnl_analyzer/backend/tests/test_calculations.py  # runs 5 tests via assert
# Expected: no output = pass, AssertionError = fail
```

## Test Structure
`test_calculations.py` covers `calculations.py`:
- `test_gross()` 10000-1500=8500 85%
- `test_net()` 3500 35%
- `test_breakeven()` 5000,10,2 → contribution 8, customers 625, revenue 6250
- `test_pnl()` vs `baseRev` etc.
- `test_forecast()` months=2

## Unit / Integration / E2E
- **Unit:** Only calculations pure funcs. **Not tested:** `models.py`, `app.py` routes, `js/app.js`, `mongo_models.py`.
- **Integration:** Not Applicable — no `test_client` integration file (though `app.test_client()` works manually).
- **E2E:** Not Applicable — manual browser.

## Manual Testing (required)
- `curl http://localhost:5000/api/health`
- Add revenue with negative amount → 400
- Dashboard 12-month charts, `Load Demo Data`, `Import CSV`, `Export PDF` (check Rs. not ₹ for jsPDF Helvetica).

## Linting / Type / Build
- **Not Applicable:** No `eslint`, `flake8`, `mypy`, `black`, `prettier` config found. `requirements.txt` has no lint deps.
- **Build validation:** `py -m py_compile pnl_analyzer/backend/*.py`

## CI
**Not Applicable:** No `.github/workflows`, no Vercel checks beyond install.

## Coverage
`Not Confirmed` quantitative — 5 tests cover ~16 funcs partially, 0% for API/DB/Frontend.

## What Is NOT Tested (honest)
- All 35 Flask routes except via manual curl.
- SQLite vs Mongo divergence (Sept 20000 vs 30000).
- Frontend `localStorage` vs `sql` vs `mongo` switch.
- Vercel `/tmp` fallback.
