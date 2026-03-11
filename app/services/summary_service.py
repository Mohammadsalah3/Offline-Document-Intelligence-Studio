from __future__ import annotations

from app.services.llm_service import generate_chat_response


def summarize_text(text: str, model: str = "llama3.2:latest") -> dict:
    prompt = f"""
Summarize the following text clearly and concisely.

Text:
{text}

Return only the summary.
""".strip()

    result = generate_chat_response(message=prompt, model=model)

    return {
        "model": model,
        "original_text": text,
        "summary": result["response"],
    }