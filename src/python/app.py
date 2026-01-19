# # src/python/app.py

# # For production
# import os
# import sys
# import uvicorn
# import logging
# import uuid
# import shutil
# import tempfile

# # ✅ FIX: These lines were commented out. They are REQUIRED.
# from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict, Optional, List, Any

# # ---------------------------------------------------------
# # 🔧 CONFIG & LOGGING
# # ---------------------------------------------------------
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# # Ensure current directory is in path so we can import local modules
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# if BASE_DIR not in sys.path:
#     sys.path.append(BASE_DIR)

# # ---------------------------------------------------------
# # ✅ ROBUST IMPORTS (Handles running from Root or Src)
# # ---------------------------------------------------------

# # 1. Interview Assistant
# try:
#     from interview_assistant import generate_question, analyze_answer
#     logger.info("✅ Interview Module loaded.")
# except ImportError:
#     try:
#         from src.python.interview_assistant import generate_question, analyze_answer
#         logger.info("✅ Interview Module loaded (via package).")
#     except ImportError:
#         logger.warning("⚠️ Interview Module missing. Using fallbacks.")
#         def generate_question(role, level, history=None): 
#             return {"question": "Describe a project you are proud of.", "follow_up": "Why?", "difficulty": level}
#         def analyze_answer(text, question_context=None): 
#             return {"strengths": ["Good flow"], "improvements": ["More detail"], "clarity_score": 80}

# # 2. Frame Analyzer
# try:
#     from frame_analyzer import analyze_frame 
#     logger.info("✅ Visual AI loaded.")
# except ImportError:
#     try:
#         from src.python.frame_analyzer import analyze_frame
#         logger.info("✅ Visual AI loaded (via package).")
#     except ImportError:
#         def analyze_frame(img): return {"success": False, "error": "Visual AI missing."}

# # 3. Roadmap Generator
# try:
#     from roadmap_generator import generate_roadmap
#     logger.info("✅ Roadmap Module loaded.")
# except ImportError:
#     try:
#         from src.python.roadmap_generator import generate_roadmap
#         logger.info("✅ Roadmap Module loaded (via package).")
#     except ImportError:
#         def generate_roadmap(role, skills): return {"roadmap": []}

# # 4. Market Trends
# try:
#     from market_trends import get_market_trends
#     logger.info("✅ Trends Module loaded.")
# except ImportError:
#     try:
#         from src.python.market_trends import get_market_trends
#         logger.info("✅ Trends Module loaded (via package).")
#     except ImportError:
#         def get_market_trends(role=None): return {"trends": ["AI is growing", "Remote work is standard"]}

# # 5. Resume Parser & Gap Analyzer
# try:
#     from resume_parser import parse_resume_text, parse_resume_from_file
#     from skill_gap_analyzer import analyze_skill_gap
#     logger.info("✅ Resume & Gap Modules loaded.")
# except ImportError:
#     try:
#         from src.python.resume_parser import parse_resume_text, parse_resume_from_file
#         from src.python.skill_gap_analyzer import analyze_skill_gap
#         logger.info("✅ Resume & Gap Modules loaded (via package).")
#     except ImportError:
#         def parse_resume_text(text): return {"skills": []}
#         def parse_resume_from_file(path): return {"parsed": {}, "analysis": {}}
#         def analyze_skill_gap(current, target): return {"missing_skills": ["Python"]}

# # ---------------------------------------------------------
# # 🚀 APP SETUP
# # ---------------------------------------------------------
# app = FastAPI(title="AI Career Copilot 2.0 - Unified Engine")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------------------------------------------
# # 📦 DATA MODELS
# # ---------------------------------------------------------
# class InterviewStartModel(BaseModel):
#     role: str
#     level: str

# class QuestionRequest(BaseModel):
#     sessionId: str
#     role: str
#     level: str

# class InterviewInput(BaseModel):
#     question: Optional[str] = None
#     answer: Optional[str] = None
#     transcript: Optional[str] = None

# class FramePayload(BaseModel):
#     image_base64: str

# class RoadmapInput(BaseModel):
#     role: str
#     skills: List[str]

# class GapInput(BaseModel):
#     current_skills: List[str]
#     target_role: str

# class ResumeAnalysisInput(BaseModel):
#     text: str
#     target_role: Optional[str] = None

# class ResumeParseRequest(BaseModel):
#     url: str
#     target_role: Optional[str] = "fullstack-developer"

