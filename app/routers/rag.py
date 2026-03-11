from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.rag_service import (
    save_uploaded_document,
    rebuild_index,
    retrieve_chunks,
)
from app.services.llm_service import generate_chat_response


router = APIRouter()


class RetrievalRequest(BaseModel):
    question: str
    top_k: int = 3


class AskRequest(BaseModel):
    question: str
    top_k: int = 3
    model: str = "llama3.2:latest"


@router.post("/upload")
async def rag_upload(file: UploadFile = File(...)):
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir) / file.filename

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        save_uploaded_document(str(temp_path), file.filename)
        stats = rebuild_index()

        return {
            "message": "Document uploaded and indexed successfully.",
            "filename": file.filename,
            "index_stats": stats,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG upload failed: {str(e)}")
    finally:
        try:
            if temp_path.exists():
                temp_path.unlink()
            Path(temp_dir).rmdir()
        except Exception:
            pass


@router.post("/retrieve")
def rag_retrieve(request: RetrievalRequest):
    try:
        return retrieve_chunks(
            question=request.question,
            top_k=request.top_k,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG retrieval failed: {str(e)}")


@router.post("/ask")
def rag_ask(request: AskRequest):
    try:
        retrieval_result = retrieve_chunks(
            question=request.question,
            top_k=request.top_k,
        )

        context_blocks = [
            f"[Source: {item['source']}]\n{item['text']}"
            for item in retrieval_result["top_chunks"]
        ]
        context = "\n\n".join(context_blocks)

        prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say: "I could not find the answer in the provided documents."

Context:
{context}

Question:
{request.question}
""".strip()

        llm_result = generate_chat_response(
            message=prompt,
            model=request.model,
        )

        return {
            "question": request.question,
            "answer": llm_result["response"],
            "retrieved_chunks": retrieval_result["top_chunks"],
            "model": request.model,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG QA failed: {str(e)}")