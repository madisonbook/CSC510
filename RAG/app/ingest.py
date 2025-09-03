import argparse
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

from app.config import CHROMA_DIR, EMBED_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for p in reader.pages:
        try:
            pages.append(p.extract_text() or "")
        except Exception:
            pass
    return "\n".join(pages)

def _load_docs(root: Path) -> List[Tuple[str, str]]:
    out = []
    for p in root.rglob("*"):
        if p.is_file():
            suf = p.suffix.lower()
            if suf in {".txt", ".md"}:
                out.append((str(p), _read_text(p)))
            elif suf == ".pdf":
                out.append((str(p), _read_pdf(p)))
    return out

def _chunk(text: str, size: int, overlap: int) -> List[str]:
    chunks, n, i = [], len(text), 0
    while i < n:
        j = min(i + size, n)
        chunk = text[i:j]
        if chunk.strip():
            chunks.append(chunk)
        if j == n:
            break
        i = max(0, j - overlap)
    return chunks

def main():
    parser = argparse.ArgumentParser(description="Ingest .txt/.md/.pdf into Chroma")
    parser.add_argument("--data", default="./data", help="Folder containing documents")
    parser.add_argument("--collection", default="docs", help="Chroma collection name")
    args = parser.parse_args()

    data_dir = Path(args.data)
    data_dir.mkdir(parents=True, exist_ok=True)

    docs = _load_docs(data_dir)
    if not docs:
        print("No documents found in", data_dir.resolve())
        return

    embedder = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False))
    col = client.get_or_create_collection(args.collection)

    ids, texts, metas = [], [], []
    idx = 0
    for path, content in docs:
        for c in _chunk(content, CHUNK_SIZE, CHUNK_OVERLAP):
            ids.append(f"doc-{idx}")
            texts.append(c)
            metas.append({"source": path})
            idx += 1

    embs = embedder.encode(texts, convert_to_numpy=True).tolist()
    col.upsert(ids=ids, embeddings=embs, documents=texts, metadatas=metas)
    print("Ingested chunks:", len(texts), "| Collection size:", col.count())

if __name__ == "__main__":
    main()
