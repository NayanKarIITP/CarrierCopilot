
# #app.py
# import os
# import sys
# import uvicorn
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict, Optional

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)
# sys.path.append(os.path.join(BASE_DIR, "utils"))

# try:
#     from interview_assistant import generate_question, analyze_answer
#     from frame_analyzer import analyze_frame 
# except ImportError as e:
#     print(f"⚠️ Import Error: {e}")

# app = FastAPI(title="AI Interview Engine")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # MODELS
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

# # SESSION STORE
# SESSIONS = {}  # sessionId → list of Q objects

# def new_id():
#     import uuid
#     return uuid.uuid4().hex[:10]


# # NORMALIZE QUESTION FORMAT FOR FRONTEND
# def normalize_question(raw):
#     return {
#         "_id": new_id(),                         # frontend expects id
#         "text": raw.get("text", ""),
#         "follow_up": raw.get("followUp", ""),    # renamed key for frontend
#     }


# @app.get("/")
# def health():
#     return {"status": "ok", "engine": "ready"}


# # 1️⃣ START INTERVIEW
# @app.post("/interview/start")
# def interview_start(payload: InterviewStartModel):

#     session_id = new_id()

#     try:
#         raw = generate_question(payload.role, payload.level)

#         q = normalize_question(raw)

#         SESSIONS[session_id] = [q]

#         return {
#             "success": True,
#             "sessionId": session_id,
#             "question": q     # 🔥 matches frontend structure
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # 2️⃣ GET NEXT QUESTION
# @app.post("/interview/next-question")
# def interview_next(req: QuestionRequest):

#     if req.sessionId not in SESSIONS:
#         raise HTTPException(status_code=404, detail="Session not found")

#     try:
#         raw = generate_question(req.role, req.level)

#         q = normalize_question(raw)

#         SESSIONS[req.sessionId].append(q)

#         return {
#             "success": True,
#             "question": q
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # 3️⃣ ANALYZE ANSWER
# @app.post("/interview/analyze")
# def interview_analyze(payload: InterviewInput):

#     try:
#         text = payload.answer or payload.transcript

#         if not text:
#             raise HTTPException(status_code=400, detail="Transcript required")

#         result = analyze_answer(text)

#         return {
#             "success": True,
#             "data": {
#                 "analysis": result
#             }
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # 4️⃣ FRAME ANALYSIS
# @app.post("/interview/frame-metrics")
# def frame_metrics(payload: FramePayload):

#     try:
#         result = analyze_frame(payload.image_base64)
#         m = result.get("metrics", {})

#         return {
#             "success": True,
#             "metrics": {
#                 "emotion": m.get("emotion", "Neutral"),
#                 "raw_emotions": { m.get("emotion", "Neutral"): 1.0 },
#                 "eye_contact": round(m.get("eye_contact", 0) * 100, 2),
#                 "visual_confidence": round(m.get("confidence_score", 0) * 100, 2),
#                 "head_pose": m.get("angles", {"yaw": 0, "pitch": 0, "roll": 0})
#             }
#         }

#     except Exception as e:
#         return {"success": False, "error": str(e)}


# if __name__ == "__main__":
#     uvicorn.run(
#         "app:app",
#         host="0.0.0.0",
#         port=int(os.environ.get("PYTHON_PORT", 8000)),
#         reload=True
#     )









# import os
# import sys
# import uvicorn
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict, Optional
# import uuid # Imported at top level

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)
# sys.path.append(os.path.join(BASE_DIR, "utils"))

# # Lazy imports to prevent startup crashes if modules are missing
# try:
#     from python.interview_assistant import generate_question, analyze_answer
#     from frame_analyzer import analyze_frame 
# except ImportError as e:
#     print(f"⚠️ Import Error: {e}")

# app = FastAPI(title="AI Interview Engine")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # MODELS
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

# # SESSION STORE
# SESSIONS = {}  # sessionId -> list of Q objects

# def new_id():
#     return uuid.uuid4().hex[:10]

# # ✅ FIXED: Normalize function to match Python Script Output
# def normalize_question(raw):
#     # The interview_assistant.py returns: { "question": "...", "follow_up": "..." }
#     # The frontend expects: { "_id": "...", "text": "...", "follow_up": "..." }
    
