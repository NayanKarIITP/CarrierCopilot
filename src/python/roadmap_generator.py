# # roadmap_generator.py
# from llm_engine import parse_with_llm
# from typing import Dict, Any
# import json

# # ---------------------------------------------------------
# # PROMPT TEMPLATE
# # ---------------------------------------------------------

# ROADMAP_PROMPT = """
# You are an AI assistant that generates a 4-step personalized learning roadmap.
# Input: a JSON containing user's skills, projects, education, experience, and the target role.

# Output JSON format:
# {
#   "steps": [
#     { "title": "", "subtitle": "", "items": [] },
#     ...
#   ]
# }

# Return JSON ONLY. No explanation text.
# """

# # ---------------------------------------------------------
# # MAIN FUNCTION (expected by FastAPI)
# # ---------------------------------------------------------

# def generate_dynamic_roadmap(skills, role: str):
#     """
#     FastAPI expects this function.
#     skills → list
#     role → string
#     """

#     summary = {
#         "skills": skills,
#         "target_role": role
#     }

#     prompt = ROADMAP_PROMPT + "\nUser Summary:\n" + str(summary)

#     try:
#         raw_output = parse_with_llm(prompt)

#         # Try parse JSON output
#         return json.loads(raw_output)

#     except Exception:
#         # fallback roadmap if HF fails
#         return {
#             "steps": [
#                 {
#                     "title": "Your Foundation",
#                     "subtitle": "Current Strengths",
#                     "items": skills[:5]
#                 },
#                 {
#                     "title": "Skills to Acquire",
#                     "subtitle": f"Skills needed for {role}",
#                     "items": ["Docker", "Kubernetes", "System Design", "GraphQL"]
#                 },
#                 {
#                     "title": "Recommended Courses",
#                     "subtitle": "Best Learning Resources",
#                     "items": [
#                         {"title": "Docker Mastery", "platform": "Udemy"},
#                         {"title": "Kubernetes for Developers", "platform": "Coursera"},
#                     ]
#                 },
#                 {
#                     "title": "Recommended Projects",
#                     "subtitle": "Build Hands-On Experience",
#                     "items": [
#                         "Deploy a microservices system on Kubernetes",
#                         "Build GraphQL real-time API with subscriptions"
#                     ]
#                 }
#             ]
#         }













# # roadmap_generator.py (FINAL CLEAN VERSION)

# from typing import List, Dict
# from llm_engine import parse_with_llm

# # -----------------------------------------------
# # Templates
# # -----------------------------------------------
# ROADMAP_PROMPT = """
# You are an expert career mentor.

# Create a **step-by-step learning roadmap** for someone aiming to become a **{role}**.

# Their current skills:
# {skills}

# Roadmap Requirements:
# - Break steps into Beginner → Intermediate → Advanced.
# - Each step should have: title, description, duration estimate, resources.
# - Keep steps practical and easy to follow.
# - Return JSON ONLY in this exact structure:

# {
#   "beginner": [
#     {"step": "string", "description": "string", "duration": "string", "resources": ["link1", "link2"] }
#   ],
#   "intermediate": [
#     ...
#   ],
#   "advanced": [
#     ...
#   ]
# }
# """

# # -----------------------------------------------
# # Safe LLM Wrapper
# # -----------------------------------------------
# def call_llm(prompt: str) -> Dict:
#     """
#     Safely calls the LLM.
#     If LLM fails / returns bad JSON -> fallback roadmap is returned.
#     """
#     try:
#         result = parse_with_llm(prompt)
#         return eval_json(result)
#     except Exception:
#         # fallback minimal roadmap
#         return {
#             "beginner": [
#                 {
#                     "step": "Fundamentals",
#                     "description": "Learn core programming and basic tools.",
#                     "duration": "1–2 weeks",
#                     "resources": ["https://www.freecodecamp.org"]
#                 }
#             ],
#             "intermediate": [
#                 {
#                     "step": "Build Projects",
#                     "description": "Create 2–3 practical projects.",
#                     "duration": "2–4 weeks",
#                     "resources": ["https://roadmap.sh"]
#                 }
#             ],
#             "advanced": [
#                 {
#                     "step": "System Design",
#                     "description": "Learn system design and architecture.",
#                     "duration": "2–3 weeks",
#                     "resources": ["https://github.com/donnemartin/system-design-primer"]
#                 }
#             ]
#         }

# # -----------------------------------------------
# # JSON Parser Helper (never crashes)
# # -----------------------------------------------
# import json

