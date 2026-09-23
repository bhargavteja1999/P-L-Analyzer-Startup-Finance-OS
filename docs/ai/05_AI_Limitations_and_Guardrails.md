# AI 05 — Limitations and Guardrails

## Guardrails (Implemented)
- `try: generate_content except Exception: _offline_response` — prevents crash if Gemini down.
- `FINANCIAL_ANALYST_SYSTEM_PROMPT` says "no hallucination" but **no validator** checks output.

## No Guardrails
- No output parsing/validation (`pydantic`), no retry, no `max_tokens` limit, no content filter.

## Failure Modes
- **Key missing:** `FinancialAIAssistant(api_key=None)` → `generate_content` fails → offline router always.
- **Offline keyword miss:** Query "hello" → falls to else bullets, not greeting.
- **Context large:** `_format_context` string ~500 chars, but no truncation for 1200 transactions.

## Token/Cost
- `gemini-2.5-flash` pricing not tracked; no cost limiter. Each `ask()` is one call.

## Limitations
- Single-turn, no memory, no RAG → answers based only on aggregated totals, not row-level drill-down.
- Offline router is rule-based, not LLM — will be wrong for nuanced finance.

## Not Claimed
No hallucination prevention, grounding, accuracy metric — **Not Confirmed**.

## Evidence
`ai/ai_assistant.py:78` fallback, `ai/prompts.py:1` no guardrail code.
