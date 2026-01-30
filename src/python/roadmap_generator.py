#2nd last working version
# # src/python/roadmap_generator.py
# import os
# import json
# import sys
# import logging
# from dotenv import load_dotenv 
# from google import genai
# from google.genai import types # ✅ Required for strict config

# load_dotenv()

# # ---------------------------------------------------------
# # 🔧 LOGGING HELPER
# # ---------------------------------------------------------
# def log_debug(message: str):
#     """Writes to stderr so it doesn't break the JSON output in stdout."""
#     try:
#         safe_message = message.encode('ascii', 'ignore').decode('ascii')
#         sys.stderr.write(f"[PYTHON LOG] {safe_message}\n")
#         sys.stderr.flush()
#     except Exception:
#         pass

# # ---------------------------------------------------------
# # ⚙️ CONFIGURATION
# # ---------------------------------------------------------
# API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = 'gemini-flash-latest' # ✅ Updated to stable model

# if not API_KEY:
#     log_debug("❌ Error: API Key is missing.")
#     # We don't exit here to allow import checks to pass, 
#     # but actual generation will fail safely below.

# # ---------------------------------------------------------
# # 🧠 AI PROMPT
# # ---------------------------------------------------------
# ROADMAP_PROMPT = """
# Act as a Senior Career Coach. Create a step-by-step learning roadmap for a user wanting to become a "{role}".
# The user already has these skills: {skills}.

# Requirements:
# 1. Compare their current skills with the target role.
# 2. Generate 5 distinct steps to bridge the gap.
# 3. Steps should be: "Foundation", "Skill Gap Fill", "Projects", "Advanced Concepts", "Job Prep".
# 4. For EVERY step, provide specific "resources" (Books, Videos, Courses) that are highly rated.

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "level": "Beginner/Intermediate/Advanced",
#     "roadmap": [
#         {{
#             "step": 1,
#             "title": "Solidify Foundations",
#             "description": "Master the basics of...",
#             "duration": "2 Weeks",
#             "type": "skills",
#             "items": ["React Hooks", "Redux"],
#             "resources": [
#                 {{
#                     "title": "Namaste React by Akshay Saini",
#                     "type": "video"
#                 }},
#                 {{
#                     "title": "You Don't Know JS (Book Series)",
#                     "type": "book"
#                 }}
#             ]
#         }},
#         {{
#             "step": 3,
#             "title": "Build Real World Projects",
#             "description": "Apply your skills...",
#             "duration": "4 Weeks",
#             "type": "projects",
#             "items": ["E-commerce App", "Task Manager"],
#             "resources": [
#                 {{
#                     "title": "Build Netflix Clone with MERN Stack",
#                     "type": "video"
#                 }}
#             ]
#         }}
#     ]
# }}
# """

# # ---------------------------------------------------------
# # 🚀 GENERATION LOGIC
# # ---------------------------------------------------------
# def generate_roadmap(skills, target_role):
#     log_debug(f"Generating roadmap for {target_role}...")
    
#     if not API_KEY:
#         return {"error": "API Key missing"}

#     try:
#         skills_str = ", ".join(skills) if skills else "General Computer Science knowledge"
        
#         # ✅ NEW: Initialize Client
#         client = genai.Client(api_key=API_KEY)

#         prompt = ROADMAP_PROMPT.format(role=target_role, skills=skills_str)
        
#         # ✅ NEW: Generate with Config
#         response = client.models.generate_content(
#             model=MODEL_NAME,
#             contents=prompt,
#             config=types.GenerateContentConfig(
#                 temperature=0.4,
#                 response_mime_type="application/json" # ✅ Forces JSON
#             )
#         )
        
#         # Clean response
#         if not response.text:
#             raise ValueError("Empty response from AI")

#         raw_text = response.text.replace("```json", "").replace("```", "").strip()
        
#         # Parse JSON
#         data = json.loads(raw_text)
#         return data

#     except Exception as e:
#         log_debug(f"Generation Failed: {e}")
#         return {
#             "level": "Error",
#             "roadmap": [
#                 {
#                     "step": 1,
#                     "title": "Service Unavailable",
#                     "description": "Could not generate roadmap at this time.",
#                     "type": "error",
#                     "resources": []
#                 }
#             ]
#         }

# # ---------------------------------------------------------
# # 🏁 MAIN EXECUTION
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     if sys.platform == "win32":
#         sys.stdout.reconfigure(encoding='utf-8')

#     try:
#         # Read from stdin if available (for Node.js integration)
#         if not sys.stdin.isatty():
#             input_data = sys.stdin.read()
#             if input_data:
#                 request = json.loads(input_data)
#             else:
#                  request = {"skills": [], "role": "Software Engineer"}
#         else:
#             # Default test case
#             request = {"skills": ["JavaScript"], "role": "Full Stack Developer"}

#         skills = request.get("skills", [])
#         role = request.get("role", "Software Engineer")
        
#         # Handle case where skills might be a comma-string
#         if isinstance(skills, str):
#             skills = [s.strip() for s in skills.split(',')]

#         result = generate_roadmap(skills, role)
#         print(json.dumps(result, indent=2))

#     except Exception as e:
#         log_debug(f"Critical Script Error: {e}")
#         print(json.dumps({"error": str(e)}))








import os
import json
import sys
import logging
from dotenv import load_dotenv 
from google import genai
from google.genai import types 

load_dotenv()

# ---------------------------------------------------------
# 🔧 LOGGING HELPER
# ---------------------------------------------------------
def log_debug(message: str):
    try:
        safe_message = message.encode('ascii', 'ignore').decode('ascii')
        sys.stderr.write(f"[PYTHON LOG] {safe_message}\n")
        sys.stderr.flush()
    except Exception:
        pass

