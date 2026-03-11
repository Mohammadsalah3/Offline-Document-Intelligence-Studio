from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import generate_chat_response


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    model: str = "llama3.2:latest"


@router.post("/")
def chat(request: ChatRequest):
    try:
        return generate_chat_response(
            message=request.message,
            model=request.model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM request failed: {str(e)}")