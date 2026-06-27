"""
Vector Service — owns the C++ HNSW index.
Runs on port 8001. All FastAPI workers talk to this instead of loading the index themselves.

Routes:
  POST /add     — add a vector to the index
  POST /search  — search for top-k nearest vectors
  GET  /health  — liveness check
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../memory_engine/build'))

from memory_engine import MemoryEngine
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

VECTOR_DIM = 1536
MAX_ELEMENTS = 50000
INDEX_PATH = os.path.join(os.path.dirname(__file__), 'memory.index')

app = FastAPI(title="MemoryOS Vector Service")

_engine = MemoryEngine(dim=VECTOR_DIM, max_elements=MAX_ELEMENTS)

@app.on_event("startup")
def load_index():
    if os.path.exists(INDEX_PATH):
        _engine.load_index(INDEX_PATH)
        print(f"✅ Loaded index from {INDEX_PATH}")
    else:
        print("🆕 Starting with empty index")


class AddRequest(BaseModel):
    vector_id: int
    embedding: list[float]

class AddResponse(BaseModel):
    vector_id: int
    status: str

class SearchRequest(BaseModel):
    embedding: list[float]
    top_k: int = 5

class SearchResult(BaseModel):
    id: int
    distance: float

class SearchResponse(BaseModel):
    results: list[SearchResult]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/add", response_model=AddResponse)
def add_vector(req: AddRequest):
    if len(req.embedding) != VECTOR_DIM:
        raise HTTPException(status_code=400, detail=f"Expected {VECTOR_DIM} dims, got {len(req.embedding)}")
    try:
        _engine.add_vector(req.vector_id, req.embedding)
        _engine.save_index(INDEX_PATH)
        return AddResponse(vector_id=req.vector_id, status="added")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
def search_vectors(req: SearchRequest):
    if len(req.embedding) != VECTOR_DIM:
        raise HTTPException(status_code=400, detail=f"Expected {VECTOR_DIM} dims, got {len(req.embedding)}")
    try:
        results = _engine.search(req.embedding, req.top_k)
        return SearchResponse(results=[SearchResult(id=r.id, distance=r.distance) for r in results])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