# # ---------------------------------------------------------
# # 🧠 SESSION STORAGE (In-Memory)
# # ---------------------------------------------------------
# SESSIONS: Dict[str, List[Dict[str, Any]]] = {}

# def new_id(): return uuid.uuid4().hex[:10]

# def clean_base64(b64_string: str) -> str:
#     if "," in b64_string: return b64_string.split(",")[1]
#     return b64_string

# # ---------------------------------------------------------
# # 🔗 ENDPOINTS
# # ---------------------------------------------------------

# @app.get("/")
# def health():
#     return {"status": "ok", "engine": "Python AI Engine Running"}

# # ==========================================
# # 1️⃣ INTERVIEW ROUTES
# # ==========================================
# @app.post("/interview/start")
# def interview_start(payload: InterviewStartModel):
#     session_id = new_id()
#     try:
#         raw = generate_question(payload.role, payload.level, history=[])
#         q = {
#             "_id": new_id(),
#             "text": raw.get("question", "Tell me about yourself."),
#             "follow_up": raw.get("follow_up", ""),
#             "difficulty": payload.level
#         }
#         SESSIONS[session_id] = [q]
#         return { "success": True, "sessionId": session_id, "question": q }
#     except Exception as e:
#         logger.error(f"Start Error: {e}")
#         return {"success": False, "error": str(e)}

# @app.post("/interview/next-question")
# def interview_next(req: QuestionRequest):
#     if req.sessionId not in SESSIONS: SESSIONS[req.sessionId] = []
#     try:
#         raw = generate_question(req.role, req.level, history=SESSIONS[req.sessionId])
#         q = {
#             "_id": new_id(),
#             "text": raw.get("question", "Describe a challenge."),
#             "follow_up": raw.get("follow_up", ""),
#             "difficulty": req.level
#         }
#         SESSIONS[req.sessionId].append(q)
#         return { "success": True, "question": q }
#     except Exception as e:
#         logger.error(f"Next Error: {e}")
#         return {"success": False, "error": str(e)}

# @app.post("/interview/analyze")
# def interview_analyze(payload: InterviewInput):
#     text = payload.answer or payload.transcript
#     if not text or len(text) < 5:
#         return { "success": True, "data": { "analysis": { "strengths": [], "clarity_score": 0 } } }
    
#     result = analyze_answer(text)
#     return { "success": True, "data": { "analysis": result } }

# @app.post("/interview/frame-metrics")
# def frame_metrics(payload: FramePayload):
#     img = clean_base64(payload.image_base64)
#     result = analyze_frame(img)
#     return result if "success" in result else {"success": True, "metrics": result}

# # ==========================================
# # 2️⃣ ROADMAP ROUTES
# # ==========================================
# @app.post("/roadmap/generate")
# def api_generate_roadmap(payload: RoadmapInput):
#     logger.info(f"🛣️ Generating roadmap for {payload.role}")
#     result = generate_roadmap(payload.role, payload.skills)
#     return result

# @app.post("/roadmap/gap")
# def api_skill_gap(payload: GapInput):
#     result = analyze_skill_gap(payload.current_skills, payload.target_role)
#     return result

# # ==========================================
# # 3️⃣ TRENDS ROUTES
# # ==========================================
# @app.get("/trends")
# def api_trends(role: Optional[str] = "Software Engineer"):
#     result = get_market_trends(role)
#     return result

# # ==========================================
# # 4️⃣ RESUME ROUTES (GEMINI NATIVE)
# # ==========================================
# @app.post("/resume/parse")
# def parse_resume(payload: ResumeParseRequest):
#     try:
#         logger.info(f"📄 Parsing Resume URL: {payload.url}")

#         # 1. Call the new Gemini Native Parser
#         # The parser now handles download and analysis
#         result = parse_resume_from_file(payload.url)

#         if not result.get("success"):
#             logger.error(f"Parser failed: {result.get('error')}")
#             return result 

#         # 2. Extract the flat data object
#         ai_data = result.get("data", {})

#         # 3. Construct the Response
#         response_payload = {
#             "success": True,
#             "score": ai_data.get("resume_score", 0),
#             "feedback": ai_data.get("feedback", []),
#             "strengths": ai_data.get("strengths", []),
#             "weaknesses": ai_data.get("weaknesses", []),
#             "data": ai_data, 
#             "skills": ai_data.get("skills", []),
#             "experience": ai_data.get("experience", []),
#             "education": ai_data.get("education", []),
#             "text": "Extracted via Gemini Vision" 
#         }

