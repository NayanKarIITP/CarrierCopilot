# src/python/resume_parser.py
import os
import re
import json
import sys
import logging
import requests
import tempfile
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Setup logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='[PARSER] %(message)s')
logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

# 1. MASTER PROMPT
MASTER_PROMPT = """
You are an expert ATS Resume Scanner. Analyze the attached resume PDF.
You MUST return the response in strict JSON format.
DO NOT use Markdown code blocks (```json). Just return the raw JSON.

REQUIRED JSON STRUCTURE:
{
    "full_name": "string",
    "emails": ["string"],
    "phones": ["string"],
    "skills": ["string", "string"],
    "education": [
        { "degree": "string", "institution": "string", "year": "string" }
    ],
    "experience": [
        { "title": "string", "company": "string", "duration": "string", "description": "string" }
    ],
    "projects": [
        { "name": "string", "description": "string" }
    ],
    "resume_score": 85,
    "feedback": ["Advice 1", "Advice 2"],
    "strengths": ["Strength 1", "Strength 2"],
    "weaknesses": ["Weakness 1", "Weakness 2"]
}
"""

# HELPER: CLEAN JSON OUTPUT

def clean_json_text(text: str) -> str:
    """
    Removes Markdown formatting and finds the valid JSON block.
    """
    if not text: return "{}"

    # 1. Remove Markdown code blocks
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text)
    
    # 2. Trim whitespace
    text = text.strip()
    
    # 3. Find the first '{' and last '}' to strip extra text
    start = text.find("{")
    end = text.rfind("}")
    
    if start != -1 and end != -1:
        text = text[start:end+1]
    
    return text

# MAIN PARSER FUNCTION
def parse_resume_from_file(path_or_url: str) -> dict:
    """
    Downloads and analyzes PDF using gemini-flash-latest (Stable).
    """
    if not API_KEY:
        return {"success": False, "error": "Missing GEMINI_API_KEY"}

    temp_path = None
    
    try:
        #  Initialize Client
        client = genai.Client(api_key=API_KEY)
        target_path = path_or_url

        # 1. Download if URL
        if path_or_url.startswith("http"):
            logger.info(f"⬇ Downloading: {path_or_url}")
            try:
                response = requests.get(path_or_url)
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(response.content)
                    target_path = tmp.name
                    temp_path = tmp.name
            except Exception as e:
                return {"success": False, "error": f"Download Failed: {str(e)}"}

        # 2. Upload to Gemini
        logger.info(f" Uploading to Gemini...")
        
        #  NEW: File Upload Syntax
        uploaded_file = client.files.upload(file=target_path, config={'mime_type': 'application/pdf'})
        
        # Wait for processing
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(1)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            return {"success": False, "error": "Gemini failed to process PDF."}

        # 3. Generate Analysis
        logger.info(" Analyzing with Gemini model...")
        
        # NEW: Generation Syntax
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[MASTER_PROMPT, uploaded_file],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # 4. Clean and Parse Result
        if not response.text:
             raise ValueError("Empty response from AI")

        cleaned_text = clean_json_text(response.text)
        
        try:
            ai_data = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            logger.error(f" JSON Parse Error: {e}")
            return {"success": False, "error": "AI returned invalid JSON format."}
        
        # Add success flag
        return {
            "success": True,
            "data": ai_data
        }

    except Exception as e:
        logger.error(f" Error: {str(e)}")
        return {"success": False, "error": str(e)}
    
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

# Fallback for text endpoint
def parse_resume_text(text: str) -> dict:
    return {"error": "Use PDF upload for best results."}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(parse_resume_from_file(sys.argv[1]), indent=2))



