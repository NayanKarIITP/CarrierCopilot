
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