#         return response_payload

#     except Exception as e:
#         logger.error(f"Route Error: {e}")
#         return {"success": False, "error": str(e)}
    
# # ==========================================
# # 🚀 MAIN ENTRY POINT
# # ==========================================
# if __name__ == "__main__":
#     port = int(os.environ.get("PYTHON_PORT", 8000))
#     logger.info(f"🔥 Python Engine starting on Port {port}...")
#     uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)









# # #For production
# # #app.py
# # import os
# # import sys
# # import uvicorn
# # import logging
# # import uuid
# # import shutil
# # import tempfile
# # from fastapi import FastAPI, HTTPException, UploadFile, File, Form
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # from typing import Dict, Optional, List, Any

# # # ---------------------------------------------------------
# # # 🔧 CONFIG & LOGGING
# # # ---------------------------------------------------------
# # logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# # logger = logging.getLogger(__name__)

# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # sys.path.append(BASE_DIR)
# # sys.path.append(os.path.join(BASE_DIR, "utils"))

# # # ---------------------------------------------------------
# # # ✅ SAFE IMPORTS
# # # ---------------------------------------------------------
# # # 1. Interview Assistant
# # try:
# #     from interview_assistant import generate_question, analyze_answer
# #     logger.info("✅ Interview Module loaded.")
# # except ImportError:
# #     logger.warning("⚠️ Interview Module missing. Using fallbacks.")
# #     def generate_question(role, level, history=None): 
# #         return {"question": "Describe a project you are proud of.", "follow_up": "Why?"}
# #     def analyze_answer(text): 
# #         return {"strengths": ["Good flow"], "improvements": ["More detail"], "clarity_score": 80}

# # # 2. Frame Analyzer
# # try:
# #     from frame_analyzer import analyze_frame 
# #     logger.info("✅ Visual AI loaded.")
# # except ImportError:
# #     def analyze_frame(img): return {"success": False, "error": "Visual AI missing."}

# # # 3. Roadmap Generator
# # try:
# #     from roadmap_generator import generate_roadmap
# #     logger.info("✅ Roadmap Module loaded.")
# # except ImportError:
# #     def generate_roadmap(role, skills): return {"roadmap": []}

# # # 4. Market Trends
# # try:
# #     from market_trends import get_market_trends
# #     logger.info("✅ Trends Module loaded.")
# # except ImportError:
# #     def get_market_trends(role=None): return {"trends": ["AI is growing", "Remote work is standard"]}

# # # 5. Resume Parser & Gap Analyzer
# # try:
# #     from resume_parser import parse_resume_text, parse_resume_from_file
# #     from skill_gap_analyzer import analyze_skill_gap
# #     logger.info("✅ Resume & Gap Modules loaded.")
# # except ImportError:
# #     def parse_resume_text(text): return {"skills": []}
# #     def parse_resume_from_file(path): return {"parsed": {}, "analysis": {}}
# #     def analyze_skill_gap(current, target): return {"missing_skills": ["Python"]}

# # # ---------------------------------------------------------
# # # 🚀 APP SETUP
# # # ---------------------------------------------------------
# # app = FastAPI(title="AI Career Copilot 2.0 - Unified Engine")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # ---------------------------------------------------------
# # # 📦 DATA MODELS
# # # ---------------------------------------------------------
# # class InterviewStartModel(BaseModel):
# #     role: str
# #     level: str

# # class QuestionRequest(BaseModel):
# #     sessionId: str
# #     role: str
# #     level: str

# # class InterviewInput(BaseModel):
# #     question: Optional[str] = None
# #     answer: Optional[str] = None
# #     transcript: Optional[str] = None

# # class FramePayload(BaseModel):
# #     image_base64: str

# # class RoadmapInput(BaseModel):
# #     role: str
# #     skills: List[str]

# # class GapInput(BaseModel):
# #     current_skills: List[str]
# #     target_role: str

# # class ResumeAnalysisInput(BaseModel):
# #     text: str
# #     target_role: Optional[str] = None

# # # ✅ NEW: Model for URL-based Resume Parsing
# # class ResumeParseRequest(BaseModel):
# #     url: str
# #     target_role: Optional[str] = "fullstack-developer"

# # # ---------------------------------------------------------
# # # 🧠 SESSION STORAGE (In-Memory)
# # # ---------------------------------------------------------
# # SESSIONS: Dict[str, List[Dict[str, Any]]] = {}

