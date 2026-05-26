from fastapi import APIRouter
from pydantic import BaseModel
from services.memory import store_memory, retrieve_memories
from services.llm import chat_with_memory

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    memories_used: list[str]

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    memories = await retrieve_memories(req.message)

    response = await chat_with_memory(req.message, memories)

    await store_memory(req.message, session_id=req.session_id, user_id=req.user_id)

    return ChatResponse(response=response, memories_used=memories)
