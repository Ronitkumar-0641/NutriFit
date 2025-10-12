"""Utilities to build Supabase-backed retrievers for LangChain."""

from __future__ import annotations

from typing import Iterable, List

import db


def _rows_to_documents(rows: Iterable[dict], source_label: str) -> List[str]:
    docs: List[str] = []
    for row in rows:
        page_content_lines = []
        for key, value in row.items():
            if key in {"id", "user_id", "created_at", "timestamp", "file_path"}:
                continue
            if value is None:
                continue
            page_content_lines.append(f"{key}: {value}")
        if page_content_lines:
            docs.append(f"[{source_label}] " + "\n".join(page_content_lines))
    return docs


def build_context_retriever(user_id: str):
    """Return a simple history list for mock retrieval."""
    chat_rows = db.fetch_chat_history(user_id)
    ocr_rows = db.fetch_ocr_reports(user_id)

    documents = []
    documents.extend(_rows_to_documents(chat_rows, "chat_history"))
    documents.extend(_rows_to_documents(ocr_rows, "ocr_reports"))
    return documents