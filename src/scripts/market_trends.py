# import json
# import random
# import sys

# # 1. Try to import the AI library
# try:
#     import google.generativeai as genai
#     AI_AVAILABLE = True
# except ImportError:
#     # If missing, we will just use simulation mode
#     AI_AVAILABLE = False
#     # Optional: Print warning to stderr (Node.js logs this)
#     # print("Warning: google-generativeai not found. Using simulation.", file=sys.stderr)

# def get_simulated_data():
#     """Returns realistic fake data so the app always works."""
#     return {
#         "skills": [
#             {"skill": "React", "demand": random.randint(85, 99)},
#             {"skill": "Python", "demand": random.randint(80, 95)},
#             {"skill": "AWS", "demand": random.randint(75, 92)},
#             {"skill": "Docker", "demand": random.randint(70, 88)},
#             {"skill": "Next.js", "demand": random.randint(82, 96)}
#         ],
#         "trends": [
#             {"month": "Jan", "hiring": 120, "salaries": 160},
#             {"month": "Feb", "hiring": 135, "salaries": 162},
#             {"month": "Mar", "hiring": 150, "salaries": 165},
#             {"month": "Apr", "hiring": 140, "salaries": 164},
#             {"month": "May", "hiring": 165, "salaries": 168},
#             {"month": "Jun", "hiring": 180, "salaries": 172}
#         ],
#         "salaries": [
#             {"role": "Junior Dev", "salary": 85},
#             {"role": "Mid-Level", "salary": 135},
#             {"role": "Senior Dev", "salary": 175},
#             {"role": "Tech Lead", "salary": 210},
#             {"role": "Manager", "salary": 230}
#         ],
#         "insights": {
#             "growing_market": "+18% (Simulated)",
#             "ai_opportunity": "+60% (Simulated)",
#             "remote_jobs": "58% (Simulated)",
#             "salary_growth": "+9% YoY"
#         }
#     }

# def get_market_trends():
#     # If library is missing, return simulation immediately
#     if not AI_AVAILABLE:
#         return get_simulated_data()

#     # If you have the library, try to use it
#     try:
#         # P.S. Ensure you set your API KEY in your environment or hardcode it for testing
#         # genai.configure(api_key="YOUR_KEY_HERE")
#         # ... AI Logic ...
#         # If AI fails, just return simulation:
#         return get_simulated_data()
#     except Exception:
#         return get_simulated_data()

# if __name__ == "__main__":
#     # Always print valid JSON to stdout
#     print(json.dumps(get_market_trends()))








# import json
# import random
# import sys
# import os

# # 1. SETUP: Try to import the AI Library
# try:
#     import google.generativeai as genai
#     AI_AVAILABLE = True
# except ImportError:
#     AI_AVAILABLE = False

# # 2. THE BACKUP PLAN (Hardcoded - Only runs if AI fails)
# def get_simulated_data():
#     return {
#         "skills": [
#             {"skill": "React (Backup)", "demand": 80},
#             {"skill": "Python (Backup)", "demand": 80}
#         ],
#         "trends": [],
#         "salaries": [],
#         "insights": {
#             "growing_market": "N/A - Check API",
#             "ai_opportunity": "N/A", 
#             "remote_jobs": "N/A", 
#             "salary_growth": "N/A"
#         }
#     }

# # 3. THE REAL WORLD LOGIC (Dynamic)
# def get_market_trends():
#     # A. Check for Library
#     if not AI_AVAILABLE:
#         # Debug print to see WHY it failed
#         # print("ERROR: Google AI Library not found.", file=sys.stderr)
#         return get_simulated_data()

#     # B. Check for API Key
#     # Paste your key here temporarily to GUARANTEE it works
#     api_key = os.getenv("GEMINI_API_KEY") or "PASTE_YOUR_API_KEY_HERE"
    
#     if not api_key or "PASTE" in api_key:
#         return get_simulated_data()

#     try:
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel('gemini-1.5-flash')
        
#         # C. THE REAL WORLD PROMPT
#         # We ask the AI to browse its knowledge for CURRENT booming tech
#         prompt = """
#         Act as a Senior Tech Market Analyst in 2025. 
#         Analyze the current job market and identify the top 6 "Booming" technologies (e.g., GenAI, Rust, Kubernetes, MLOps).
        
