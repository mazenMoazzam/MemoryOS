import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
    return _pool

async def setup_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL DEFAULT 'default',
                session_id TEXT,
                raw_text TEXT NOT NULL,
                vector_id INTEGER NOT NULL,
                source TEXT NOT NULL DEFAULT 'chat',
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL DEFAULT 'default',
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)

async def insert_memory(raw_text: str, vector_id: int, session_id: str = None, user_id: str = "default", source: str = "chat") -> int:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO memories (user_id, session_id, raw_text, vector_id, source)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            user_id, session_id, raw_text, vector_id, source
        )
        return row["id"]

async def fetch_memories_by_ids(vector_ids: list[int]) -> list[str]:
    if not vector_ids:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT raw_text, vector_id FROM memories WHERE vector_id = ANY($1)",
            vector_ids
        )
        id_to_text = {row["vector_id"]: row["raw_text"] for row in rows}
        return [id_to_text[vid] for vid in vector_ids if vid in id_to_text]

async def get_next_vector_id() -> int:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT COUNT(*) as count FROM memories")
        return (row["count"] or 0) + 1
