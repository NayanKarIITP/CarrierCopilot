
# # skill_gap_analyzer.py (FINAL FIXED VERSION)

# from sentence_transformers import SentenceTransformer, util
# from typing import List, Dict, Union
# import numpy as np

# # Load model once
# EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# # ---------------------------------------------------------
# # Helpers
# # ---------------------------------------------------------
# def normalize_list(skills: Union[List[str], str]):
#     """Accepts list OR comma-separated string and normalizes to list."""
#     if not skills:
#         return []
#     if isinstance(skills, list):
#         return [s.strip() for s in skills if s.strip()]
#     if isinstance(skills, str):
#         return [s.strip() for s in skills.split(",") if s.strip()]
#     return []

# def embed_list(items: List[str]):
#     if not items:
#         return None
#     return EMBED_MODEL.encode(items, convert_to_tensor=True)

# # ---------------------------------------------------------
# # Main logic — safe version
# # ---------------------------------------------------------
# def find_skill_gaps(user_skills_raw, role_skills_raw, top_k: int = 10):
#     """Compute gaps between role skills and user skills, returns top missing skills."""

#     user_skills = normalize_list(user_skills_raw)
#     role_skills = normalize_list(role_skills_raw)

#     # If no role skills → no gaps
#     if not role_skills:
#         return []

#     # If user has zero skills → return all role skills with score 0
#     if not user_skills:
#         return [{"skill": s, "match_score": 0.0} for s in role_skills]

#     # Embed
#     user_emb = embed_list(user_skills)
#     role_emb = embed_list(role_skills)

#     if user_emb is None or role_emb is None:
#         return [{"skill": s, "match_score": 0.0} for s in role_skills]

#     # Compute similarity safely
#     try:
#         cos_sim = util.pytorch_cos_sim(role_emb, user_emb).cpu().numpy()
#     except Exception:
#         return [{"skill": s, "match_score": 0.0} for s in role_skills]

#     # Build gap list
#     gaps = []
#     for i, skill in enumerate(role_skills):
#         row = cos_sim[i] if i < len(cos_sim) else []
#         best_sim = float(np.max(row)) if hasattr(row, "size") and row.size > 0 else 0.0

#         gaps.append({
#             "skill": skill,
#             "match_score": best_sim
#         })

#     # Sort: lowest similarity = biggest gap
#     return sorted(gaps, key=lambda x: x["match_score"])[:top_k]

# # ---------------------------------------------------------
# # REQUIRED EXPORT — FIX FOR FASTAPI IMPORT ERROR
# # ---------------------------------------------------------
# def analyze_skill_gap(user_skills, target_role_skills):
#     """Wrapper used by FastAPI. Must exist at top level."""
#     return find_skill_gaps(user_skills, target_role_skills)


# # Debug test
# if __name__ == "__main__":
#     print(analyze_skill_gap(["React", "Node.js"], ["Docker", "Kubernetes", "React"]))







import os
import json
import google.generativeai as genai
from typing import List, Union
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ WARNING: GEMINI_API_KEY not found. Skill Gap Analysis will fail.")

# Use the fast, free-tier friendly model
MODEL_NAME = "gemini-flash-latest"  # Or 'gemini-1.5-flash' if you prefer

# ---------------------------------------------------------
# PROMPT TEMPLATE
# ---------------------------------------------------------
GAP_ANALYSIS_PROMPT = """
You are an expert Career Coach and Tech Recruiter.
Compare a candidate's existing skills against the required skills for a target role.

CANDIDATE SKILLS: {user_skills}
REQUIRED ROLE SKILLS: {role_skills}

TASK:
1. Identify which required skills are MISSING or WEAK in the candidate's profile.
2. Ignore skills the candidate already has (even if named slightly differently, e.g., "ReactJS" vs "React").
3. Assign a "match_score" (0.0 to 1.0) for each required skill:
   - 1.0 = Exact match (User has this skill).
   - 0.5 = Partial match (User has a related skill).
   - 0.0 = Missing (User completely lacks this skill).

OUTPUT FORMAT (Strict JSON, list of objects):
[
  {{ "skill": "Skill Name", "match_score": 0.0, "reason": "Brief explanation" }},
  ...
]
"""

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def normalize_list(skills: Union[List[str], str]) -> str:
    """Converts list or string to a comma-separated string for the prompt."""
    if not skills:
        return "None"
    if isinstance(skills, list):
        return ", ".join([str(s) for s in skills if s])
    return str(skills)

def clean_json_response(text: str) -> str:
    """Removes Markdown formatting from AI response."""
    text = text.replace("```json", "").replace("```", "").strip()
    return text

# ---------------------------------------------------------
# Main Logic (Gemini API)
# ---------------------------------------------------------
def analyze_skill_gap(user_skills, role_skills):
    """
    Uses Gemini AI to semantically compare skills and find gaps.
    """
    user_str = normalize_list(user_skills)
    role_str = normalize_list(role_skills)

    # Fast fail if data is missing
    if role_str == "None":
        return []
    if user_str == "None":
        # If user has no skills, everything is a gap (score 0)
        return [{"skill": s.strip(), "match_score": 0.0, "reason": "User has no listed skills."} 
                for s in role_str.split(",") if s.strip()]

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = GAP_ANALYSIS_PROMPT.format(user_skills=user_str, role_skills=role_str)
        
        # Determine temperature=0 for consistent, logical results
        response = model.generate_content(prompt, generation_config={"temperature": 0.0})
        
        cleaned_json = clean_json_response(response.text)
        gaps_data = json.loads(cleaned_json)

        # Sort: Lowest match score (biggest gaps) first
        gaps_data.sort(key=lambda x: x["match_score"])
        
        return gaps_data

    except Exception as e:
        print(f"⚠️ Skill Gap Analysis Failed: {e}")
        # Fallback: Return simple list assuming 0 match if AI fails
        return [{"skill": s.strip(), "match_score": 0.0, "reason": "AI Analysis Failed"} 
                for s in role_str.split(",") if s.strip()]

# ---------------------------------------------------------
# Debug Test
# ---------------------------------------------------------
if __name__ == "__main__":
    # Example Test
    u_skills = ["React", "JavaScript", "HTML", "CSS"]
    r_skills = ["React", "TypeScript", "AWS", "Docker", "Kubernetes"]
    
    print("--- 🔍 Testing Gemini Skill Gap Analyzer ---")
    result = analyze_skill_gap(u_skills, r_skills)
    print(json.dumps(result, indent=2))