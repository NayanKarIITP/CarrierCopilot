# src/python/skill_gap_analyzer.py
import os
import json
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_skill_gap(current_skills: list, target_role: str) -> dict:
    """
    Uses Gemini to identify missing skills AND assign an importance score.
    """
    if not API_KEY: 
        logger.warning(" API Key missing. Skipping gap analysis.")
        return {"missing_skills": []}
    
    # 1. Update Prompt to ask for scores
    prompt = f"""
    Act as a Technical Recruiter.
    
    Candidate Skills: {', '.join(current_skills)}
    Target Role: "{target_role}"
    
    Identify 3-5 missing technical skills critical for this role.
    For each, assign an "importance" score (1-100) based on market demand.
    
    JSON Structure:
    {{
        "missing_skills": [
            {{ "skill": "Skill Name", "importance": 90 }},
            {{ "skill": "Another Skill", "importance": 75 }}
        ]
    }}
    """
    
    try:
        #  NEW: Initialize Client
        client = genai.Client(api_key=API_KEY)

        #  NEW: Generate with Config
        response = client.models.generate_content(
            model='gemini-flash-latest', # Updated to stable model
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        if not response.text:
            return {"missing_skills": []}

        result = json.loads(response.text)
        gaps = result.get("missing_skills", [])
        
        return {"missing_skills": gaps}

    except Exception as e:
        logger.error(f"Gap Analysis Error: {e}")
        return {"missing_skills": []}