# # def new_id(): return uuid.uuid4().hex[:10]

# # def clean_base64(b64_string: str) -> str:
# #     if "," in b64_string: return b64_string.split(",")[1]
# #     return b64_string

# # # ---------------------------------------------------------
# # # 🔗 ENDPOINTS
# # # ---------------------------------------------------------

# # @app.get("/")
# # def health():
# #     return {"status": "ok", "engine": "Python AI Engine Running"}

# # # ==========================================
# # # 1️⃣ INTERVIEW ROUTES
# # # ==========================================
# # @app.post("/interview/start")
# # def interview_start(payload: InterviewStartModel):
# #     session_id = new_id()
# #     try:
# #         raw = generate_question(payload.role, payload.level, history=[])
# #         q = {
# #             "_id": new_id(),
# #             "text": raw.get("question", "Tell me about yourself."),
# #             "follow_up": raw.get("follow_up", ""),
# #             "difficulty": payload.level
# #         }
# #         SESSIONS[session_id] = [q]
# #         return { "success": True, "sessionId": session_id, "question": q }
# #     except Exception as e:
# #         logger.error(f"Start Error: {e}")
# #         return {"success": False, "error": str(e)}

# # @app.post("/interview/next-question")
# # def interview_next(req: QuestionRequest):
# #     if req.sessionId not in SESSIONS: SESSIONS[req.sessionId] = []
# #     try:
# #         raw = generate_question(req.role, req.level, history=SESSIONS[req.sessionId])
# #         q = {
# #             "_id": new_id(),
# #             "text": raw.get("question", "Describe a challenge."),
# #             "follow_up": raw.get("follow_up", ""),
# #             "difficulty": req.level
# #         }
# #         SESSIONS[req.sessionId].append(q)
# #         return { "success": True, "question": q }
# #     except Exception as e:
# #         logger.error(f"Next Error: {e}")
# #         return {"success": False, "error": str(e)}

# # @app.post("/interview/analyze")
# # def interview_analyze(payload: InterviewInput):
# #     text = payload.answer or payload.transcript
# #     if not text or len(text) < 5:
# #         return { "success": True, "data": { "analysis": { "strengths": [], "clarity_score": 0 } } }
    
# #     result = analyze_answer(text)
# #     return { "success": True, "data": { "analysis": result } }

# # @app.post("/interview/frame-metrics")
# # def frame_metrics(payload: FramePayload):
# #     img = clean_base64(payload.image_base64)
# #     result = analyze_frame(img)
# #     return result if "success" in result else {"success": True, "metrics": result}

# # # ==========================================
# # # 2️⃣ ROADMAP ROUTES
# # # ==========================================
# # @app.post("/roadmap/generate")
# # def api_generate_roadmap(payload: RoadmapInput):
# #     logger.info(f"🛣️ Generating roadmap for {payload.role}")
# #     result = generate_roadmap(payload.role, payload.skills)
# #     return result

# # @app.post("/roadmap/gap")
# # def api_skill_gap(payload: GapInput):
# #     result = analyze_skill_gap(payload.current_skills, payload.target_role)
# #     return result

# # # ==========================================
# # # 3️⃣ TRENDS ROUTES
# # # ==========================================
# # @app.get("/trends")
# # def api_trends(role: Optional[str] = "Software Engineer"):
# #     result = get_market_trends(role)
# #     return result

# # # ==========================================
# # # 4️⃣ RESUME ROUTES (✅ UPDATED FOR GEMINI NATIVE)
# # # ==========================================
# # @app.post("/resume/parse")
# # def parse_resume(payload: ResumeParseRequest):
# #     # Safety Check
# #     if 'parse_resume_from_file' not in globals():
# #         raise HTTPException(status_code=500, detail="Parser not loaded")

# #     try:
# #         logger.info(f"📄 Parsing Resume URL: {payload.url}")

# #         # 1. Call the new Gemini Native Parser
# #         result = parse_resume_from_file(payload.url)

# #         if not result.get("success"):
# #             logger.error(f"Parser failed: {result.get('error')}")
# #             return result 

# #         # 2. Extract the flat data object
# #         ai_data = result.get("data", {})

# #         # 3. Construct the Response (Flattened for Frontend)
# #         response_payload = {
# #             "success": True,
# #             "score": ai_data.get("resume_score", 0),
# #             "feedback": ai_data.get("feedback", []),
# #             "strengths": ai_data.get("strengths", []),
# #             "weaknesses": ai_data.get("weaknesses", []),
            
