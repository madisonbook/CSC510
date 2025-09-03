from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.query import retrieve, answer
from app.config import TOP_K

app = FastAPI()

class QueryIn(BaseModel):
    q: str
    k: int | None = None

class QueryOut(BaseModel):
    answer: str
    sources: List[str]

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/query", response_model=QueryOut)
def query(qin: QueryIn):
    k = qin.k or TOP_K
    results = retrieve(qin.q, k=k)
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    ans = answer(qin.q)
    srcs = [m.get("source","") for m in metas]
    return {"answer": ans, "sources": srcs}
