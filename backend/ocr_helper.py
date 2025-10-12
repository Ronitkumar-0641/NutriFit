import asyncio
from typing import Optional
import io
from PIL import Image


async def extract_text_from_image_bytes(image_bytes: bytes) -> str:
    """Attempt to extract text from image bytes using pytesseract, falling back to easyocr if unavailable.
    Returns extracted text (possibly empty).
    """
    try:
        import pytesseract

        img = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(img)
        return text
    except Exception:
        # Fallback to easyocr if installed
        try:
            import easyocr

            reader = easyocr.Reader(["en"])
            img = Image.open(io.BytesIO(image_bytes))
            res = reader.readtext(img)
            return "\n".join([r[1] for r in res])
        except Exception:
            return ""
