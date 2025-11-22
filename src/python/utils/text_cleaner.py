# utils/text_cleaner.py
import re
from typing import List

def clean_text(text: str) -> str:
    """
    Basic cleaning: normalize whitespace, remove non-printables, fix dashes, remove
    weird unicode, reduce multiple newlines to single.
    """
    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\u2013|\u2014", "-", text)  # en/em dash
    # Remove non-printable characters
    text = "".join([ch for ch in text if ord(ch) >= 9 and ord(ch) <= 55295])
    # Collapse many newlines
    text = re.sub(r"\n\s+\n", "\n\n", text)
    # Remove excessive spaces
    text = re.sub(r"[ \t]{2,}", " ", text)
    # Strip
    return text.strip()

def extract_paragraphs(text: str) -> List[str]:
    """
    Splits text into paragraphs (heuristic): by double newlines or long lines.
    """
    if not text:
        return []
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paras
