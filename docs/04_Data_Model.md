# 04 — Data Model

## SQLite SaaS (`pnl_analyzer/backend/models.py:11`)

`DB_PATH = Path(__file__).parent/"pnl.db"` locally, `/tmp/pnl.db` on `VERCEL=1` with `shutil.copy2` seed. Fallback `:memory:` on failure. `PRAGMA journal_mode=WAL`.

```mermaid
erDiagram
    businesses ||--o{ months : has
    businesses ||--o{ revenue : has
    businesses ||--o{ cogs : has
    businesses ||--o{ expenses : has
    months ||--o{ revenue : "month_id"
    months ||--o{ cogs : "month_id"
    months ||--o{ expenses : "month_id"
    businesses ||--o{ scenarios : has
    businesses ||--o{ audit_log : has

    businesses {
        int id PK
        text name
        text created_at
    }
    months {
        int id PK
        int business_id FK
        int month_index
        text month_name
        int year
        UNIQUE business_id month_index year
    }
    revenue {
        int id PK
        int business_id FK
        int month_id FK
        text source
        real amount CHECK>=0
    }
    cogs {
        int id PK
        int business_id FK
        int month_id FK
        text source
        real amount CHECK>=0
    }
    expenses {
        int id PK
        int business_id FK
        int month_id FK
        text category
        real amount CHECK>=0
        int is_opex
    }
    scenarios {
        int id PK
        int business_id
        text name
        text params_json
        text created_at
    }
    users {
        int id PK
        text email UNIQUE
        text name
        text role
        text created_at
    }
    audit_log {
        int id PK
        int business_id
        text user_email
        text action
        text details
        text created_at
    }
```

**Seed:** `AI SaaS Startup` + `months` Jan-Dec 2026. SQLite `baseRev 20000` for Sept, `baseCogs 1500`, `baseOpex 5000` split `40/40/10/10` Marketing/Salaries/Software/Other, `Cloud 66%, Database 20%, Payment 14%`. 3 users seeded.

**Relationships:** No FK enforcement (`REFERENCES` without `FOREIGN KEY` constraint); app enforces via deletes (`DELETE FROM months WHERE business_id=?`). `is_opex` unused.

## Mongo (`mongo_models.py:1`)

Collections `businesses{_id:1, name, created_at}`, `months{_id:1..12, business_id:"1", month_index, month_name, year, biz_seq_id}`, `revenue/cogs/expenses{business_id:"1", month_id:1..12, source/category, amount, created_at}`. Seed `baseRev[8]=30000` (intentional 10k higher than SQLite). Uses `pymongo.MongoClient` `serverSelectionTimeoutMS=2000` → fallback `mongomock`.

## Legacy Analytics DB (`data/expense_sales.db`)

Star schema `sql/02_create_tables.sql`:
- `products_dim(product_id PK, product_name UNIQUE, product_category)`
- `cities_dim(city_id PK, city_name UNIQUE, region_name)`
- `sales_reps_dim`, `sales_fact(transaction_id FK, product_id FK, city_id FK, transaction_date, revenue, cogs, marketing, shipping, operating, total_expense, net_profit)` — not used by SaaS.

## Browser Storage

`js/app.js:42` `STORAGE_KEY="pnl_v2"` JSON `{businesses, months, revenue, cogs, expenses}` in `localStorage`. `DATA_MODE` local/sql/mongo switch.

## Data Flow & Lifecycle
User add → `POST /api/revenue` → `INSERT` → `GET /api/pnl` → `SELECT` → `calculate_pnl` → response. Vercel: write to `/tmp`, ephemeral, lost on cold start.

## Indexes & Constraints
Only `UNIQUE(business_id,month_index,year)` and `CHECK(amount>=0)`, `UNIQUE email`. No other indexes.

## Not Confirmed
No migration versioning (only `CREATE TABLE IF NOT EXISTS`).