#         Return a STRICT JSON object with no markdown:
#         {
#             "skills": [
#                 {"skill": "Name of Booming Tech", "demand": <Score 80-100>}
#             ],
#             "trends": [
#                 {"month": "Jan", "hiring": <Index 100-200>, "salaries": <Index 140-180>},
#                 {"month": "Feb", "hiring": <Index>, "salaries": <Index>},
#                 {"month": "Mar", "hiring": <Index>, "salaries": <Index>},
#                 {"month": "Apr", "hiring": <Index>, "salaries": <Index>},
#                 {"month": "May", "hiring": <Index>, "salaries": <Index>},
#                 {"month": "Jun", "hiring": <Index>, "salaries": <Index>}
#             ],
#             "salaries": [
#                 {"role": "Junior Engineer", "salary": <Real Market Rate k$>},
#                 {"role": "Senior Engineer", "salary": <Real Market Rate k$>},
#                 {"role": "AI Engineer", "salary": <Real Market Rate k$>},
#                 {"role": "DevOps Lead", "salary": <Real Market Rate k$>},
#                 {"role": "Engineering Manager", "salary": <Real Market Rate k$>}
#             ],
#             "insights": {
#                 "growing_market": "<Real Growth % (e.g. +22%)>",
#                 "ai_opportunity": "<Real Demand % (e.g. +65%)>",
#                 "remote_jobs": "<Real % (e.g. 45%)>",
#                 "salary_growth": "<Real % (e.g. +8% YoY)>"
#             }
#         }
#         """
        
#         response = model.generate_content(prompt)
#         text_response = response.text.replace("```json", "").replace("```", "").strip()
#         return json.loads(text_response)

#     except Exception as e:
#         # print(f"API ERROR: {e}", file=sys.stderr)
#         return get_simulated_data()

# if __name__ == "__main__":
#     print(json.dumps(get_market_trends()))







import json
import os
import sys
from dotenv import load_dotenv 

load_dotenv()

# 1. SETUP: Try to import the AI Library
try:
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    # This print will show up in your Node.js logs if it fails
    print("ERROR: 'google-generativeai' library not found!", file=sys.stderr)

# 2. THE REAL WORLD LOGIC
def get_market_trends():
    # A. Validation
    if not AI_AVAILABLE:
        return get_fallback_data()

    # B. Auth
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        print("ERROR: API Key is missing.", file=sys.stderr)
        return get_fallback_data()

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # C. PROMPT FOR REAL DATA (Optimized for Charts)
        prompt = """
        Act as a Senior Tech Recruiter in 2025.
        Provide a JSON object with REAL-WORLD stats for:
        1. Top 6 booming tech skills (e.g. Agentic AI, Rust).
        2. Monthly hiring trends (Index 100-200).
        3. Real salary stats for Software Engineers.
        4. Market insights.

        IMPORTANT: For 'salaries', return the 'average' salary as a generic INTEGER number (in thousands). 
        Example: instead of "$100k-$120k", return 110.

        Strictly follow this JSON structure (no markdown):
        {
            "skills": [{"skill": "Name", "demand": 0-100}],
            "trends": [{"month": "Jan", "hiring": 0, "salaries": 0}],
            "salaries": [{"role": "Junior", "salary": 110}], 
            "insights": {"growing_market": "+X%", "ai_opportunity": "+X%", "remote_jobs": "X%", "salary_growth": "+X%"}
        }
        """
        
        response = model.generate_content(prompt)
        text_response = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text_response)

    except Exception as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        return get_fallback_data()

# 3. FALLBACK (Only runs if the above fails)
def get_fallback_data():
    return {
        "skills": [{"skill": "Python (Backup)", "demand": 50}],
        "trends": [], 
        "salaries": [],
        "insights": {
            "growing_market": "N/A", "ai_opportunity": "N/A", 
            "remote_jobs": "N/A", "salary_growth": "N/A"
        }
    }

if __name__ == "__main__":
    print(json.dumps(get_market_trends()))