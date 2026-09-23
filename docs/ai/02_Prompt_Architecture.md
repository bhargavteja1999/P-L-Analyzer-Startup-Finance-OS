# AI 02 — Prompt Architecture

## Templates (`ai/prompts.py:1`)

**`FINANCIAL_ANALYST_SYSTEM_PROMPT` (44 lines):**
```
You are Antigravity, an expert Financial AI CFO...
4 guidelines: accuracy, no hallucination, structured, actionable.
```

**`USER_QUERY_TEMPLATE`:**
```
Context: {context_data}
User Query: {user_query}
Provide concise financial insight.
```

**`INSIGHT_GENERATION_PROMPT`:**
Placeholders: `{total_revenue, total_expense, cogs, marketing, shipping, operating, net_profit, total_transactions, top_category, top_city, highest_margin_category, low_margin_count}` → 4-section report (Health, Drivers, Risks, Recommendations).

## Construction
`ai_assistant.py:52` builds `contents=[SYSTEM_PROMPT + USER_TEMPLATE.format(context_data=_format_context(), user_query=query)]` — single list, no chat history.

## No Prompt Versioning
Prompts are hardcoded strings, not in DB or env.

## Evidence
`ai/prompts.py:10` `FINANCIAL_ANALYST_SYSTEM_PROMPT`, `ai/ai_assistant.py:55` `generate_content`.
