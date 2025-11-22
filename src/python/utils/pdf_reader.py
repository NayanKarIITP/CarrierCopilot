# utils/pdf_reader.py
import io
from typing import List
from pdfminer.high_level import extract_text
from pathlib import Path

def read_pdf_text(path: str) -> str:
    """
    Read text from PDF file. Returns plain text.
    If path is not a PDF, tries to read raw text.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # for PDF use pdfminer
    if p.suffix.lower() == ".pdf":
        text = extract_text(path)
        return text or ""
    else:
        # fallback: read as binary/text
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            # fallback: return empty
            return ""
