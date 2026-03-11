from __future__ import annotations

from pathlib import Path
from typing import List
import json
import shutil
import tempfile

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.ocr_service import run_ocr


DOCUMENTS_DIR = Path("app/data/documents")
INDEX_DIR = Path("app/data/index")
CHUNKS_FILE = INDEX_DIR / "chunks.json"
VECTORIZER_FILE = INDEX_DIR / "vectorizer.pkl"
MATRIX_FILE = INDEX_DIR / "matrix.pkl"


def ensure_directories() -> None:
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)


def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end

    return chunks


def save_uploaded_document(file_path: str, filename: str) -> Path:
    ensure_directories()
    destination = DOCUMENTS_DIR / filename
    shutil.copy(file_path, destination)
    return destination


def extract_document_text(file_path: str, filename: str) -> str:
    suffix = Path(filename).suffix.lower()

    if suffix in [".txt"]:
        return Path(file_path).read_text(encoding="utf-8")

    if suffix in [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".webp"]:
        result = run_ocr(
            file_path=file_path,
            filename=filename,
            language="eng",
            steps=["Grayscale", "Resize"]
        )
        return result["extracted_text"]

    raise ValueError("Unsupported file type for RAG upload.")


def rebuild_index() -> dict:
    ensure_directories()

    all_chunks = []

    for file_path in DOCUMENTS_DIR.iterdir():
        if not file_path.is_file():
            continue

        try:
            text = extract_document_text(str(file_path), file_path.name)
            chunks = chunk_text(text)

            for chunk in chunks:
                all_chunks.append(
                    {
                        "source": file_path.name,
                        "text": chunk,
                    }
                )
        except Exception:
            continue

    if not all_chunks:
        with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        return {"documents_indexed": 0, "chunks_indexed": 0}

    texts = [item["text"] for item in all_chunks]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)

    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    joblib.dump(vectorizer, VECTORIZER_FILE)
    joblib.dump(matrix, MATRIX_FILE)

    return {
        "documents_indexed": len(list(DOCUMENTS_DIR.iterdir())),
        "chunks_indexed": len(all_chunks),
    }


def load_index():
    ensure_directories()

    if not CHUNKS_FILE.exists() or not VECTORIZER_FILE.exists() or not MATRIX_FILE.exists():
        raise FileNotFoundError("RAG index not found. Please upload and index documents first.")

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    vectorizer = joblib.load(VECTORIZER_FILE)
    matrix = joblib.load(MATRIX_FILE)

    return chunks, vectorizer, matrix


def retrieve_chunks(question: str, top_k: int = 3) -> dict:
    chunks, vectorizer, matrix = load_index()

    if not chunks:
        return {"question": question, "top_chunks": []}

    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, matrix).flatten()
    ranked_indices = similarities.argsort()[::-1][:top_k]

    top_chunks = [
        {
            "source": chunks[idx]["source"],
            "text": chunks[idx]["text"],
            "score": float(similarities[idx]),
        }
        for idx in ranked_indices
    ]

    return {
        "question": question,
        "top_chunks": top_chunks,
    }