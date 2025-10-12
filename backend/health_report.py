"""Health report pipeline: OCR extraction, lab metric parsing, and Gemini summarization."""

from __future__ import annotations

import asyncio
import io
import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


from .ocr_helper import extract_text_from_image_bytes

logger = logging.getLogger(__name__)

PARSER_PATTERNS: Dict[str, re.Pattern[str]] = {
    "hemoglobin": re.compile(r"hemoglobin\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "blood_sugar": re.compile(r"(?:fasting\s*)?(?:blood\s*)?(?:glucose|sugar)\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "cholesterol": re.compile(r"cholesterol\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "hdl": re.compile(r"hdl\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "ldl": re.compile(r"ldl\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "triglycerides": re.compile(r"triglycerides\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "vitamin_d": re.compile(r"vitamin\s*d\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "platelet_count": re.compile(r"platelet\s*count\s*[:\-]?\s*(?P<value>\d+(?:\.\d+)?)", re.IGNORECASE),
    "bp_systolic": re.compile(r"(bp|blood\s*pressure)\s*[:\-]?\s*(?P<value>\d{2,3})\s*/", re.IGNORECASE),
    "bp_diastolic": re.compile(r"(bp|blood\s*pressure)\s*[:\-]?\s*\d{2,3}\s*/\s*(?P<value>\d{2,3})", re.IGNORECASE),
}


@dataclass
class ParsedMetric:
    name: str
    value: float
    unit: Optional[str] = None


@dataclass
class ParsedReport:
    raw_text: str
    metrics: List[ParsedMetric] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


async def read_file_bytes(file: Any) -> bytes:
    """Read bytes from an UploadFile-like object or raw bytes."""
    if isinstance(file, bytes):
        return file
    if hasattr(file, "read"):
        data = file.read()
        if asyncio.iscoroutine(data):
            data = await data
        return data
    raise TypeError("Unsupported file type for OCR processing")


async def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Simple PDF OCR pipeline using Pillow for the first page only."""
    try:
        from pdf2image import convert_from_bytes
    except Exception:
        logger.warning("pdf2image not installed; skipping PDF OCR")
        return ""

    images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
    if not images:
        return ""

    buf = io.BytesIO()
    images[0].save(buf, format="PNG")
    return await extract_text_from_image_bytes(buf.getvalue())


async def ocr_extract_text(file_bytes: bytes, filename: Optional[str]) -> str:
    """Extract text from bytes, using PDF parsing if necessary."""
    if filename and filename.lower().endswith(".pdf"):
        return await extract_text_from_pdf_bytes(file_bytes)
    return await extract_text_from_image_bytes(file_bytes)


def _match_metric(name: str, text: str) -> Optional[ParsedMetric]:
    pattern = PARSER_PATTERNS.get(name)
    if not pattern:
        return None
    match = pattern.search(text)
    if not match:
        return None
    try:
        value = float(match.group("value"))
    except (ValueError, TypeError, KeyError):
        return None
    unit = None
    metric = ParsedMetric(name=name, value=value, unit=unit)
    return metric


def parse_lab_values(text: str) -> List[ParsedMetric]:
    """Run regex parsers across the extracted text."""
    metrics: List[ParsedMetric] = []
    lower_text = text.lower()
    for name in PARSER_PATTERNS:
        metric = _match_metric(name, lower_text)
        if metric:
            metrics.append(metric)
    return metrics


def metrics_to_json(metrics: Iterable[ParsedMetric]) -> str:
    """Serialize parsed metrics for the LLM."""
    return json.dumps(
        [
            {"name": metric.name, "value": metric.value, "unit": metric.unit}
            for metric in metrics
        ]
    )


SUMMARY_PROMPT = """You are a compassionate medical assistant generating structured health summaries.
Given raw OCR text from a lab or medical report and structured metrics in JSON,
produce a JSON object with the following keys:
- overview: High-level interpretation in plain language for patients.
- metrics: For each metric present, provide status (normal/high/low) and any context.
- recommendations: Actionable suggestions or questions to ask a doctor.
- warnings: List safety flags that require medical follow-up.

The response must be valid JSON and avoid additional commentary."""


def summarize_health_report(raw_text: str, metrics: List[ParsedMetric]) -> Dict[str, Any]:
    """Return a rule-based summary instead of calling external LLM services."""
    overview = (
        "The uploaded report has been reviewed with built-in heuristics. "
        "Key metrics are highlighted below. For medical decisions, consult a licensed professional."
    )
    metrics_summary = []
    for metric in metrics:
        status = "normal"
        if metric.name in {"blood_sugar", "cholesterol", "ldl", "bp_systolic", "bp_diastolic"}:
            status = "monitor"
        metrics_summary.append({"name": metric.name, "value": metric.value, "status": status})

    return {
        "overview": overview,
        "metrics": metrics_summary,
        "recommendations": [
            "Maintain a balanced diet rich in vegetables, lean proteins, and whole grains.",
            "Stay active with at least 150 minutes of moderate exercise weekly.",
            "Schedule follow-ups with healthcare providers for personalized advice.",
        ],
        "warnings": [
            "This summary is heuristic only; abnormalities should be reviewed by a medical professional."
        ],
    }


async def process_health_document(file: Any, filename: Optional[str] = None) -> ParsedReport:
    """End-to-end processing pipeline."""
    file_bytes = await read_file_bytes(file)
    raw_text = await ocr_extract_text(file_bytes, filename)
    metrics = parse_lab_values(raw_text)
    summary = summarize_health_report(raw_text, metrics)
    return ParsedReport(raw_text=raw_text, metrics=metrics, summary=summary)


async def process_health_document_sync(file: Any, filename: Optional[str] = None) -> ParsedReport:
    """Synchronous-style wrapper retaining async signature for compatibility."""
    return await process_health_document(file, filename)