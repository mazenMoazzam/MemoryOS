import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../memory_engine/build'))

from memory_engine import MemoryEngine
from services.embedding import embed_text
from db.postgres import insert_memory, fetch_memories_by_ids, get_next_vector_id

VECTOR_DIM = 1536
MAX_ELEMENTS = 10000
INDEX_PATH = os.path.join(os.path.dirname(__file__), '../memory.index')

_engine = None

def get_engine() -> MemoryEngine:
    global _engine
    if _engine is None:
        _engine = MemoryEngine(dim=VECTOR_DIM, max_elements=MAX_ELEMENTS)
        if os.path.exists(INDEX_PATH):
            _engine.load_index(INDEX_PATH)
    return _engine

async def store_memory(text: str, session_id: str = None, user_id: str = "default") -> int:
    vector = await embed_text(text)
    vector_id = await get_next_vector_id()

    engine = get_engine()
    engine.add_vector(vector_id, vector)
    engine.save_index(INDEX_PATH)

    row_id = await insert_memory(
        raw_text=text,
        vector_id=vector_id,
        session_id=session_id,
        user_id=user_id
    )

    return row_id

async def retrieve_memories(query: str, top_k: int = 5) -> list[str]:
    vector = await embed_text(query)

    engine = get_engine()
    results = engine.search(vector, top_k)

    vector_ids = [r.id for r in results]
    texts = await fetch_memories_by_ids(vector_ids)

    return texts
