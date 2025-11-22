# # app.py (FINAL CLEAN VERSION)

# import sys
# import os
# from dotenv import load_dotenv
# load_dotenv()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)
# sys.path.append(os.path.join(BASE_DIR, "utils"))

# # IMPORTS
# from fastapi import FastAPI, UploadFile, File, HTTPException, Form
# from fastapi.middleware.cors import CORSMiddleware
# from tempfile import NamedTemporaryFile
# import uvicorn
# from pydantic import BaseModel

# # Modules
# from resume_parser import parse_resume_text, parse_resume_file
# from skill_gap_analyzer import analyze_skill_gap
# from roadmap_generator import generate_dynamic_roadmap
# from market_trends import get_dynamic_market_trends
# from interview_assistant import generate_question, analyze_answer
# from interview_assistant import generate_question, analyze_answer



# app = FastAPI(title="AI Career Copilot Microservice")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # MODELS
# class ResumeText(BaseModel):
#     text: str
#     target_role: str = "fullstack-developer"

# class SkillGapInput(BaseModel):
#     resumeSkills: list
#     targetRole: str

# class RoadmapInput(BaseModel):
#     skills: list
#     role: str

# class InterviewInput(BaseModel):
#     question: str = None
#     answer: str = None


# # ------------------------------------------------------
# # RESUME PARSE FROM FILE  (NEW FIXED VERSION)
# # ------------------------------------------------------
# @app.post("/parse-resume")
# async def parse_resume(
#     file: UploadFile = File(...),
#     target_role: str = Form("fullstack-developer")
# ):
#     try:
#         suffix = os.path.splitext(file.filename)[1] or ".pdf"
#         with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             tmp.write(await file.read())
#             temp_path = tmp.name

#         parsed_result = parse_resume_file(temp_path)

#         # Extract skills safely
#         skills = parsed_result.get("parsed", {}).get("skills", [])

#         roadmap = generate_dynamic_roadmap(skills, target_role)

#         return {
#             "success": True,
#             "parsedResume": parsed_result,
#             "generatedRoadmap": roadmap
#         }

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------
# # RESUME PARSE FROM TEXT (CLEANED)
# # ------------------------------------------------------
# @app.post("/parse-resume-text")
# def parse_resume_from_text(payload: ResumeText):
#     try:
#         parsed_result = parse_resume_text(payload.text)

#         # Skills are inside parsed_result["parsed"]["skills"]
#         skills = parsed_result.get("parsed", {}).get("skills", [])

#         roadmap = generate_dynamic_roadmap(skills, payload.target_role)

#         return {
#             "success": True,
#             "parsedResume": parsed_result,
#             "generatedRoadmap": roadmap,
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------
# # SKILL GAP ANALYZER
# # ------------------------------------------------------
# @app.post("/skill-gap")
# def skill_gap(payload: SkillGapInput):
#     try:
#         result = analyze_skill_gap(payload.resumeSkills, payload.targetRole)
#         return {"success": True, "skillGap": result}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------
# # ROADMAP GENERATOR
# # ------------------------------------------------------
# @app.post("/roadmap")
# def roadmap(payload: RoadmapInput):
#     try:
#         result = generate_dynamic_roadmap(payload.skills, payload.role)
#         return {"success": True, "roadmap": result}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------
# # MARKET TRENDS
# # ------------------------------------------------------
# @app.get("/market-trends")
# def trends():
#     try:
#         return {"success": True, "trends": get_dynamic_market_trends()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------
# # INTERVIEW MODULE
# # ------------------------------------------------------
# @app.post("/interview")
# def interview(payload: InterviewInput):
#     try:
#         if payload.answer:
#             analysis = analyze_answer(payload.answer)
#             return {"success": True, "analysis": analysis}

#         question = generate_question(payload.question)
#         return {"success": True, "question": question}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------
# # NEW ROUTE: GET /interview/question
# # ------------------------------------------------------

# @app.get("/interview/question")
# def interview_question():
#     try:
#         question = generate_question(None)
#         return {
#             "success": True,
#             "question": question
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------
# # RUN SERVER
# # ------------------------------------------------------
# if __name__ == "__main__":
#     uvicorn.run(
#         "app:app",
#         host="0.0.0.0",
#         port=int(os.environ.get("PYTHON_PORT", 8000)),
#         reload=True
#     )





















# app.py (FINAL CLEAN VERSION)

import sys
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "utils"))

# IMPORTS
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
import uvicorn
from pydantic import BaseModel

# Modules
from resume_parser import parse_resume_text, parse_resume_file
from skill_gap_analyzer import analyze_skill_gap
from roadmap_generator import generate_dynamic_roadmap
from market_trends import get_dynamic_market_trends
from interview_assistant import generate_question, analyze_answer


app = FastAPI(title="AI Career Copilot Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELS
class ResumeText(BaseModel):
    text: str
    target_role: str = "fullstack-developer"

class SkillGapInput(BaseModel):
    resumeSkills: list
    targetRole: str

class RoadmapInput(BaseModel):
    skills: list
    role: str

class InterviewInput(BaseModel):
    question: str = None
    answer: str = None


# ------------------------------------------------------
# RESUME UPLOAD (FILE)
# ------------------------------------------------------
@app.post("/parse-resume")
async def parse_resume(
    file: UploadFile = File(...),
    target_role: str = Form("fullstack-developer")
):
    try:
        suffix = os.path.splitext(file.filename)[1] or ".pdf"
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        parsed_result = parse_resume_file(temp_path)

        skills = parsed_result.get("parsed", {}).get("skills", [])
        roadmap = generate_dynamic_roadmap(skills, target_role)

        return {
            "success": True,
            "parsedResume": parsed_result,
            "generatedRoadmap": roadmap
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# RESUME PARSE FROM TEXT
# ------------------------------------------------------
@app.post("/parse-resume-text")
def parse_resume_from_text(payload: ResumeText):
    try:
        parsed_result = parse_resume_text(payload.text)
        skills = parsed_result.get("parsed", {}).get("skills", [])
        roadmap = generate_dynamic_roadmap(skills, payload.target_role)

        return {
            "success": True,
            "parsedResume": parsed_result,
            "generatedRoadmap": roadmap,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# SKILL GAP
# ------------------------------------------------------
@app.post("/skill-gap")
def skill_gap(payload: SkillGapInput):
    try:
        result = analyze_skill_gap(payload.resumeSkills, payload.targetRole)
        return {"success": True, "skillGap": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# ROADMAP GENERATOR
# ------------------------------------------------------
@app.post("/roadmap")
def roadmap(payload: RoadmapInput):
    try:
        result = generate_dynamic_roadmap(payload.skills, payload.role)
        return {"success": True, "roadmap": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# MARKET TRENDS
# ------------------------------------------------------
@app.get("/market-trends")
def trends():
    try:
        return {"success": True, "trends": get_dynamic_market_trends()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# INTERVIEW MODULE → POST (answer/question)
# ------------------------------------------------------
@app.post("/interview")
def interview(payload: InterviewInput):
    try:
        if payload.answer:
            analysis = analyze_answer(payload.answer)
            return {"success": True, "analysis": analysis}

        question = generate_question(payload.question)
        return {"success": True, "question": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# GET /interview/question (NO INPUT)
# ------------------------------------------------------
@app.get("/interview/question")
def interview_question():
    try:
        question = generate_question(None)
        return {"success": True, "question": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PYTHON_PORT", 8000)),
        reload=True
    )
