import os
import sys
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../backend/.env'))

from openai import AsyncOpenAI
from db.postgres import setup_db, insert_memory, get_next_vector_id
from services.embedding import embed_text
from services.memory import get_engine

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def summarize_file(relative_path: str, content: str) -> str:
    """Ask GPT to summarize what a file does in 2-3 sentences."""
    prompt = f"""Summarize what this file does in 2-3 sentences. Be specific and technical.
Focus on: what it contains, what technologies it uses, what its purpose is.

File: {relative_path}

Content:
{content[:3000]}
"""
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    summary = response.choices[0].message.content.strip()
    return f"[FILE: {relative_path}] {summary}"


async def index_file(file: dict, user_id: str = "default") -> str:
    """Summarize a file and store it as a memory."""
    memory_text = await summarize_file(file['relative_path'], file['content'])

    vector = await embed_text(memory_text)
    vector_id = await get_next_vector_id()

    engine = get_engine()
    engine.add_vector(vector_id, vector)

    index_path = os.path.join(os.path.dirname(__file__), '../backend/memory.index')
    engine.save_index(index_path)

    await insert_memory(
        raw_text=memory_text,
        vector_id=vector_id,
        session_id="mcp_index",
        user_id=user_id,
        source="mcp_file"
    )

    return memory_text
