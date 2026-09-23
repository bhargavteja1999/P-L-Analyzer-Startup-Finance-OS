# AI 03 — Retrieval and RAG

**Status: Not Applicable — No RAG implemented.**

- **No embeddings:** No `sentence-transformers`, `openai.embeddings`, `cohere`.
- **No vector DB:** No `pinecone`, `chroma`, `faiss`, `pgvector`, `milvus`.
- **No retrieval:** `ai_assistant.py` does not search documents; it uses `_format_context()` from `python/eda.py` `generate_eda_summary()` which aggregates `data/processed/cleaned_sales_data.csv` in-memory (pandas).
- **No chunking:** Not present.

**Current implemented retrieval:** `python/data_loader.py:1` `load_processed_data()` loads precomputed `data/processed/summary_metrics.json` (14494612 revenue etc.) — file-based, not vector.

**If RAG were added:** Would need embeddings for `data/raw/sales_expense_data.csv` + vector store + tool calling — not in repo.

**Evidence:** `grep -r "embedding\|vector\|rag\|pinecone\|chroma" ai/ python/` returns 0.