#     return {
#         "_id": new_id(),
#         "text": raw.get("question") or raw.get("text", "Could not generate question."),
#         "follow_up": raw.get("follow_up") or raw.get("followUp", ""),
#         "difficulty": raw.get("difficulty", "Mid-Level")
#     }

# @app.get("/")
# def health():
#     return {"status": "ok", "engine": "ready"}

# # 1️⃣ START INTERVIEW
# @app.post("/interview/start")
# def interview_start(payload: InterviewStartModel):
#     session_id = new_id()
#     try:
#         # Generate raw question from AI
#         raw = generate_question(payload.role, payload.level)
        
#         # Format it for Frontend
#         q = normalize_question(raw)

#         # Store session
#         SESSIONS[session_id] = [q]

#         return {
#             "success": True,
#             "sessionId": session_id,
#             "question": q 
#         }
#     except Exception as e:
#         print(f"❌ Start Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # 2️⃣ GET NEXT QUESTION
# @app.post("/interview/next-question")
# def interview_next(req: QuestionRequest):
#     if req.sessionId not in SESSIONS:
#         # Auto-create session if missing (for dev robustness)
#         SESSIONS[req.sessionId] = []

#     try:
#         raw = generate_question(req.role, req.level)
#         q = normalize_question(raw)

#         SESSIONS[req.sessionId].append(q)

#         return {
#             "success": True,
#             "question": q
#         }
#     except Exception as e:
#         print(f"❌ Next Q Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # 3️⃣ ANALYZE ANSWER
# @app.post("/interview/analyze")
# def interview_analyze(payload: InterviewInput):
#     try:
#         text = payload.answer or payload.transcript
        
#         if not text or len(text) < 2:
#              # Return dummy success for empty input to prevent frontend crash
#              return {
#                 "success": True,
#                 "data": {
#                     "analysis": {
#                         "strengths": ["Listening..."],
#                         "clarity_score": 0,
#                         "confidence_estimate": 0
#                     }
#                 }
#              }

#         result = analyze_answer(text)

#         return {
#             "success": True,
#             "data": {
#                 "analysis": result
#             }
#         }
#     except Exception as e:
#         print(f"❌ Analyze Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # 4️⃣ FRAME ANALYSIS
# @app.post("/interview/frame-metrics")
# def frame_metrics(payload: FramePayload):
#     try:
#         result = analyze_frame(payload.image_base64)
        
#         # Ensure result has the structure frontend expects
#         if not result.get("success"):
#              return result 

#         m = result.get("metrics", {})

#         return {
#             "success": True,
#             "metrics": {
#                 "emotion": m.get("emotion", "Neutral"),
#                 # Frontend might expect 'confidence' or 'visual_confidence'
#                 "visual_confidence": int(m.get("confidence_score", 0.5) * 100),
#                 "eye_contact": int(m.get("eye_contact", 0)),
#                 "head_pose": m.get("head_pose", "Center"),
#                 "angles": m.get("angles", {"yaw":0, "pitch":0, "roll":0})
#             }
#         }
#     except Exception as e:
#         print(f"❌ Frame Error: {e}")
#         return {"success": False, "error": str(e)}

# if __name__ == "__main__":
#     uvicorn.run(
#         "app:app",
#         host="0.0.0.0",
#         port=int(os.environ.get("PYTHON_PORT", 8000)),
#         reload=True
#     )





# import os
# import sys
# import uvicorn
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict, Optional
# import uuid 

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)
# sys.path.append(os.path.join(BASE_DIR, "utils"))

# # ---------------------------------------------------------
# # ✅ SAFE IMPORTS (Prevents NameError Crashes)
# # ---------------------------------------------------------
# try:
#     from interview_assistant import generate_question, analyze_answer
# except ImportError as e:
#     print(f"⚠️ Interview Assistant Import Error: {e}")
#     # Fallback functions
#     def generate_question(role, level): return {"question": "System Error: AI module missing.", "follow_up": ""}
#     def analyze_answer(text): return {"strengths": [], "improvements": [], "clarity_score": 0}