# #             # Pass the WHOLE object as 'data' so page.tsx finds skills/experience there
# #             "data": ai_data, 
            
# #             # Legacy support fields (populating root level too, just in case)
# #             "skills": ai_data.get("skills", []),
# #             "experience": ai_data.get("experience", []),
# #             "education": ai_data.get("education", []),
# #             "text": "Extracted via Gemini Vision" 
# #         }

# #         return response_payload

# #     except Exception as e:
# #         logger.error(f"Route Error: {e}")
# #         return {"success": False, "error": str(e)}
    
# # # ==========================================
# # # 🚀 MAIN ENTRY POINT
# # # ==========================================
# # if __name__ == "__main__":
# #     port = int(os.environ.get("PYTHON_PORT", 8000))
# #     logger.info(f"🔥 Python Engine starting on Port {port}...")
# #     uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)







# src/python/app.py

import os
import sys
import uvicorn
import logging
import uuid
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List, Any

# ---------------------------------------------------------
# 🔧 CONFIG & LOGGING
# ---------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ensure current directory is in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ---------------------------------------------------------
# 🛠️ HELPER: ROBUST JSON PARSER (The Fix for Gemini Errors)
# ---------------------------------------------------------
def clean_and_parse_json(ai_text):
    """
    Attempts to fix common AI JSON syntax errors before parsing.
    """
    try:
        # 1. Try direct parse
        return json.loads(ai_text)
    except json.JSONDecodeError:
        try:
            # 2. Extract JSON from Markdown code blocks
            match = re.search(r"```json\n(.*?)```", ai_text, re.DOTALL)
            text_to_parse = match.group(1) if match else ai_text
            
            # 3. Fix common trailing commas (e.g., "item",] -> "item"])
            text_to_parse = re.sub(r",\s*([\]}])", r"\1", text_to_parse)
            
            return json.loads(text_to_parse)
        except Exception:
            logger.error(f"❌ Failed to parse AI JSON. Raw text start: {ai_text[:100]}...")
            return None

# ---------------------------------------------------------
# ✅ MODULE IMPORTS (With Fallbacks)
# ---------------------------------------------------------
try:
    from interview_assistant import generate_question, analyze_answer
    logger.info("✅ Interview Module loaded.")
except ImportError:
    logger.warning("⚠️ Interview Module missing.")
    def generate_question(role, level, history=None): return {"question": "Describe a project.", "difficulty": level}
    def analyze_answer(text, question_context=None): return {"strengths": [], "clarity_score": 0}

try:
    from frame_analyzer import analyze_frame 
    logger.info("✅ Visual AI loaded.")
except ImportError:
    def analyze_frame(img): return {"success": False, "error": "Visual AI missing."}

try:
    from roadmap_generator import generate_roadmap
    logger.info("✅ Roadmap Module loaded.")
except ImportError:
    def generate_roadmap(role, skills): return {"roadmap": []}

try:
    from market_trends import get_market_trends
    logger.info("✅ Trends Module loaded.")
except ImportError:
    def get_market_trends(role=None): return {"trends": []}

try:
    from resume_parser import parse_resume_from_file
    from skill_gap_analyzer import analyze_skill_gap
    logger.info("✅ Resume & Gap Modules loaded.")
except ImportError:
    def parse_resume_from_file(path): return {"success": False, "error": "Parser missing"}
    def analyze_skill_gap(current, target): return {"missing_skills": []}


