# AI 04 — Agent and Tool Workflows

**Status: No agents, no tools, no orchestration.**

## Current Workflow
- `ai/ai_assistant.py:78` `_offline_response(query)` is **keyword router**, not LLM agent:
```python
if "revenue" in query.lower() or "sales" in query: 
    return category_summary (Services 5639759)
elif "expense" in query.lower():
    return cogs/marketing/shipping breakdown
elif "profit" in query:
    return highest_margin_category
else: return strategic bullets
```

## No Tool Calling
- No `tool_calls`, `function_calling`, `openai.tools` — `grep tool` in `ai/` only `insight_generator.py` tool-like name, but is report generation, not LLM tool.

## No Agent Orchestration
- No `langchain`, `langgraph`, `crewai`, `autogen`.

## Memory
**Not Applicable:** No `conversation_id`, no `chat_history` passed to `generate_content` (single turn).

## Evidence
`ai/ai_assistant.py:1` 126 lines, `ai/insight_generator.py:64` only Markdown, no `agent` string.
