from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.extraction_service import extract_information


router = APIRouter()


class ExtractRequest(BaseModel):
    text: str
    model: str = "llama3.2:latest"


@router.post("/")
def extract(request: ExtractRequest):
    try:
        return extract_information(
            text=request.text,
            model=request.model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")