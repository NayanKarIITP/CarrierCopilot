
# # src/python/resume_parser.py

# import os
# import re
# import json
# import sys
# from typing import Dict, Any
# from dotenv import load_dotenv

# # ---------------------------------------------------------
# # LOAD ENV (SAFE FOR LOCAL + PROD)
# # ---------------------------------------------------------
# load_dotenv()  # harmless in prod, useful locally

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # ---------------------------------------------------------
# # LOGGING (stderr ONLY)
# # ---------------------------------------------------------
# def log_debug(message: str):
#     try:
#         sys.stderr.write(f"[PYTHON LOG] {message}\n")
#         sys.stderr.flush()
#     except:
#         pass

# # ---------------------------------------------------------
# # SAFE IMPORTS
# # ---------------------------------------------------------
# try:
#     import google.generativeai as genai
#     from utils.pdf_reader import read_pdf_text
#     from utils.text_cleaner import clean_text
#     AI_LIB_AVAILABLE = True
# except ImportError as e:
#     log_debug(f"Import error: {e}")
#     AI_LIB_AVAILABLE = False

# # ---------------------------------------------------------
# # CONFIG
# # ---------------------------------------------------------
# API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-flash-latest"

# log_debug(f"GEMINI_API_KEY present: {bool(API_KEY)}")

# AI_AVAILABLE = False
# if AI_LIB_AVAILABLE and API_KEY:
#     try:
#         genai.configure(api_key=API_KEY)
#         AI_AVAILABLE = True
#         log_debug("Gemini enabled")
#     except Exception as e:
#         log_debug(f"Gemini config failed: {e}")

# # ---------------------------------------------------------
# # PROMPTS
# # ---------------------------------------------------------
# EXTRACTION_PROMPT = """
# Extract resume info into JSON:
# {
#   "skills": ["string"],
#   "education": [],
#   "experience": []
# }
# Resume:
# """

# ANALYZE_PROMPT = """
# Analyze resume JSON and return:
# {
#   "resume_score": 75,
#   "feedback": [],
#   "strengths": [],
#   "weaknesses": []
# }
# Data:
# """

# COMMON_SKILLS = ["python", "javascript", "react", "node", "sql", "aws"]

# # ---------------------------------------------------------
# # GEMINI CALL (SAFE)
# # ---------------------------------------------------------
# def call_gemini(prompt: str) -> str | None:
#     if not AI_AVAILABLE:
#         return None
#     try:
#         model = genai.GenerativeModel(MODEL_NAME)
#         response = model.generate_content(prompt)
#         text = response.text or ""
#         text = text.replace("```json", "").replace("```", "").strip()
#         return text
#     except Exception as e:
#         log_debug(f"Gemini error: {e}")
#         return None

# # ---------------------------------------------------------
# # FALLBACKS
# # ---------------------------------------------------------
# def fallback_parse(text: str) -> dict:
#     text_lower = text.lower()
#     skills = [s.capitalize() for s in COMMON_SKILLS if s in text_lower]
#     return {
#         "skills": skills,
#         "education": [],
#         "experience": [],
#         "raw_text": text
#     }

# def fallback_analysis(parsed: dict) -> dict:
#     score = 30 + (20 if parsed.get("skills") else 0)
#     return {
#         "resume_score": min(score, 70),
#         "feedback": ["Improve resume formatting", "Add more projects"],
#         "strengths": parsed.get("skills", []),
#         "weaknesses": []
#     }

# # ---------------------------------------------------------
# # CORE PIPELINE
# # ---------------------------------------------------------
# def process_resume_text(text: str) -> Dict[str, Any]:
#     parsed = None
#     analysis = None

#     # ---- PARSE ----
#     gemini_json = call_gemini(EXTRACTION_PROMPT + text[:8000])
#     if gemini_json:
#         try:
#             parsed = json.loads(gemini_json)
#         except Exception:
#             parsed = None

#     if not parsed:
#         parsed = fallback_parse(text)

#     # ---- ANALYZE ----
#     gemini_analysis = call_gemini(ANALYZE_PROMPT + json.dumps(parsed))
#     if gemini_analysis:
#         try:
#             analysis = json.loads(gemini_analysis)
#         except Exception:
#             analysis = None

#     if not analysis:
#         analysis = fallback_analysis(parsed)

#     return {
#         "success": True,
#         "parsed": parsed,
#         "analysis": analysis,
#         "mode": "ai" if AI_AVAILABLE else "fallback"
#     }

