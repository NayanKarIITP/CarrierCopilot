
import sys
import json
import os
import random
from dotenv import load_dotenv 

load_dotenv()

# 1. Try Imports
try:
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# 2. Safety Fallback (Runs if API fails)
def get_fallback_roadmap(skills, role):
    # Simple logic: If user has very few skills, assume Beginner
    level = "Beginner"
    if len(skills) > 5: level = "Intermediate"
    if len(skills) > 10: level = "Advanced"

    return {
        "roadmap": [
            {
                "step": 1,
                "title": "Foundation Check",
                "description": f"Reviewing your current {len(skills)} skills",
                "type": "skills",
                "items": skills if skills else ["No resume skills found"]
            },
            {
                "step": 2,
                "title": "Core Gaps",
                "description": f"Essential skills missing for {role}",
                "type": "gaps",
                "items": ["System Design", "Cloud Basics", "API Development"]
            },
            {
                "step": 3,
                "title": "Recommended Learning",
                "description": "Bridge the gap",
                "type": "courses",
                "items": [{"title": f"{role} Masterclass", "platform": "Udemy"}]
            }
        ],
        "level": level # <--- Dynamic Fallback Level
    }

# 3. The AI Logic (Real World)
def generate_real_roadmap(skills, role):
    # A. Check Library
    if not AI_AVAILABLE:
        return get_fallback_roadmap(skills, role)

    # B. Auth
    api_key=os.getenv("GEMINI_API_KEY")

    if not api_key:
        return get_fallback_roadmap(skills, role)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')

        # C. The Smart Prompt
        prompt = f"""
        Act as a Senior Career Coach.
        
        1. ANALYZE USER:
        - Current Skills (from Resume): {json.dumps(skills)}
        - Target Role: {role}
        
        2. DETERMINE LEVEL:
        Compare their current skills vs the industry requirements for {role}.
        - If they lack basics -> "Beginner"
        - If they have basics but lack specialized tools -> "Intermediate"
        - If they match most requirements -> "Advanced"

        3. CREATE ROADMAP:
        Generate a 5-step roadmap specifically to bridge their specific gaps.

        Strictly follow this JSON structure (NO MARKDOWN):
        {{
            "level": "Beginner/Intermediate/Advanced", 
            "roadmap": [
                {{
                    "step": 1,
                    "title": "Current Strengths",
                    "description": "Skills you already have for this role",
                    "type": "skills",
                    "items": {json.dumps(skills)}
                }},
                {{
                    "step": 2,
                    "title": "Critical Gaps",
                    "description": "What you are missing",
                    "type": "gaps",
                    "items": ["Gap 1", "Gap 2", "Gap 3"] 
                }},
                {{
                    "step": 3,
                    "title": "Learning Path",
                    "description": "Courses to take",
                    "type": "courses",
                    "items": [
                        {{"title": "Specific Course Name", "platform": "Udemy/Coursera"}},
                        {{"title": "Specific Course Name", "platform": "YouTube"}}
                    ]
                }},
                {{
                    "step": 4,
                    "title": "Build Projects",
                    "description": "Apply your knowledge",
                    "type": "projects",
                    "items": [
                        {{"title": "Project Name", "description": "What to build"}}
                    ]
                }},
                {{
                    "step": 5,
                    "title": "Apply for Jobs",
                    "description": "Roles matching your new profile",
                    "type": "roles",
                    "items": [
                        {{"title": "{role}", "company": "Tech Corp", "match": "Predicted Match %"}}
                    ]
                }}
            ]
        }}
        """

        response = model.generate_content(prompt)
        text_response = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text_response)

    except Exception as e:
        return get_fallback_roadmap(skills, role)

if __name__ == "__main__":
    try:
        # Read input from Node.js
        input_data = json.loads(sys.argv[1])
        skills_in = input_data.get("skills", [])
        role_in = input_data.get("role", "Software Engineer")
        
        # Generate
        result = generate_real_roadmap(skills_in, role_in)
        
        # Print JSON for Node.js
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps(get_fallback_roadmap([], "Developer")))