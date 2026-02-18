

import os
import json
import sys
import logging
from dotenv import load_dotenv 
from google import genai
from google.genai import types 

load_dotenv()

# LOGGING HELPER
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

# PROMPT 
ROADMAP_PROMPT = """
Act as a strict Senior Technical Mentor for a University Student.
Create a high-quality, resource-heavy learning roadmap for the role: **{role}**.

User's Background Skills: {skills}

### STRICT CONSTRAINTS (DO NOT BREAK):
1. **DOMAIN ISOLATION:** - If the Target Role is **"Full Stack Developer"**, you must **ONLY** include Web Technologies (React, Node.js, Next.js, SQL, Docker, System Design).
   - **FORBIDDEN TOPICS:** Do NOT include Machine Learning, Data Science, Pandas, NumPy, or Computer Vision. Even if the user knows them, **DROP THEM**. They are irrelevant for this specific roadmap.

2. **RESOURCE DENSITY (CRITICAL):** - The user is a student. For *every single step*, you MUST provide **4 DISTINCT RESOURCES**:
     1. **Video Course:** (e.g., specific YouTube Playlist or FreeCodeCamp link).
     2. **Documentation:** (e.g., React Docs, MDN).
     3. **Project Idea:** A specific small tool to build to practice this step.
     4. **Interactive:** (e.g., LeetCode tag, Odin Project link, or similar).

3. **STEP STRUCTURE:** Generate **8 to 12 steps**. Start from "Core Foundations" (assuming they need a refresh) to "Deployment & DevOps".

### OUTPUT FORMAT (Strict JSON):
{{
    "roadmap": [
        {{
            "step": 1,
            "title": "Web Fundamentals & Advanced JavaScript",
            "description": "Master the DOM, Event Loop, Promises, and ES6+ syntax before touching frameworks.",
            "duration": "2 Weeks",
            "type": "skills",
            "items": ["DOM Manipulation", "Fetch API", "ES6 Modules", "Async/Await"],
            "resources": [
                {{ "title": "Namaste JavaScript (YouTube)", "type": "Video", "link": "https://www.youtube.com/@AkshaySaini" }},
                {{ "title": "MDN Web Docs - JS", "type": "Documentation", "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript" }},
                {{ "title": "Build a Kanban Board", "type": "Project", "link": "#" }},
                {{ "title": "The Odin Project - Foundations", "type": "Interactive", "link": "https://www.theodinproject.com/" }}
            ]
        }}
    ]
}}
"""

# GENERATION LOGIC
def generate_roadmap(arg1, arg2):
    # BULLETPROOF ARGUMENT HANDLING
    # Detect which argument is the Role (string) and which is Skills (list/string)
    if isinstance(arg1, list) or (isinstance(arg1, str) and "," in arg1 and len(arg1) > 50):
        skills = arg1
        target_role = arg2
    else:
        target_role = arg1
        skills = arg2
    
    # Ensure target_role is a string
    if not isinstance(target_role, str):
        target_role = "Software Engineer" # Fallback

    log_debug(f"Generating ISOLATED roadmap for '{target_role}'...")
    
    if not API_KEY:
        return {"error": "API Key missing"}

    try:
        # Pre-process skills
        if isinstance(skills, list):
            # FILTERING MAGIC: If Web Dev, physically remove ML keywords from the list
            if any(x in target_role.lower() for x in ["full stack", "web", "frontend", "backend", "react", "node"]):
                log_debug("⚡️ Web Dev detected: Purging Data Science skills from context...")
                forbidden = ['pandas', 'numpy', 'scikit', 'learn', 'tensor', 'keras', 'pytorch', 'vision', 'opencv', 'mediapipe', 'jupyter']
                skills = [s for s in skills if not any(bad in s.lower() for bad in forbidden)]

            skills_str = ", ".join(skills)
        else:
            skills_str = str(skills)

        client = genai.Client(api_key=API_KEY)

        prompt = ROADMAP_PROMPT.format(role=target_role, skills=skills_str)
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2, # Low temp = Follows instructions strictly
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
            "roadmap": [
                {
                    "step": 1,
                    "title": "Error Generating Roadmap",
                    "description": "Please try again.",
                    "duration": "0 Weeks",
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
            # Manual Test Case
            request = {"skills": ["Python", "Machine Learning"], "role": "Full Stack Developer"} 

        skills = request.get("skills", [])
        role = request.get("role", "Software Engineer")
        
        # Call with (Role, Skills) which is the standard convention
        result = generate_roadmap(role, skills)
        print(json.dumps(result, indent=2))

    except Exception as e:
        log_debug(f"Critical Script Error: {e}")
        print(json.dumps({"error": str(e)}))