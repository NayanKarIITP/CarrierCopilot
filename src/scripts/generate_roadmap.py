# import sys
# import json

# # Define the "Brain"
# ROLE_REQUIREMENTS = {
#     "senior-fullstack": ["System Design", "Docker", "Kubernetes", "CI/CD", "Next.js"],
#     "data-scientist": ["Python", "Pandas", "Scikit-learn", "TensorFlow", "SQL"],
#     "devops": ["AWS", "Terraform", "Linux", "Jenkins", "Ansible"],
#     "ml-engineer": ["PyTorch", "Linear Algebra", "Model Deployment", "NLP"]
# }

# def generate(skills, role):
#     current_skills = [s.lower() for s in skills]
#     # Default to fullstack if role not found
#     required = ROLE_REQUIREMENTS.get(role, ROLE_REQUIREMENTS["senior-fullstack"])
    
#     # Calculate Gaps
#     gaps = [s for s in required if s.lower() not in current_skills]
#     if not gaps: gaps = ["Advanced System Design", "Cloud Architecture"]

#     # Build Roadmap Object
#     roadmap = [
#         {
#             "step": 1,
#             "icon": "✓",
#             "title": "Your Foundation",
#             "subtitle": "Current Strengths",
#             "color": "bg-green-100 dark:bg-green-900",
#             "textColor": "text-green-700 dark:text-green-100",
#             "items": skills if skills else ["No skills provided"],
#             "type": "skills"
#         },
#         {
#             "step": 2,
#             "icon": "⚠",
#             "title": "Skills to Acquire",
#             "subtitle": "Identified Gaps",
#             "color": "bg-amber-100 dark:bg-amber-900",
#             "textColor": "text-amber-700 dark:text-amber-100",
#             "items": gaps,
#             "type": "gaps"
#         },
#         {
#             "step": 3,
#             "icon": "📚",
#             "title": "Recommended Courses",
#             "subtitle": "Learning Resources",
#             "color": "bg-blue-100 dark:bg-blue-900",
#             "textColor": "text-blue-700 dark:text-blue-100",
#             "items": [{"title": f"Master {g}", "platform": "Udemy"} for g in gaps[:3]],
#             "type": "courses"
#         },
#         {
#             "step": 4,
#             "icon": "🔨",
#             "title": "Projects",
#             "subtitle": "Build Experience",
#             "color": "bg-purple-100 dark:bg-purple-900",
#             "textColor": "text-purple-700 dark:text-purple-100",
#             "items": [f"Build a {role} App", f"Integrate {gaps[0] if gaps else 'Tech'}"],
#             "type": "projects"
#         }
#     ]
#     return {"roadmap": roadmap}

# if __name__ == "__main__":
#     try:
#         input_data = json.loads(sys.argv[1])
#         print(json.dumps(generate(input_data.get("skills", []), input_data.get("role", ""))))
#     except Exception as e:
#         print(json.dumps({"roadmap": []}))








import sys
import json
import os
import random

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
    api_key = "AIzaSyCCs3_htORG197m0bz6SeVjqERnlfco5I4"
    # IF ENV FAILS, PASTE KEY HERE FOR TESTING:
    # api_key = "AIzaSy..." 

    if not api_key:
        return get_fallback_roadmap(skills, role)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

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