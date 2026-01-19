# src/python/interview_assistant.py
import json
import re
import os
import sys
import random
import logging

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# 🔧 ROBUST IMPORT (Finds llm_engine anywhere)
# ---------------------------------------------------------
try:
    # Try direct import (works if running inside src/python)
    from llm_engine import parse_with_llm
except ImportError:
    try:
        # Try package import (works if running from root via uvicorn)
        from src.python.llm_engine import parse_with_llm
    except ImportError:
        logger.warning("⚠️ llm_engine not found. Using MOCK mode.")
        def parse_with_llm(prompt, model_name=None): return "{}"

# ---------------------------------------------------------
# 🧠 PROMPTS
# ---------------------------------------------------------

QUESTION_PROMPT_TEMPLATE = """
You are an expert Technical Interviewer for a FAANG company.
Generate ONE behavioral or technical interview question for a {level} {role} position.

CONTEXT:
- Difficulty: {level_desc}
- Previous Questions (DO NOT REPEAT): {history_str}

OUTPUT FORMAT (Strict JSON, No Markdown):
{{
    "question": "The question text here",
    "follow_up": "A probing follow-up question",
    "difficulty": "{level}"
}}
"""

ANALYZE_PROMPT = """
You are an expert Interview Coach. Analyze this candidate's answer.

TRANSCRIPT: "{transcript}"
QUESTION CONTEXT: "{question}"

OUTPUT FORMAT (Strict JSON, No Markdown):
{{
    "filler_words_count": {{ "um": 0, "like": 0, "basically": 0 }},
    "confidence_estimate": 85,
    "strengths": ["Strength 1", "Strength 2"],
    "improvements": ["Improvement 1", "Improvement 2"],
    "clarity_score": 80
}}
"""

# ---------------------------------------------------------
# 🛡️ FALLBACK TEMPLATES
# ---------------------------------------------------------
FALLBACK_TEMPLATES = [
    {
        "question": "Describe a challenging project you worked on as a {role}.",
        "follow_up": "What specific technical trade-offs did you have to make?",
        "difficulty": "Mid-Level"
    },
    {
        "question": "How do you stay updated with the latest trends in {role}?",
        "follow_up": "Can you give an example of a new technology you recently applied?",
        "difficulty": "Junior"
    },
    {
        "question": "Tell me about a time you had a conflict with a team member.",
        "follow_up": "How did you resolve it and what was the outcome?",
        "difficulty": "Behavioral"
    }
]

# ---------------------------------------------------------
# 🛠️ HELPER: CLEAN JSON
# ---------------------------------------------------------
def clean_json_output(text: str) -> str:
    if not text: return "{}"
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text)
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return text[start : end + 1]
    return text.strip()

# ---------------------------------------------------------
# 1. GENERATE QUESTION
# ---------------------------------------------------------
def generate_question(role="Software Engineer", level="Mid-Level", history=None):
    if history is None:
        history = []

    level_desc = "Focus on fundamentals."
    if "Senior" in level: level_desc = "Focus on system design and leadership."
    if "Junior" in level: level_desc = "Focus on core concepts and learning."

    history_str = ", ".join([h.get('text', '') for h in history]) if history else "None"

    try:
        prompt = QUESTION_PROMPT_TEMPLATE.format(
            role=role, 
            level=level, 
            level_desc=level_desc,
            history_str=history_str
        )
        
        # Uses the new llm_engine
        raw_response = parse_with_llm(prompt)
        cleaned_json = clean_json_output(raw_response)
        
        if not cleaned_json or cleaned_json == "{}": 
            raise Exception("Empty AI response received.")

        data = json.loads(cleaned_json)
        
        return {
            "question": data.get("question", f"Tell me about your experience as a {role}."),
            "follow_up": data.get("follow_up", "Can you elaborate on that?"),
            "difficulty": level
        }

    except Exception as e:
        logger.error(f"⚠️ Question Generation Failed: {e}")
        
        # Fallback
        template = random.choice(FALLBACK_TEMPLATES)
        return {
            "question": template["question"].format(role=role),
            "follow_up": template["follow_up"],
            "difficulty": level
        }

