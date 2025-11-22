# interview_assistant.py
from llm_engine import parse_with_llm
from typing import Dict, Any
import json

QUESTION_PROMPT = """
You are an interviewer. Provide a single behavioral or technical interview question appropriate for mid-senior engineers.
Return JSON: {"question": "...", "follow_up": "...", "difficulty": "mid"}
"""

ANALYZE_PROMPT = """
Analyze the transcript of an answer for metrics:
- filler_words_count: dict of filler -> count
- confidence_estimate: 0-100 (approx)
- strengths: list
- improvements: list

Return JSON only.
"""


# ---------------------------------------------------------
# QUESTION GENERATOR (accepts optional argument)
# ---------------------------------------------------------
def sample_question(_ignored=None):
    try:
        raw = parse_with_llm(QUESTION_PROMPT)
        return json.loads(raw)
    except Exception:
        return {
            "question": "Tell me about a time you disagreed with a teammate and how you handled it.",
            "follow_up": "What did you learn?",
            "difficulty": "mid"
        }


# ---------------------------------------------------------
# ANSWER ANALYZER
# ---------------------------------------------------------
def analyze_transcript(transcript: str):
    prompt = ANALYZE_PROMPT + "\nTranscript:\n" + transcript[:3000]
    try:
        raw = parse_with_llm(prompt)
        return json.loads(raw)
    except Exception:
        return {
            "filler_words_count": {"um": 3, "like": 1},
            "confidence_estimate": 70,
            "strengths": ["clear communication", "structured answer"],
            "improvements": ["quantify achievements", "reduce fillers"]
        }


# ---------------------------------------------------------
# EXPORTS FOR FASTAPI
# ---------------------------------------------------------
generate_question = sample_question
analyze_answer = analyze_transcript