# def eval_json(raw: str):
#     """
#     Attempts to cleanly parse JSON from LLM response.
#     Extracts JSON substring if required.
#     Never crashes.
#     """
#     try:
#         return json.loads(raw)
#     except:
#         # Attempt to extract JSON substring
#         import re
#         match = re.search(r"{.*}", raw, re.DOTALL)
#         if match:
#             try:
#                 return json.loads(match.group())
#             except:
#                 pass
#     # Final fallback
#     return {}

# # -----------------------------------------------
# # MAIN FUNCTION
# # -----------------------------------------------
# def generate_dynamic_roadmap(skills: List[str], role: str) -> Dict:
#     """
#     Generates an LLM-based roadmap.
#     Always returns a clean structure with beginner/intermediate/advanced.
#     """

#     # Normalize inputs
#     skills = skills or []
#     role = role or "Software Engineer"

#     prompt = ROADMAP_PROMPT.format(
#         role=role,
#         skills=", ".join(skills) if skills else "No skills provided"
#     )

#     response = call_llm(prompt)

#     # Ensure complete structure
#     roadmap = {
#         "beginner": response.get("beginner", []),
#         "intermediate": response.get("intermediate", []),
#         "advanced": response.get("advanced", [])
#     }

#     # Auto-fill if any category is empty
#     default_step = {
#         "step": "Learning Step",
#         "description": "Learn core concepts.",
#         "duration": "1 week",
#         "resources": []
#     }

#     if not roadmap["beginner"]:
#         roadmap["beginner"] = [default_step]

#     if not roadmap["intermediate"]:
#         roadmap["intermediate"] = [default_step]

#     if not roadmap["advanced"]:
#         roadmap["advanced"] = [default_step]

#     return roadmap

# # For FastAPI compatibility
# generate_roadmap = generate_dynamic_roadmap

# # Debug example
# if __name__ == "__main__":
#     print(generate_dynamic_roadmap(["React", "Node.js"], "Fullstack Developer"))













# python/roadmap_generator.py
from llm_engine import parse_with_llm
import json

# ---------------------------------------------------------
# HELPER: DETERMINE LEVEL
# ---------------------------------------------------------
def calculate_level(user_skills, target_role):
    # Define keywords for simple matching
    role_keywords = {
        "senior": ["system design", "architecture", "scaling", "leadership", "kubernetes", "cloud patterns"],
        "data": ["python", "sql", "pandas", "numpy", "statistics", "machine learning"],
        "devops": ["docker", "kubernetes", "aws", "ci/cd", "linux", "terraform"],
        "frontend": ["react", "javascript", "css", "html", "redux", "typescript"],
        "backend": ["node", "python", "java", "database", "api", "sql"]
    }
    
    # Normalize
    role_lower = target_role.lower()
    skills_lower = [s.lower() for s in user_skills]
    
    # Find relevant keyword set
    relevant_keywords = []
    for key, words in role_keywords.items():
        if key in role_lower:
            relevant_keywords.extend(words)
            
    # Default to generic tech if no specific match
    if not relevant_keywords:
        relevant_keywords = ["git", "coding", "algorithms", "database"]
        
    # Calculate match
    matches = sum(1 for k in relevant_keywords if any(k in s for s in skills_lower))
    total_criteria = len(relevant_keywords)
    
    score = matches / total_criteria if total_criteria > 0 else 0

    if score < 0.3: return "Beginner"
    if score < 0.7: return "Intermediate"
    return "Advanced"

# ---------------------------------------------------------
# PROMPT TEMPLATE
# ---------------------------------------------------------
ROADMAP_PROMPT = """
You are an expert Career Coach AI. 
The user is currently at a **{level}** level based on their resume.
Target Role: "{target_role}"
Current Skills: {skills}

Generate a 5-step personalized learning roadmap JSON to help them reach the target role.
Since they are {level}, ensure the recommendations are appropriate (e.g., if Beginner, suggest fundamentals; if Advanced, suggest System Design/Architecture).

The output MUST be a valid JSON object with:
1. "level": "{level}"
2. "roadmap": A list of 5 steps.

Each step items must have: "title", and optionally "link" (URL).
Structure:
1. "Your Foundation" (type: "skills")
2. "Skills to Acquire" (type: "gaps")
3. "Recommended Courses" (type: "courses") 
4. "Recommended Projects" (type: "projects")
5. "Trending Roles to Target" (type: "roles")

Return ONLY JSON. No text.
"""

