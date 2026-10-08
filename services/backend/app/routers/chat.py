from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from connections.connector_ollama import call_agent, messages, tools, functions

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def stream_chat(request: ChatRequest):
    messages.append({"role": "user", "content": request.message})
    return StreamingResponse(call_agent(messages, tools, functions), media_type="text/event-stream")