from fastapi import FastAPI
from pydantic import BaseModel
from chains.router_chain import router_chain
import logging
import uuid

from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse

load_dotenv()
CLIENT_PRODUCTION_URL = os.getenv("CLIENT_PRODUCTION_URL")
CLIENT_DEVELOPMENT_URL = os.getenv("CLIENT_DEVELOPMENT_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_PRODUCTION_URL, CLIENT_DEVELOPMENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_histories = {}

class UserQuery(BaseModel):
    query: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.post("/chat")
async def chat(query: UserQuery):
    session_id = query.session_id or str(uuid.uuid4())
    previous_messages = session_histories.get(session_id, [])

    input_with_memory = {
        "input": query.query,
        "history": previous_messages
    }

    config = {"configurable": {"session_id": session_id}}

    async def stream_response():
        try:
            async for chunk in router_chain.astream(input_with_memory, config=config):
                yield str(chunk)
        except Exception as e:
            yield f"[Error: {e}]"

    return StreamingResponse(stream_response(), media_type="text/plain")


@app.get("/")
async def root():
    return {"message": "Personal Chatbot API is running!"}

