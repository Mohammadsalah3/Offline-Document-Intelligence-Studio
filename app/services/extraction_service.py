from __future__ import annotations

import json

from app.services.llm_service import generate_chat_response


def extract_information(text: str, model: str = "llama3.2:latest") -> dict:
    prompt = f"""
Extract the following fields from the text below:

- name
- email
- phone
- skills

Return ONLY valid JSON in this format:
{{
  "name": "",
  "email": "",
  "phone": "",
  "skills": []
}}

If a field is missing, return an empty string or empty list.

Text:
{text}
""".strip()

    result = generate_chat_response(message=prompt, model=model)
    raw_output = result["response"]

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        parsed = {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "raw_output": raw_output,
        }

    return {
        "model": model,
        "input_text": text,
        "extracted_data": parsed,
    }