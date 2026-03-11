from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.summary_service import summarize_text


router = APIRouter()


class SummarizeRequest(BaseModel):
    text: str
    model: str = "llama3.2:latest"


@router.post("/")
def summarize(request: SummarizeRequest):
    try:
        return summarize_text(
            text=request.text,
            model=request.model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")