# # ---------------------------------------------------------
# # PUBLIC ENTRY (FILE)
# # ---------------------------------------------------------
# def parse_resume_from_file(file_path: str) -> Dict[str, Any]:
#     try:
#         text = read_pdf_text(file_path)
#         text = clean_text(text)
#         return process_resume_text(text)
#     except Exception as e:
#         log_debug(f"Resume read error: {e}")
#         return {
#             "success": True,
#             "parsed": fallback_parse(""),
#             "analysis": fallback_analysis({"skills": []}),
#             "mode": "fallback"
#         }

# # ---------------------------------------------------------
# # CLI ENTRYPOINT (NODE SPAWN)
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         if len(sys.argv) < 2:
#             print(json.dumps({"success": False, "error": "No file path provided"}))
#             sys.exit(0)

#         file_path = sys.argv[1]
#         result = parse_resume_from_file(file_path)

#         # STRICT JSON OUTPUT
#         print(json.dumps(result))

#     except Exception as e:
#         print(json.dumps({
#             "success": False,
#             "error": str(e),
#             "mode": "fallback"
#         }))








# import os
# import re
# import json
# import sys
# from typing import Dict, Any
# from dotenv import load_dotenv 

# load_dotenv()
# # Ensure we can import local utils
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # ---------------------------------------------------------
# # 🔧 LOGGING HELPER (Prevents Node.js JSON Errors)
# # ---------------------------------------------------------
# def log_debug(message: str):
#     """Writes to stderr so it doesn't break the JSON output in stdout."""
#     try:
#         # We strip emojis just in case to prevent Windows crashes
#         safe_message = message.encode('ascii', 'ignore').decode('ascii')
#         sys.stderr.write(f"[PYTHON LOG] {safe_message}\n")
#         sys.stderr.flush()
#     except Exception:
#         pass

# # 1. Try to import Google AI Library & Utils
# try:
#     import google.generativeai as genai
#     from utils.pdf_reader import read_pdf_text
#     from utils.text_cleaner import clean_text
#     AI_AVAILABLE = True
# except ImportError as e:
#     log_debug(f"Import Error: {e}")
#     AI_AVAILABLE = False

# # ---------------------------------------------------------
# # ⚙️ CONFIGURATION
# # ---------------------------------------------------------

# API_KEY =os.getenv("GEMINI_API_KEY")
# MODEL_NAME = 'gemini-flash-latest' 

# if AI_AVAILABLE and API_KEY:
#     try:
#         genai.configure(api_key=API_KEY)
#     except Exception as e:
#         log_debug(f"Config Error: {e}")

# # ---------------------------------------------------------
# # 🧠 PROMPTS
# # ---------------------------------------------------------

# EXTRACTION_PROMPT = """
# You are an expert ATS Parser. 
# Extract the following from the resume text below into valid JSON:
# {
#     "full_name": "string",
#     "emails": ["string"],
#     "phones": ["string"],
#     "skills": ["string", "string"],
#     "education": [{ "degree": "string", "school": "string", "year": "string" }],
#     "experience": [{ "title": "string", "company": "string", "dates": "string", "bullets": ["string"] }],
#     "projects": [{ "name": "string", "description": "string" }]
# }
# Rules: Return ONLY raw JSON. No markdown.
# Resume Text:
# """

# ANALYZE_PROMPT = """
# You are a Senior Tech Recruiter.
# Analyze the resume data and provide specific feedback.
# Required JSON Structure:
# {
#     "resume_score": 85,
#     "feedback": ["Advice 1", "Advice 2"],
#     "strengths": ["Strength 1", "Strength 2"],
#     "weaknesses": ["Weakness 1", "Weakness 2"]
# }
# Parsed Data:
# """

# COMMON_SKILLS = ['python', 'javascript', 'java', 'react', 'node', 'aws', 'docker', 'sql', 'git']

# # ---------------------------------------------------------
# # 🛠️ HELPER
# # ---------------------------------------------------------

# def call_gemini(prompt: str) -> str:
#     if not AI_AVAILABLE or not API_KEY:
#         raise Exception("Google AI SDK not installed or API Key missing")
#     try:
#         model = genai.GenerativeModel(MODEL_NAME)
#         response = model.generate_content(prompt)
#         return response.text.replace("```json", "").replace("```", "").strip()
#     except Exception as e:
#         log_debug(f"Gemini API Error: {e}")
#         raise e

