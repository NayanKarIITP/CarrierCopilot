# roadmap_generator.py
from llm_engine import parse_with_llm
from typing import Dict, Any
import json

# ---------------------------------------------------------
# PROMPT TEMPLATE
# ---------------------------------------------------------

ROADMAP_PROMPT = """
You are an AI assistant that generates a 4-step personalized learning roadmap.
Input: a JSON containing user's skills, projects, education, experience, and the target role.

Output JSON format:
{
  "steps": [
    { "title": "", "subtitle": "", "items": [] },
    ...
  ]
}

Return JSON ONLY. No explanation text.
"""

# ---------------------------------------------------------
# MAIN FUNCTION (expected by FastAPI)
# ---------------------------------------------------------

def generate_dynamic_roadmap(skills, role: str):
    """
    FastAPI expects this function.
    skills → list
    role → string
    """

    summary = {
        "skills": skills,
        "target_role": role
    }

    prompt = ROADMAP_PROMPT + "\nUser Summary:\n" + str(summary)

    try:
        raw_output = parse_with_llm(prompt)

        # Try parse JSON output
        return json.loads(raw_output)

    except Exception:
        # fallback roadmap if HF fails
        return {
            "steps": [
                {
                    "title": "Your Foundation",
                    "subtitle": "Current Strengths",
                    "items": skills[:5]
                },
                {
                    "title": "Skills to Acquire",
                    "subtitle": f"Skills needed for {role}",
                    "items": ["Docker", "Kubernetes", "System Design", "GraphQL"]
                },
                {
                    "title": "Recommended Courses",
                    "subtitle": "Best Learning Resources",
                    "items": [
                        {"title": "Docker Mastery", "platform": "Udemy"},
                        {"title": "Kubernetes for Developers", "platform": "Coursera"},
                    ]
                },
                {
                    "title": "Recommended Projects",
                    "subtitle": "Build Hands-On Experience",
                    "items": [
                        "Deploy a microservices system on Kubernetes",
                        "Build GraphQL real-time API with subscriptions"
                    ]
                }
            ]
        }













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
