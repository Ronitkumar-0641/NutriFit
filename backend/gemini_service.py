"""
Gemini AI service utilities.
Safe for Streamlit Cloud (lazy initialization).
"""

import os
import re
from typing import Optional


# -------------------------------
# Gemini client (LAZY, SAFE)
# -------------------------------

def get_gemini_model():
    """
    Lazily configure and return a Gemini model.
    This MUST NOT run at import time.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        return genai.GenerativeModel(
            "gemini-2.0-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            },
        )
    except Exception:
        return None


# -------------------------------
# Public API
# -------------------------------

def get_gemini_response(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the response text.
    Safe if Gemini is unavailable.
    """
    model = get_gemini_model()
    if not model:
        return "AI service is currently unavailable."

    try:
        response = model.generate_content(prompt)
        return response.text or ""
    except Exception:
        return "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."


def extract_json_from_response(text: str) -> str:
    """
    Extract JSON from Gemini response, handling markdown code blocks and formatting.
    """
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        return json_match.group(1)

    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        return json_match.group(0)

    return text
