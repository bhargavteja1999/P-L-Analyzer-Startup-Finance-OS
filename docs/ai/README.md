# AI Documentation — Overview

**Scope:** `ai/` has **no RAG/vector DB**, no agent orchestration, no memory. It is a thin Gemini wrapper + offline keyword router.

**Files:**
- `ai/ai_assistant.py:1` `FinancialAIAssistant` — main class, `google.genai` `gemini-2.5-flash`.
- `ai/prompts.py:1` — `FINANCIAL_ANALYST_SYSTEM_PROMPT`, `USER_QUERY_TEMPLATE`, `INSIGHT_GENERATION_PROMPT`.
- `ai/insight_generator.py:1` — `generate_executive_insights()` markdown report.

**Pipeline:**
```
User query → ai_assistant.py ask() → _format_context (totals) → google.genai generate_content → offline _offline_response fallback
```

**Not Applicable:** RAG, embeddings, vector DB, tools, retries, guardrails beyond try/except.

**Docs in this folder:**
- `01_AI_Architecture.md` — providers/models/flow
- `02_Prompt_Architecture.md` — templates + construction
- `03_Retrieval_and_RAG.md` — Not Applicable, explicit
- `04_Agent_and_Tool_Workflows.md` — No agents/tools, keyword router
- `05_AI_Limitations_and_Guardrails.md` — Failures/costs