# ---------------------------------------------------------
# ⚙️ CONFIGURATION
# ---------------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = 'gemini-flash-latest' # ✅ Specific stable version is safer than 'latest'

# ---------------------------------------------------------
# 🧠 AI PROMPT (UPDATED FOR ACCURACY)
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 🚀 GENERATION LOGIC
# ---------------------------------------------------------
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
                temperature=0.3, # ⬇️ Lower temp = Less hallucination, more strict
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

# ---------------------------------------------------------
# 🏁 MAIN EXECUTION
# ---------------------------------------------------------
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





#FINAL WORKING
# #roadmap_generator.py>>
# import os
# import json
# import sys
# import google.generativeai as genai
# from dotenv import load_dotenv 

# load_dotenv()

# # ---------------------------------------------------------
# # 🔧 LOGGING HELPER
# # ---------------------------------------------------------
# def log_debug(message: str):
#     """Writes to stderr so it doesn't break the JSON output in stdout."""
#     try:
#         safe_message = message.encode('ascii', 'ignore').decode('ascii')
#         sys.stderr.write(f"[PYTHON LOG] {safe_message}\n")
#         sys.stderr.flush()
#     except Exception:
#         pass

# # ---------------------------------------------------------
# # ⚙️ CONFIGURATION
# # ---------------------------------------------------------
# API_KEY = os.getenv("GEMINI_API_KEY")

# if not API_KEY:
#     log_debug("❌ Error: API Key is missing.")
#     print(json.dumps({"error": "API Key missing"}))
#     sys.exit(1)

# try:
#     genai.configure(api_key=API_KEY)
# except Exception as e:
#     log_debug(f"❌ Config Error: {e}")

# MODEL_NAME = 'gemini-flash-latest' # Ensure using a valid model name

# # ---------------------------------------------------------
# # 🧠 AI PROMPT (UPDATED FOR DYNAMIC RESOURCES)
# # ---------------------------------------------------------
# ROADMAP_PROMPT = """
# Act as a Senior Career Coach. Create a step-by-step learning roadmap for a user wanting to become a "{role}".
# The user already has these skills: {skills}.

# Requirements:
# 1. Compare their current skills with the target role.
# 2. Generate 5 distinct steps to bridge the gap.
# 3. Steps should be: "Foundation", "Skill Gap Fill", "Projects", "Advanced Concepts", "Job Prep".
# 4. For EVERY step, provide specific "resources" (Books, Videos, Courses) that are highly rated.

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "level": "Beginner/Intermediate/Advanced",
#     "roadmap": [
#         {{
#             "step": 1,
#             "title": "Solidify Foundations",
#             "description": "Master the basics of...",
#             "duration": "2 Weeks",
#             "type": "skills",
#             "items": ["React Hooks", "Redux"],
#             "resources": [
#                 {{
#                     "title": "Namaste React by Akshay Saini",
#                     "type": "video"
#                 }},
#                 {{
#                     "title": "You Don't Know JS (Book Series)",
#                     "type": "book"
#                 }},
#                 {{
#                     "title": "Official Redux Documentation",
#                     "type": "article"
#                 }}
#             ]
#         }},
#         {{
#             "step": 3,
#             "title": "Build Real World Projects",
#             "description": "Apply your skills...",
#             "duration": "4 Weeks",
#             "type": "projects",
#             "items": ["E-commerce App", "Task Manager"],
#             "resources": [
#                 {{
#                     "title": "Build Netflix Clone with MERN Stack",
#                     "type": "video"
#                 }},
#                 {{
#                     "title": "Full Stack Open (University of Helsinki)",
#                     "type": "course"
#                 }}
#             ]
#         }}
#     ]
# }}
# """

# # ---------------------------------------------------------
# # 🚀 GENERATION LOGIC
# # ---------------------------------------------------------
# def generate_roadmap(skills, target_role):
#     log_debug(f"Generating roadmap for {target_role}...")
    
#     try:
#         skills_str = ", ".join(skills) if skills else "General Computer Science knowledge"
        
#         model = genai.GenerativeModel(MODEL_NAME)
#         prompt = ROADMAP_PROMPT.format(role=target_role, skills=skills_str)
        
#         response = model.generate_content(prompt)
        
#         # Clean response
#         raw_text = response.text.replace("```json", "").replace("```", "").strip()
        
#         # Parse JSON
#         data = json.loads(raw_text)
#         return data

#     except Exception as e:
#         log_debug(f"Generation Failed: {e}")
#         return {
#             "level": "Error",
#             "roadmap": [
#                 {
#                     "step": 1,
#                     "title": "Service Unavailable",
#                     "description": "Could not generate roadmap at this time.",
#                     "type": "error",
#                     "resources": []
#                 }
#             ]
#         }

# # ---------------------------------------------------------
# # 🏁 MAIN EXECUTION
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     if sys.platform == "win32":
#         sys.stdout.reconfigure(encoding='utf-8')

#     try:
#         input_data = sys.stdin.read()
        
#         if not input_data:
#             request = {"skills": ["JavaScript"], "role": "Full Stack Developer"}
#         else:
#             request = json.loads(input_data)

#         skills = request.get("skills", [])
#         role = request.get("role", "Software Engineer")

#         result = generate_roadmap(skills, role)
#         print(json.dumps(result, indent=2))

#     except Exception as e:
#         log_debug(f"Critical Script Error: {e}")
#         print(json.dumps({"error": str(e)}))