# ---------------------------------------------------------
# 2. ANALYZE ANSWER
# ---------------------------------------------------------
def analyze_answer(transcript: str, question_context: str = "General Interview"):
    if not transcript or len(transcript) < 5:
        return {
            "strengths": ["N/A"], "improvements": ["Answer too short"],
            "confidence_estimate": 0, "clarity_score": 0, "filler_words_count": {}
        }

    try:
        prompt = ANALYZE_PROMPT.format(transcript=transcript, question=question_context)
        
        raw_response = parse_with_llm(prompt)
        cleaned_json = clean_json_output(raw_response)
        
        if not cleaned_json or cleaned_json == "{}": 
            raise Exception("Empty AI response received.")

        result = json.loads(cleaned_json)
        
        # Ensure default keys exist
        if "clarity_score" not in result: result["clarity_score"] = 70
        if "confidence_estimate" not in result: result["confidence_estimate"] = 75
        if "filler_words_count" not in result: result["filler_words_count"] = {}
        
        return result

    except Exception as e:
        logger.error(f"⚠️ Analysis Failed: {e}")
        return {
            "filler_words_count": {}, 
            "confidence_estimate": 70,
            "strengths": ["Good effort", "Clear communication"], 
            "improvements": ["Add more technical details", "Structure your answer better"], 
            "clarity_score": 70
        }

# ---------------------------------------------------------
# ✅ MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    print(json.dumps(generate_question("DevOps", "Senior"), indent=2))





# #last working version
# #interview_assistant.py
# import json
# import re
# import os
# import sys
# import random

# # ---------------------------------------------------------
# # 🔧 SETUP PATHS & IMPORTS
# # ---------------------------------------------------------
# current_dir = os.path.dirname(os.path.abspath(__file__))
# if current_dir not in sys.path:
#     sys.path.append(current_dir)

# try:
#     from llm_engine import parse_with_llm
# except ImportError:
#     print("⚠️ Warning: llm_engine not found. Using mock mode.")
#     def parse_with_llm(prompt, model_name=None): return "{}"

# # ---------------------------------------------------------
# # 🧠 DYNAMIC PROMPTS
# # ---------------------------------------------------------

# QUESTION_PROMPT_TEMPLATE = """
# You are an expert Technical Interviewer for a FAANG company.
# Generate ONE behavioral or technical interview question for a {level} {role} position.

# CONTEXT:
# - Difficulty: {level_desc}
# - Previous Questions (DO NOT REPEAT): {history_str}

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "question": "The question text here",
#     "follow_up": "A probing follow-up question",
#     "difficulty": "{level}"
# }}
# """

# ANALYZE_PROMPT = """
# You are an expert Interview Coach. Analyze this candidate's answer.

# TRANSCRIPT: "{transcript}"
# QUESTION CONTEXT: "{question}"

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "filler_words_count": {{ "um": 0, "like": 0, "basically": 0 }},
#     "confidence_estimate": 85,
#     "strengths": ["Strength 1", "Strength 2"],
#     "improvements": ["Improvement 1", "Improvement 2"],
#     "clarity_score": 80
# }}
# """

# # ---------------------------------------------------------
# # 🛡️ FALLBACK TEMPLATES (Backup Questions)
# # ---------------------------------------------------------
# FALLBACK_TEMPLATES = [
#     {
#         "question": "Describe a challenging project you worked on as a {role}.",
#         "follow_up": "What specific technical trade-offs did you have to make?",
#         "difficulty": "Mid-Level"
#     },
#     {
#         "question": "How do you stay updated with the latest trends in {role}?",
#         "follow_up": "Can you give an example of a new technology you recently applied?",
#         "difficulty": "Junior"
#     },
#     {
#         "question": "Tell me about a time you had a conflict with a team member.",
#         "follow_up": "How did you resolve it and what was the outcome?",
#         "difficulty": "Behavioral"
#     }
# ]

