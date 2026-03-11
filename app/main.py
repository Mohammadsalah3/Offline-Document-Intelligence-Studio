from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import sys

from app.routers import ocr, llm, summarize, extract, predict, rag

# Detect if running inside PyInstaller
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(_file_))

# Paths for static files and templates
static_path = os.path.join(BASE_DIR, "app", "static")
templates_path = os.path.join(BASE_DIR, "app", "templates")

CLOUD_DEMO_MODE = os.getenv("CLOUD_DEMO_MODE", "false").lower() == "true"

app = FastAPI(
    title="Offline Document Intelligence API",
    description="An offline AI API for OCR, local LLM chat, summarization, extraction, prediction, and RAG.",
    version="1.0.0"
)

# Include routers
app.include_router(ocr.router, prefix="/ocr", tags=["OCR"])
app.include_router(llm.router, prefix="/chat", tags=["LLM"])
app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])
app.include_router(extract.router, prefix="/extract", tags=["Extraction"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])

# Mount static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Templates
templates = Jinja2Templates(directory=templates_path)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cloud_demo_mode": CLOUD_DEMO_MODE
        }
    )