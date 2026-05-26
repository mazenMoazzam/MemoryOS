from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from db.postgres import setup_db
from routes.chat import router as chat_router

load_dotenv()

app = FastAPI(title="MemoryOS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await setup_db()

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
