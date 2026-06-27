import os
import httpx
from services.embedding import embed_text
from db.postgres import insert_memory, fetch_memories_by_ids, get_next_vector_id

VECTOR_SERVICE_URL = os.getenv("VECTOR_SERVICE_URL", "http://localhost:8001")


async def store_memory(text: str, session_id: str = None, user_id: str = "default") -> int:
    vector = await embed_text(text)
    vector_id = await get_next_vector_id()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{VECTOR_SERVICE_URL}/add",
            json={"vector_id": vector_id, "embedding": vector},
            timeout=10.0
        )
        resp.raise_for_status()

    row_id = await insert_memory(
        raw_text=text,
        vector_id=vector_id,
        session_id=session_id,
        user_id=user_id
    )

    return row_id


async def retrieve_memories(query: str, top_k: int = 5) -> list[str]:
    vector = await embed_text(query)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{VECTOR_SERVICE_URL}/search",
            json={"embedding": vector, "top_k": top_k},
            timeout=10.0
        )
        resp.raise_for_status()

    data = resp.json()
    vector_ids = [r["id"] for r in data["results"]]
    texts = await fetch_memories_by_ids(vector_ids)

    return texts