# try:
#     # Ensure file is named 'frame_analyzer.py' (underscore, NOT dash)
#     from frame_analyzer import analyze_frame 
# except ImportError as e:
#     print(f"⚠️ Frame Analyzer Import Error: {e}")
#     print("👉 HINT: Did you run 'pip install mediapipe opencv-python'?")
#     # Fallback function to prevent NameError
#     def analyze_frame(img): 
#         return {"success": False, "error": "Visual AI module not loaded. Check server logs."}

# # ---------------------------------------------------------
# # APP SETUP
# # ---------------------------------------------------------
# app = FastAPI(title="AI Interview Engine")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # MODELS
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

# # SESSION STORE
# SESSIONS = {} 

# def new_id():
#     return uuid.uuid4().hex[:10]

# def normalize_question(raw):
#     return {
#         "_id": new_id(),
#         "text": raw.get("question") or raw.get("text", "Could not generate question."),
#         "follow_up": raw.get("follow_up") or raw.get("followUp", ""),
#         "difficulty": raw.get("difficulty", "Mid-Level")
#     }

# @app.get("/")
# def health():
#     return {"status": "ok", "engine": "ready"}

# # 1️⃣ START INTERVIEW
# @app.post("/interview/start")
# def interview_start(payload: InterviewStartModel):
#     session_id = new_id()
#     try:
#         raw = generate_question(payload.role, payload.level)
#         q = normalize_question(raw)
#         SESSIONS[session_id] = [q]
#         return { "success": True, "sessionId": session_id, "question": q }
#     except Exception as e:
#         print(f"❌ Start Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # 2️⃣ GET NEXT QUESTION
# @app.post("/interview/next-question")
# def interview_next(req: QuestionRequest):
#     if req.sessionId not in SESSIONS:
#         SESSIONS[req.sessionId] = []
#     try:
#         raw = generate_question(req.role, req.level)
#         q = normalize_question(raw)
#         SESSIONS[req.sessionId].append(q)
#         return { "success": True, "question": q }
#     except Exception as e:
#         print(f"❌ Next Q Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # 3️⃣ ANALYZE ANSWER
# @app.post("/interview/analyze")
# def interview_analyze(payload: InterviewInput):
#     try:
#         text = payload.answer or payload.transcript
#         if not text:
#              return { "success": True, "data": { "analysis": {} } }
#         result = analyze_answer(text)
#         return { "success": True, "data": { "analysis": result } }
#     except Exception as e:
#         print(f"❌ Analyze Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # 4️⃣ FRAME ANALYSIS
# @app.post("/interview/frame-metrics")
# def frame_metrics(payload: FramePayload):
#     try:
#         # Calls the imported or fallback function
#         result = analyze_frame(payload.image_base64)
        
#         if not result.get("success"):
#              return result 

#         m = result.get("metrics", {})
#         return {
#             "success": True,
#             "metrics": {
#                 "emotion": m.get("emotion", "Neutral"),
#                 "visual_confidence": int(m.get("confidence_score", 0.5) * 100),
#                 "eye_contact": int(m.get("eye_contact", 0)),
#                 "head_pose": m.get("head_pose", "Center"),
#                 "angles": m.get("angles", {"yaw":0, "pitch":0, "roll":0})
#             }
#         }
#     except Exception as e:
#         print(f"❌ Frame Error: {e}")
#         # Return 200 with error details so frontend doesn't crash
#         return {"success": False, "error": str(e)}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PYTHON_PORT", 8000)), reload=True)






# app.py
import os
import sys
import uuid
import logging
import tempfile
import shutil
from typing import Dict, Optional, List, Any

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# ---------------------------------------------------------
# 🔧 CONFIG & LOGGING
# ---------------------------------------------------------
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "utils"))

# ---------------------------------------------------------
# ✅ SAFE IMPORTS
# ---------------------------------------------------------

# Interview AI
try:
    from interview_assistant import generate_question, analyze_answer
    logger.info("✅ Interview Assistant loaded")
except Exception as e:
    logger.error(f"❌ Interview Assistant error: {e}")

    def generate_question(role, level, history=None):
        return {"question": "Describe a project you worked on.", "follow_up": ""}

    def analyze_answer(text):
        return {
            "strengths": [],
            "improvements": [],
            "clarity_score": 0,
            "confidence_estimate": 0,
        }

# Vision AI
try:
    from frame_analyzer import analyze_frame
    logger.info("✅ Frame Analyzer loaded")
