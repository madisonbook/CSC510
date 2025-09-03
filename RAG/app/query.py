import sys
from typing import List, Dict, Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from app.config import CHROMA_DIR, EMBED_MODEL, TOP_K, OPENAI_API_KEY

def retrieve(q: str, k: int = TOP_K) -> Dict[str, Any]:
    client = chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False))
    col = client.get_or_create_collection("docs")
    embedder = SentenceTransformer(EMBED_MODEL)
    q_emb = embedder.encode([q], convert_to_numpy=True).tolist()
    return col.query(query_embeddings=q_emb, n_results=k, include=["documents", "metadatas", "distances"])

def _generate_with_openai(question: str, contexts: List[str]) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    system = "Answer ONLY using the provided chunks. If unknown, say you don't know."
    ctx = "\n\n".join(f"- {c}" for c in contexts)
    prompt = f"Context:\n{ctx}\n\nQuestion: {question}\nAnswer:"
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content

def answer(question: str) -> str:
    results = retrieve(question, k=TOP_K)
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    contexts = list(docs)[:TOP_K]
    if not OPENAI_API_KEY:
        header = "[No OPENAI_API_KEY] Top retrieved chunks:\n\n"
        body = "\n\n---\n\n".join(contexts)
        srcs = "\n".join(f"- {m.get('source','')}" for m in metas[:TOP_K])
        return header + body + "\n\nSources:\n" + srcs
    return _generate_with_openai(question, contexts)

def main():
    if len(sys.argv) < 2:
        print('Usage: python -m app.query "your question"')
        sys.exit(1)
    print(answer(sys.argv[1]))

if __name__ == "__main__":
    main()
