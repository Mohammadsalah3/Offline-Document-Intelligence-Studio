from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.ocr_service import run_ocr, validate_file_extension


router = APIRouter()


@router.post("/")
async def ocr_file(
    file: UploadFile = File(...),
    language: str = Form("eng"),
    preprocessing_steps: str = Form("Grayscale,Resize"),
):
    try:
        validate_file_extension(file.filename)

        steps = [
            step.strip()
            for step in preprocessing_steps.split(",")
            if step.strip()
        ]

        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir) / file.filename

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = run_ocr(
            file_path=str(temp_path),
            filename=file.filename,
            language=language,
            steps=steps,
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
    finally:
        try:
            if "temp_path" in locals() and temp_path.exists():
                temp_path.unlink()
            if "temp_dir" in locals():
                Path(temp_dir).rmdir()
        except Exception:
            pass