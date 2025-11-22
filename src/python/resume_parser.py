# resume_parser.py
import os
from typing import Dict, Any
from utils.pdf_reader import read_pdf_text
from utils.text_cleaner import clean_text, extract_paragraphs
from llm_engine import parse_with_llm
import json

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------

EXTRACTION_PROMPT = """
You are an advanced resume parser. Extract the following JSON from the resume text:
- full_name (if present)
- emails (list)
- phones (list)
- skills (list of single-word or short phrases)
- education (list of degree+school)
- experience (list of {title, company, start, end, bullets})
- projects (list of project short descriptions)

Return only valid JSON, no explanation.
Resume text:
"""

ANALYZE_PROMPT = """
Given the user's extracted fields (skills, experience, education), rate their resume from 0-100 and provide:
- resume_score: integer
- high_level_feedback: list of short suggestions
Return JSON only.
"""

# ---------------------------------------------------------
# FILE PARSER
# ---------------------------------------------------------

def parse_resume_from_file(path: str) -> Dict[str, Any]:
    raw = read_pdf_text(path)
    cleaned = clean_text(raw)

    prompt = EXTRACTION_PROMPT + cleaned[:4500]

    # 💡 Call LLM to extract JSON
    try:
        result_text = parse_with_llm(prompt)
    except Exception:
        result_text = '{"skills": [], "education": [], "experience": [], "full_name": null, "emails": [], "phones": [], "projects": []}'

    # Parse JSON safely
    try:
        parsed = json.loads(result_text)
    except:
        parsed = _fallback_parse(cleaned)

    # Analyze resume quality
    analysis = _analyze_resume(parsed)

    return {
        "parsed": parsed,
        "analysis": analysis,
        "raw_text_preview": cleaned[:2000]
    }

# ---------------------------------------------------------
# TEXT-ONLY PARSER (Required by FastAPI)
# ---------------------------------------------------------

def parse_resume_text(text: str) -> Dict[str, Any]:
    cleaned = clean_text(text)

    prompt = EXTRACTION_PROMPT + cleaned[:4500]

    # LLM extraction
    try:
        result_text = parse_with_llm(prompt)
    except:
        result_text = '{"skills": [], "education": [], "experience": [], "full_name": null, "emails": [], "phones": [], "projects": []}'

    # JSON parse
    try:
        parsed = json.loads(result_text)
    except:
        parsed = _fallback_parse(cleaned)

    # Quality analysis
    analysis = _analyze_resume(parsed)

    # SAFETY: ensure skills always exists
    skills = parsed.get("skills", [])

    return {
        "skills": skills,                 
        "parsed": parsed,
        "analysis": analysis,
        "raw_text_preview": cleaned[:2000]
    }


# ---------------------------------------------------------
# FALLBACK LOGIC (Used when LLM fails)
# ---------------------------------------------------------

def _fallback_parse(cleaned_text: str):
    paragraphs = extract_paragraphs(cleaned_text)

    skills_hint = []
    for p in paragraphs:
        if "skills" in p.lower() and len(p) < 300:
            skills_hint = [
                s.strip() for s in p.split(":")[-1].split(",") if s.strip()
            ]
            break

    return {
        "raw_text": cleaned_text,
        "skills": skills_hint,
        "education": [],
        "experience": [],
        "projects": [],
        "emails": [],
        "phones": []
    }
# ---------------------------------------------------------
# ANALYSIS LOGIC
# ---------------------------------------------------------

def _analyze_resume(parsed):
    try:
        analysis = parse_with_llm(ANALYZE_PROMPT + str(parsed))
        return json.loads(analysis)
    except:
        return {"resume_score": None, "high_level_feedback": []}

# ✔ REQUIRED EXPORT ALIAS (IMPORTANT)
parse_resume_file = parse_resume_from_file

# ---------------------------------------------------------
# CLI TESTING
# ---------------------------------------------------------

if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    out = parse_resume_from_file(path)
    print(json.dumps(out, indent=2))