def generate_dynamic_roadmap(skills, role: str):
    # 1. Calculate Level based on Resume/Skills
    level = calculate_level(skills, role)
    
    formatted_prompt = ROADMAP_PROMPT.format(
        target_role=role,
        skills=", ".join(skills) if skills else "General Tech Interest",
        level=level
    )

    try:
        raw_output = parse_with_llm(formatted_prompt)
        parsed = json.loads(raw_output)
        
        # Ensure structure
        if "roadmap" not in parsed:
            if isinstance(parsed, list): parsed = {"roadmap": parsed}
            else: raise ValueError("Invalid JSON structure")
            
        # Inject level if missing
        if "level" not in parsed: parsed["level"] = level
            
        return parsed

    except Exception as e:
        print(f"LLM Roadmap Gen failed ({e}), using rich fallback logic.")
        
        # -----------------------------------------------------
        # RICH FALLBACK LOGIC (Level-Based)
        # -----------------------------------------------------
        
        role_lower = role.lower()
        
        # DEFAULT: Full Stack
        gaps = ["Docker", "Kubernetes", "System Design"]
        courses = [
            {"title": "Docker for Beginners", "platform": "YouTube", "link": "https://www.youtube.com/watch?v=fqMOX6JJhGo"},
            {"title": "Kubernetes Mastery", "platform": "Udemy", "link": "https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/"}
        ]
        
        # ADJUST BASED ON LEVEL
        if level == "Beginner":
            gaps = ["JavaScript Advanced", "React Basics", "API Integration"]
            courses = [
                {"title": "The Web Developer Bootcamp", "platform": "Udemy", "link": "https://www.udemy.com/course/the-web-developer-bootcamp/"},
                {"title": "JavaScript Crash Course", "platform": "YouTube", "link": "https://www.youtube.com/watch?v=hdI2bqOjy3c"}
            ]
        elif level == "Advanced":
            gaps = ["Microservices Patterns", "High Availability", "Cloud Architecture"]
            courses = [
                {"title": "System Design Primer", "platform": "GitHub", "link": "https://github.com/donnemartin/system-design-primer"},
                {"title": "Advanced Kubernetes", "platform": "Udemy", "link": "https://www.udemy.com/course/advanced-kubernetes/"}
            ]

        # Role Specific Overrides
        if "data" in role_lower:
            gaps = ["Machine Learning", "Deep Learning", "MLOps"] if level == "Advanced" else ["Python", "SQL", "Pandas"]
        
        return {
            "level": level,
            "roadmap": [
                {
                    "step": 1,
                    "icon": "✓",
                    "title": "Your Foundation",
                    "subtitle": f"Current {level} Level Strengths",
                    "color": "bg-green-100 dark:bg-green-900",
                    "textColor": "text-green-700 dark:text-green-100",
                    "items": skills[:5] if skills else ["Programming Basics"],
                    "type": "skills",
                },
                {
                    "step": 2,
                    "icon": "⚠",
                    "title": "Skills to Acquire",
                    "subtitle": "Identified Gaps",
                    "color": "bg-amber-100 dark:bg-amber-900",
                    "textColor": "text-amber-700 dark:text-amber-100",
                    "items": [{"name": g, "link": f"https://www.youtube.com/results?search_query={g}+tutorial"} for g in gaps],
                    "type": "gaps",
                },
                {
                    "step": 3,
                    "icon": "📚",
                    "title": "Recommended Courses",
                    "subtitle": f"Best for {level}s",
                    "color": "bg-blue-100 dark:bg-blue-900",
                    "textColor": "text-blue-700 dark:text-blue-100",
                    "items": courses,
                    "type": "courses",
                },
                {
                    "step": 4,
                    "icon": "🔨",
                    "title": "Recommended Projects",
                    "subtitle": "Build Experience",
                    "color": "bg-purple-100 dark:bg-purple-900",
                    "textColor": "text-purple-700 dark:text-purple-100",
                    "items": [
                        {"title": f"Build a {role} App", "link": "https://github.com/topics/portfolio"},
                        {"title": "Real-time Dashboard", "link": "https://www.youtube.com/results?search_query=build+real+time+dashboard"},
                    ],
                    "type": "projects",
                },
                {
                    "step": 5,
                    "icon": "🚀",
                    "title": "Trending Roles",
                    "subtitle": "Your Next Move",
                    "color": "bg-indigo-100 dark:bg-indigo-900",
                    "textColor": "text-indigo-700 dark:text-indigo-100",
                    "items": [
                        {"title": f"Senior {role}", "company": "Tech Giants", "match": "95%", "link": f"https://www.google.com/about/careers/applications/jobs/results?q={role}"},
                        {"title": "Tech Lead", "company": "Startups", "match": "90%", "link": f"https://angel.co/jobs?q={role}"},
                    ],
                    "type": "roles",
                },
            ]
        }

if __name__ == "__main__":
    import sys
    try:
        input_data = json.loads(sys.argv[1])
        print(json.dumps(generate_dynamic_roadmap(input_data.get("skills", []), input_data.get("role", ""))))
    except Exception as e:
        # Important: Return empty JSON to prevent node crash
        print(json.dumps({"level": "Unknown", "roadmap": []}))