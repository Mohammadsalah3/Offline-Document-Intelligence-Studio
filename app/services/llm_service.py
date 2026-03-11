from __future__ import annotations

import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
DEFAULT_MODEL = "llama3.2:latest"


def generate_chat_response(message: str, model: str = DEFAULT_MODEL) -> dict:
    payload = {
        "model": model,
        "prompt": message,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()

    return {
        "model": model,
        "message": message,
        "response": data.get("response", "").strip(),
    }