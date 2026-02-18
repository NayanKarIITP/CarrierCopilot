# src/python/roadmap_generator.py


import os
import json
import sys
import logging
from dotenv import load_dotenv 
from google import genai
from google.genai import types 

load_dotenv()

#  LOGGING HELPER
def log_debug(message: str):
    try:
        safe_message = message.encode('ascii', 'ignore').decode('ascii')
        sys.stderr.write(f"[PYTHON LOG] {safe_message}\n")
        sys.stderr.flush()
    except Exception:
        pass

# CONFIGURATION
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = 'gemini-flash-latest' 

# AI PROMPT 
ROADMAP_PROMPT = """
Act as a strict Senior Career Coach. Create a step-by-step learning roadmap for a user wanting to become a: **{role}**.

The user's CURRENT skills are: {skills}.

CRITICAL INSTRUCTIONS:
1. **Target Role Priority:** Your ONLY goal is to make them a {role}. 
2. **Ignore Irrelevant Skills:** If the user knows "HTML/CSS" but wants to be a "Data Scientist", IGNORE the HTML. Do not try to combine them. Start from scratch with Python/Math if needed.
3. **Gap Analysis:** Only use their current skills if they strictly help with the {role}.
4. **Structure:** Generate exactly 5 distinct steps: "Foundation", "Skill Gap Fill", "Real World Projects", "Advanced Specialization", "Job Preparation".

OUTPUT FORMAT (Strict JSON, No Markdown):
{{
    "level": "Beginner/Intermediate/Advanced",
    "roadmap": [
        {{
            "step": 1,
            "title": "Solidify Foundations",
            "description": "Master the core basics required for {role}...",
            "duration": "2 Weeks",
            "type": "skills",
            "items": ["Skill A", "Skill B"],
            "resources": [
                {{
                    "title": "Top Rated Book/Course Name",
                    "type": "course"
                }}
            ]
        }}
    ]
}}
"""

# GENERATION LOGIC
def generate_roadmap(skills, target_role):
    log_debug(f"Generating roadmap for {target_role}...")
    
    if not API_KEY:
        return {"error": "API Key missing"}

    try:
        skills_str = ", ".join(skills) if skills else "No prior experience"
        
        client = genai.Client(api_key=API_KEY)

        prompt = ROADMAP_PROMPT.format(role=target_role, skills=skills_str)
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3, #  Lower temp = Less hallucination, more strict
                response_mime_type="application/json"
            )
        )
        
        if not response.text:
            raise ValueError("Empty response from AI")

        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_text)

    except Exception as e:
        log_debug(f"Generation Failed: {e}")
        return {
            "level": "Error",
            "roadmap": [
                {
                    "step": 1,
                    "title": "AI Busy",
                    "description": "Could not generate roadmap. Please try again.",
                    "type": "error",
                    "resources": []
                }
            ]
        }

# MAIN EXECUTION
if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    try:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            if input_data:
                request = json.loads(input_data)
            else:
                request = {"skills": [], "role": "Full Stack Developer"}
        else:
            request = {"skills": ["HTML", "CSS"], "role": "Data Scientist"} # Test case

        skills = request.get("skills", [])
        role = request.get("role", "Software Engineer")
        
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',')]

        result = generate_roadmap(skills, role)
        print(json.dumps(result, indent=2))

    except Exception as e:
        log_debug(f"Critical Script Error: {e}")
        print(json.dumps({"error": str(e)}))