# # ---------------------------------------------------------
# # 🛠️ HELPER: CLEAN JSON
# # ---------------------------------------------------------
# def clean_json_output(text: str) -> str:
#     if not text: return "{}"
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
#     start = text.find('{')
#     end = text.rfind('}')
#     if start != -1 and end != -1:
#         return text[start : end + 1]
#     return text.strip()

# # ---------------------------------------------------------
# # 1. GENERATE QUESTION
# # ---------------------------------------------------------
# def generate_question(role="Software Engineer", level="Mid-Level", history=None):
#     if history is None:
#         history = []

#     level_desc = "Focus on fundamentals."
#     if "Senior" in level: level_desc = "Focus on system design and leadership."
#     if "Junior" in level: level_desc = "Focus on core concepts and learning."

#     history_str = ", ".join([h.get('text', '') for h in history]) if history else "None"

#     try:
#         prompt = QUESTION_PROMPT_TEMPLATE.format(
#             role=role, 
#             level=level, 
#             level_desc=level_desc,
#             history_str=history_str
#         )
        
#         raw_response = parse_with_llm(prompt)
#         cleaned_json = clean_json_output(raw_response)
        
#         # ✅ CRITICAL FIX: If AI returns empty, raise error immediately to trigger fallback
#         if not cleaned_json or cleaned_json == "{}": 
#             raise Exception("Empty AI response received (Rate Limit or Network Error).")

#         data = json.loads(cleaned_json)
        
#         return {
#             "question": data.get("question", f"Tell me about your experience as a {role}."),
#             "follow_up": data.get("follow_up", "Can you elaborate on that?"),
#             "difficulty": level
#         }

#     except Exception as e:
#         print(f"⚠️ Question Generation Failed: {e}")
#         print("🔄 Switching to FALLBACK TEMPLATE to prevent crash.")
        
#         # ✅ FALLBACK LOGIC: Pick a random backup question
#         template = random.choice(FALLBACK_TEMPLATES)
#         return {
#             "question": template["question"].format(role=role),
#             "follow_up": template["follow_up"],
#             "difficulty": level
#         }

# # ---------------------------------------------------------
# # 2. ANALYZE ANSWER
# # ---------------------------------------------------------
# def analyze_answer(transcript: str, question_context: str = "General Interview"):
#     if not transcript or len(transcript) < 5:
#         return {
#             "strengths": ["N/A"], "improvements": ["Answer too short"],
#             "confidence_estimate": 0, "clarity_score": 0, "filler_words_count": {}
#         }

#     try:
#         prompt = ANALYZE_PROMPT.format(transcript=transcript, question=question_context)
#         raw_response = parse_with_llm(prompt)
#         cleaned_json = clean_json_output(raw_response)
        
#         if not cleaned_json or cleaned_json == "{}": 
#             raise Exception("Empty AI response received.")

#         result = json.loads(cleaned_json)
        
#         if "clarity_score" not in result: result["clarity_score"] = 70
#         if "confidence_estimate" not in result: result["confidence_estimate"] = 75
        
#         return result

#     except Exception as e:
#         print(f"⚠️ Analysis Failed: {e}")
#         # FALLBACK: Return dummy analysis so frontend doesn't break
#         return {
#             "filler_words_count": {}, 
#             "confidence_estimate": 70,
#             "strengths": ["Good effort", "Clear communication"], 
#             "improvements": ["Add more technical details", "Structure your answer better"], 
#             "clarity_score": 70
#         }

# # ---------------------------------------------------------
# # ✅ MAIN EXECUTION
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     print(json.dumps(generate_question("DevOps", "Senior"), indent=2))