# # ---------------------------------------------------------
# # 🚀 CORE LOGIC (Shared)
# # ---------------------------------------------------------

# def _process_resume_content(cleaned_text: str) -> Dict[str, Any]:
#     """Internal function to process text with Gemini"""
    
#     # 1. Extraction
#     parsed_data = {}
#     try:
#         log_debug("Extracting data...")
#         json_str = call_gemini(EXTRACTION_PROMPT + cleaned_text[:10000])
#         parsed_data = json.loads(json_str)
#         parsed_data["raw_text"] = cleaned_text 
#     except Exception as e:
#         log_debug(f"Extraction Failed: {e}")
#         parsed_data = _fallback_parse(cleaned_text)

#     # 2. Analysis
#     analysis_data = {}
#     try:
#         log_debug("Analyzing...")
#         analysis_payload = {
#             "skills": parsed_data.get("skills", []),
#             "exp_preview": [e.get("title", "") for e in parsed_data.get("experience", [])]
#         }
#         analysis_json = call_gemini(ANALYZE_PROMPT + json.dumps(analysis_payload))
#         analysis_data = json.loads(analysis_json)
#     except Exception as e:
#         log_debug(f"Analysis Failed: {e}")
#         analysis_data = {
#             "resume_score": _calculate_basic_score(parsed_data),
#             "feedback": _generate_basic_feedback(parsed_data),
#             "strengths": [],
#             "weaknesses": []
#         }

#     return {
#         "parsed": parsed_data,
#         "analysis": analysis_data,
#         "success": True
#     }

# # ---------------------------------------------------------
# # 🚀 EXPORTED FUNCTIONS
# # ---------------------------------------------------------

# def parse_resume_from_file(path: str) -> Dict[str, Any]:
#     # ✅ FIX: No emojis here anymore
#     log_debug(f"Reading PDF: {path}") 
#     try:
#         raw_text = read_pdf_text(path)
#         cleaned_text = clean_text(raw_text)
#         return _process_resume_content(cleaned_text)
#     except Exception as e:
#         log_debug(f"PDF Read Error: {e}")
#         return {"success": False, "error": str(e)}

# def parse_resume_text(text: str) -> Dict[str, Any]:
#     log_debug("Processing Raw Text input...")
#     cleaned_text = clean_text(text)
#     return _process_resume_content(cleaned_text)

# # ---------------------------------------------------------
# # 🛡️ FALLBACKS
# # ---------------------------------------------------------

# def _fallback_parse(text: str) -> dict:
#     text_lower = text.lower()
#     found_skills = [s.capitalize() for s in COMMON_SKILLS if s in text_lower]
#     emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
#     return {
#         "full_name": "Candidate",
#         "emails": emails,
#         "skills": list(set(found_skills)),
#         "education": [],
#         "experience": [],
#         "raw_text": text
#     }

# def _calculate_basic_score(data: dict) -> int:
#     score = 0
#     if data.get("skills"): score += 30
#     if len(data.get("experience", [])) > 0: score += 40
#     return min(score, 75)

# def _generate_basic_feedback(data: dict) -> list:
#     feedback = []
#     if not data.get("skills"): feedback.append("Add a Skills section.")
#     return feedback

# # Aliases
# parse_resume_file = parse_resume_from_file

# if __name__ == "__main__":
#     # Ensure stdout uses utf-8 (fixes some Windows pipe issues)
#     if sys.platform == "win32":
#         sys.stdout.reconfigure(encoding='utf-8')

#     if len(sys.argv) > 1:
#         # ✅ FIX: This is the ONLY print statement (prints final JSON)
#         print(json.dumps(parse_resume_from_file(sys.argv[1]), indent=2))








import os
import re
import json
import sys
import logging
import typing
from dotenv import load_dotenv 

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Logging
logger = logging.getLogger(__name__)

# 1. Try to import Google AI Library & Utils
try:
    import google.generativeai as genai
    from utils.pdf_reader import read_pdf_text
    from utils.text_cleaner import clean_text
    AI_AVAILABLE = True
except ImportError as e:
    logger.error(f"Import Error: {e}")
    AI_AVAILABLE = False

# ⚙️ CONFIGURATION


API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = 'gemini-2.5-flash' 

if AI_AVAILABLE and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        logger.error(f"Config Error: {e}")

# ---------------------------------------------------------
# 🧠 PROMPTS
# ---------------------------------------------------------