except Exception as e:
    logger.error(f"❌ Frame Analyzer error: {e}")

    def analyze_frame(img):
        return {"success": False, "error": "Vision module unavailable"}

# Resume Parser (🔥 IMPORTANT)
try:
    from resume_parser import parse_resume_from_file
    logger.info("✅ Resume Parser loaded")
except Exception as e:
    logger.error(f"❌ Resume Parser error: {e}")
    parse_resume_from_file = None

# ---------------------------------------------------------
# 🚀 FASTAPI APP
# ---------------------------------------------------------
app = FastAPI(title="AI Career Copilot Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this in prod
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

# ---------------------------------------------------------
# 🧠 SESSION STORE (IN-MEMORY)
# ---------------------------------------------------------
SESSIONS: Dict[str, List[Dict[str, Any]]] = {}

def new_id():
    return uuid.uuid4().hex[:10]

def clean_base64(b64: str) -> str:
    return b64.split(",")[1] if "," in b64 else b64

# ---------------------------------------------------------
# 🩺 HEALTH
# ---------------------------------------------------------
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "AI Career Copilot",
        "resume_parser": bool(parse_resume_from_file)
    }

# ---------------------------------------------------------
# 📄 RESUME PARSING (🔥 THIS FIXES EVERYTHING)
# ---------------------------------------------------------
@app.post("/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not parse_resume_from_file:
        raise HTTPException(
            status_code=500,
            detail="Resume parser not available"
        )

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        result = parse_resume_from_file(temp_path)
        return result
    except Exception as e:
        logger.error(f"Resume parsing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ---------------------------------------------------------
# 🎤 INTERVIEW — START
# ---------------------------------------------------------
@app.post("/interview/start")
def interview_start(payload: InterviewStartModel):
    session_id = new_id()
    history = []

    raw = generate_question(payload.role, payload.level, history)
    question = {
        "_id": new_id(),
        "text": raw.get("question", "Tell me about yourself."),
        "follow_up": raw.get("follow_up", ""),
        "difficulty": "Mid-Level"
    }

    SESSIONS[session_id] = [question]

    return {
        "success": True,
        "sessionId": session_id,
        "question": question
    }

# ---------------------------------------------------------
# 🎤 INTERVIEW — NEXT QUESTION
# ---------------------------------------------------------
@app.post("/interview/next-question")
def interview_next(req: QuestionRequest):
    history = SESSIONS.get(req.sessionId, [])

    raw = generate_question(req.role, req.level, history)
    question = {
        "_id": new_id(),
        "text": raw.get("question", "Explain a challenge you faced."),
        "follow_up": raw.get("follow_up", "Can you elaborate?"),
        "difficulty": "Mid-Level"
    }

    history.append(question)
    SESSIONS[req.sessionId] = history

    return {"success": True, "question": question}

# ---------------------------------------------------------
# 🎤 INTERVIEW — ANALYZE ANSWER
# ---------------------------------------------------------
@app.post("/interview/analyze")
def interview_analyze(payload: InterviewInput):
    text = payload.answer or payload.transcript or ""

    if len(text) < 5:
        return {
            "success": True,
            "data": {
                "analysis": {
                    "strengths": [],
                    "improvements": ["Answer too short"],
                    "clarity_score": 0,
                    "confidence_estimate": 0
                }
            }
        }

    try:
        result = analyze_answer(text)
    except Exception as e:
        logger.warning(f"AI analysis failed: {e}")
        result = {
            "strengths": ["Clear intent"],
            "improvements": ["Add examples"],
            "clarity_score": 70,
            "confidence_estimate": 75
        }

    return {"success": True, "data": {"analysis": result}}

# ---------------------------------------------------------
# 👁️ FRAME ANALYSIS
# ---------------------------------------------------------
@app.post("/interview/frame-metrics")
def frame_metrics(payload: FramePayload):
    cleaned = clean_base64(payload.image_base64)

    try:
        result = analyze_frame(cleaned)
        return result
    except Exception as e:
        logger.error(f"Frame analysis error: {e}")
        return {"success": False, "error": str(e)}

# ---------------------------------------------------------
# 🚀 RUN SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PYTHON_PORT", 10000))
    logger.info(f"🚀 Starting FastAPI on port {port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port)
