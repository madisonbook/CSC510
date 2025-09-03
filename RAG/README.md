# Minimal RAG (GitHub Codespaces Friendly)

**What this gives you**
- Local ChromaDB vector store (`.chroma/`)
- Sentence-Transformers embeddings (`all-MiniLM-L6-v2`)
- Ingest `.txt`, `.md`, `.pdf`
- Query via CLI or FastAPI
- Optional OpenAI answer generation (otherwise returns retrieved context)

## Quick Start (in Codespaces)
1. Open this repo in **GitHub Codespaces**.
2. (Optional) `cp .env.example .env` and add your `OPENAI_API_KEY`.
3. Put documents into `rag/data/` (or `data/` if you use the folder as repo root).
4. Ingest:
   ```bash
   python -m app.ingest --data ./data
   ```
5. Ask a question:
   ```bash
   python -m app.query "What does this doc say about X?"
   ```
6. Run API:
   ```bash
   uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
   # GET  http://localhost:8000/health
   # POST http://localhost:8000/query  {"q":"your question"}
   ```