EXTRACTION_PROMPT = """
Extract the following from the resume text into JSON format.
If a section is missing, return an empty array [].

{
    "full_name": "string",
    "emails": ["string"],
    "phones": ["string"],
    "skills": ["string"],
    "education": [{ "degree": "string", "school": "string", "year": "string" }],
    "experience": [{ 
        "title": "string", 
        "company": "string", 
        "dates": "string", 
        "description": "string" 
    }],
    "projects": [{ "name": "string", "description": "string" }]
}

Resume Text:
"""

ANALYZE_PROMPT = """
Analyze the resume and provide feedback in JSON format:
{
    "resume_score": 85,
    "feedback": ["Advice 1", "Advice 2"],
    "strengths": ["Strength 1", "Strength 2"],
    "weaknesses": ["Weakness 1", "Weakness 2"]
}
Parsed Data:
"""

COMMON_SKILLS = ['python', 'javascript', 'java', 'react', 'node', 'aws', 'docker', 'sql', 'git']

# ---------------------------------------------------------
# 🚀 CORE LOGIC
# ---------------------------------------------------------

def call_gemini_json(prompt: str, content: str) -> dict:
    """
    ✅ FIX: Uses Native JSON Mode to guarantee valid output
    """
    if not AI_AVAILABLE or not API_KEY:
        raise Exception("Google AI SDK not installed or API Key missing")
    try:
        # Configure model to force JSON output
        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config={"response_mime_type": "application/json"}
        )
        
        response = model.generate_content(prompt + content)
        
        # Parse the response directly
        return json.loads(response.text)
        
    except Exception as e:
        logger.error(f"Gemini JSON Error: {e}")
        # If Native JSON fails, try standard extraction
        try:
             model = genai.GenerativeModel(MODEL_NAME)
             response = model.generate_content(prompt + content)
             text = response.text.replace("```json", "").replace("```", "").strip()
             start = text.find("{")
             end = text.rfind("}")
             return json.loads(text[start:end+1])
        except:
             raise e

def _process_resume_content(cleaned_text: str) -> dict:
    
    # 1. Extraction (The Data Tab)
    parsed_data = {}
    try:
        # Use Native JSON call
        parsed_data = call_gemini_json(EXTRACTION_PROMPT, cleaned_text[:12000])
        parsed_data["raw_text"] = cleaned_text 
    except Exception as e:
        logger.error(f"Extraction Failed: {e}")
        parsed_data = _fallback_parse(cleaned_text)

    # 2. Analysis (The Analysis Tab)
    analysis_data = {}
    try:
        # Prepare small payload
        analysis_payload = {
            "skills": parsed_data.get("skills", []),
            "experience": [e.get("title", "") for e in parsed_data.get("experience", [])]
        }
        # Use Native JSON call
        analysis_data = call_gemini_json(ANALYZE_PROMPT, json.dumps(analysis_payload))
    except Exception as e:
        logger.error(f"Analysis Failed: {e}")
        analysis_data = {
            "resume_score": 50,
            "feedback": ["Could not analyze details."],
            "strengths": [],
            "weaknesses": []
        }

    return {
        "parsed": parsed_data,
        "analysis": analysis_data,
        "success": True
    }

# ---------------------------------------------------------
# 🚀 EXPORTED FUNCTIONS
# ---------------------------------------------------------

def parse_resume_from_file(path: str) -> dict:
    try:
        raw_text = read_pdf_text(path)
        cleaned_text = clean_text(raw_text)
        if not cleaned_text:
            return {"success": False, "error": "Empty PDF"}
        return _process_resume_content(cleaned_text)
    except Exception as e:
        logger.error(f"PDF Error: {e}")
        return {"success": False, "error": str(e)}

def parse_resume_text(text: str) -> dict:
    cleaned_text = clean_text(text)
    return _process_resume_content(cleaned_text)

# ---------------------------------------------------------
# 🛡️ FALLBACKS
# ---------------------------------------------------------

def _fallback_parse(text: str) -> dict:
    text_lower = text.lower()
    found_skills = [s.capitalize() for s in COMMON_SKILLS if s in text_lower]
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return {
        "full_name": "Candidate",
        "emails": emails,
        "skills": list(set(found_skills)),
        "education": [],
        "experience": [],
        "raw_text": text
    }

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) > 1:
        print(json.dumps(parse_resume_from_file(sys.argv[1]), indent=2))