# ---------------------------------------------------------
# 🚀 APP SETUP
# ---------------------------------------------------------
app = FastAPI(title="AI Career Copilot 2.0 - Unified Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 📦 DATA MODELS
# ---------------------------------------------------------
class InterviewStartModel(BaseModel):
    role: str
    level: str

class QuestionRequest(BaseModel):
    sessionId: str
    role: str
    level: str

class InterviewInput(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    transcript: Optional[str] = None

class FramePayload(BaseModel):
    image_base64: str

class RoadmapInput(BaseModel):
    role: str
    skills: List[str]

class GapInput(BaseModel):
    current_skills: List[str]
    target_role: str

class ResumeParseRequest(BaseModel):
    url: str
    target_role: Optional[str] = "fullstack-developer"

# ---------------------------------------------------------
# 🧠 SESSION STORAGE
# ---------------------------------------------------------
SESSIONS: Dict[str, List[Dict[str, Any]]] = {}

def new_id(): return uuid.uuid4().hex[:10]

# ---------------------------------------------------------
# 🔗 ENDPOINTS
# ---------------------------------------------------------

@app.get("/")
def health():
    return {"status": "ok", "engine": "Python AI Engine Running"}

# --- Interview Routes ---
@app.post("/interview/start")
def interview_start(payload: InterviewStartModel):
    session_id = new_id()
    raw = generate_question(payload.role, payload.level, history=[])
    q = {
        "_id": new_id(),
        "text": raw.get("question", "Tell me about yourself."),
        "follow_up": raw.get("follow_up", ""),
        "difficulty": payload.level
    }
    SESSIONS[session_id] = [q]
    return { "success": True, "sessionId": session_id, "question": q }

@app.post("/interview/next-question")
def interview_next(req: QuestionRequest):
    if req.sessionId not in SESSIONS: SESSIONS[req.sessionId] = []
    raw = generate_question(req.role, req.level, history=SESSIONS[req.sessionId])
    q = {
        "_id": new_id(),
        "text": raw.get("question", "Describe a challenge."),
        "follow_up": raw.get("follow_up", ""),
        "difficulty": req.level
    }
    SESSIONS[req.sessionId].append(q)
    return { "success": True, "question": q }

@app.post("/interview/analyze")
def interview_analyze(payload: InterviewInput):
    text = payload.answer or payload.transcript
    if not text or len(text) < 5:
        return { "success": True, "data": { "analysis": { "strengths": [], "clarity_score": 0 } } }
    result = analyze_answer(text)
    return { "success": True, "data": { "analysis": result } }

@app.post("/interview/frame-metrics")
def frame_metrics(payload: FramePayload):
    # Basic cleanup if header exists
    img = payload.image_base64.split(",")[1] if "," in payload.image_base64 else payload.image_base64
    result = analyze_frame(img)
    return result if "success" in result else {"success": True, "metrics": result}

# --- Roadmap & Trends ---
@app.post("/roadmap/generate")
def api_generate_roadmap(payload: RoadmapInput):
    return generate_roadmap(payload.role, payload.skills)

@app.post("/roadmap/gap")
def api_skill_gap(payload: GapInput):
    return analyze_skill_gap(payload.current_skills, payload.target_role)

@app.get("/trends")
def api_trends(role: Optional[str] = "Software Engineer"):
    return get_market_trends(role)

# ==========================================
# 4️⃣ RESUME ROUTES (✅ FIXED & ROBUST)
# ==========================================
@app.post("/resume/parse")
def parse_resume(payload: ResumeParseRequest):
    try:
        logger.info(f"📄 Parsing Resume URL: {payload.url}")

        # 1. Call Gemini Parser
        result = parse_resume_from_file(payload.url)

        # 2. Check for Soft Failures (Bad JSON from AI)
        if not result.get("success"):
            error_msg = result.get("error", "")
            
            # If it was a JSON error, we can try to recover or send a Partial Success
            if "JSON" in str(error_msg) or "expecting" in str(error_msg).lower():
                logger.warning("⚠️ JSON Error detected. Returning fallback data.")
                return {
                    "success": True,
                    "score": 50,
                    "feedback": ["Resume parsed but AI formatting was imperfect. Please review extracted data."],
                    "data": { "skills": ["Review Extracted Text"], "experience": [] },
                    "text": "Partial extraction due to AI formatting error."
                }
            
            logger.error(f"Parser failed: {error_msg}")
            return result 

        # 3. Extract Data safely
        ai_data = result.get("data", {})
        
        # 4. Construct Response
        return {
            "success": True,
            "score": ai_data.get("resume_score", 0),
            "feedback": ai_data.get("feedback", []),
            "strengths": ai_data.get("strengths", []),
            "weaknesses": ai_data.get("weaknesses", []),
            "data": ai_data, 
            "skills": ai_data.get("skills", []),
            "experience": ai_data.get("experience", []),
            "education": ai_data.get("education", []),
            "text": ai_data.get("raw_text", "Extracted via Gemini Vision")
        }

    except Exception as e:
        logger.error(f"Route Error: {e}")
        return {"success": False, "error": str(e)}

# ==========================================
# 🚀 MAIN ENTRY POINT
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PYTHON_PORT", 8000))
    logger.info(f"🔥 Python Engine starting on Port {port}...")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)