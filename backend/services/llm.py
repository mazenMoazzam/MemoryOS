import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def chat_with_memory(user_message: str, memories: list[str]) -> str:
    memory_block = "\n".join(f"- {m}" for m in memories) if memories else "No relevant memories found."

    system_prompt = f"""You are a helpful AI assistant with persistent memory.
You remember things the user has told you across past conversations.

Relevant memories from past conversations:
{memory_block}

Use these memories to give more relevant, personalized responses.
If a memory is directly relevant, use it. If not, just answer normally."""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content
