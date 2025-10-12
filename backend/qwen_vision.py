"""Helper utilities to analyze medical imagery with Qwen vision models via OpenRouter."""

from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict, Optional

import requests

_OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
_OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL")
_OPENROUTER_SITE_NAME = os.getenv("OPENROUTER_SITE_NAME")

_OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
_MODEL_ID = "qwen/qwen2.5-vl-32b-instruct:free"


class OpenRouterConfigurationError(RuntimeError):
    """Raised when the OpenRouter client is not properly configured."""


def _build_headers() -> Dict[str, str]:
    if not _OPENROUTER_API_KEY:
        raise OpenRouterConfigurationError("OPENROUTER_API_KEY environment variable is not set.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {_OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    if _OPENROUTER_SITE_URL:
        headers["HTTP-Referer"] = _OPENROUTER_SITE_URL
    if _OPENROUTER_SITE_NAME:
        headers["X-Title"] = _OPENROUTER_SITE_NAME
    return headers


def _bytes_to_data_url(image_bytes: bytes, content_type: Optional[str]) -> str:
    if not content_type:
        content_type = "image/png"
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{content_type};base64,{encoded}"


def analyze_image_with_qwen(
    image_bytes: bytes,
    *,
    content_type: Optional[str] = None,
    prompt: str = "Describe this medical image. Highlight key clinical observations."
) -> str:
    """Send an image to Qwen vision model and return the assistant's description."""

    headers = _build_headers()
    image_data_url = _bytes_to_data_url(image_bytes, content_type)

    payload: Dict[str, Any] = {
        "model": _MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        ],
    }

    response = requests.post(_OPENROUTER_ENDPOINT, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    try:
        choice = data["choices"][0]
        message = choice["message"]
        content = message["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected OpenRouter response structure: {data}") from exc

    if isinstance(content, list):
        text_parts = [part.get("text", "") for part in content if isinstance(part, dict)]
        return "".join(text_parts).strip()

    if isinstance(content, str):
        return content.strip()

    # If content is another structure, return its JSON string for debugging.
    return json.dumps(content)