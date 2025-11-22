# # skill_gap_analyzer.py
# from sentence_transformers import SentenceTransformer, util
# from typing import List, Dict, Union
# import numpy as np

# EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# def normalize_list(skills: Union[List[str], str]):
#     """Accepts list OR comma-separated string."""
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

# def find_skill_gaps(user_skills_raw, role_skills_raw, top_k: int = 10):
#     """
#     Returns missing role skills with similarity scoring.
#     Safe version (never crashes).
#     """

#     user_skills = normalize_list(user_skills_raw)
#     role_skills = normalize_list(role_skills_raw)

#     if not role_skills:
#         return []

#     # If user has zero skills → return all role skills with score 0
#     if not user_skills:
#         return [{"skill": s, "match_score": 0.0} for s in role_skills]

#     user_emb = embed_list(user_skills)
#     role_emb = embed_list(role_skills)

#     # If embeddings failed
#     if user_emb is None or role_emb is None:
#         return [{"skill": s, "match_score": 0.0} for s in role_skills]

#     # Compute similarity safely
#     try:
#         cos_sim = util.pytorch_cos_sim(role_emb, user_emb).cpu().numpy()
#     except Exception:
#         # fallback: zero similarity
#         return [{"skill": s, "match_score": 0.0} for s in role_skills]

#     gaps = []
#     for i, skill in enumerate(role_skills):
#         row = cos_sim[i]

#         # safe max: handle shape (1,), empty, etc.
#         best_sim = float(np.max(row)) if row.size > 0 else 0.0

#         gaps.append({
#             "skill": skill,
#             "match_score": best_sim
#         })

#     # sort: lowest similarity = biggest gap
#     gaps_sorted = sorted(gaps, key=lambda x: x["match_score"])
#     return gaps_sorted[:top_k]

# # Alias for FastAPI
# analyze_skill_gap = find_skill_gaps





# skill_gap_analyzer.py (FINAL FIXED VERSION)

from sentence_transformers import SentenceTransformer, util
from typing import List, Dict, Union
import numpy as np

# Load model once
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def normalize_list(skills: Union[List[str], str]):
    """Accepts list OR comma-separated string and normalizes to list."""
    if not skills:
        return []
    if isinstance(skills, list):
        return [s.strip() for s in skills if s.strip()]
    if isinstance(skills, str):
        return [s.strip() for s in skills.split(",") if s.strip()]
    return []

def embed_list(items: List[str]):
    if not items:
        return None
    return EMBED_MODEL.encode(items, convert_to_tensor=True)

# ---------------------------------------------------------
# Main logic — safe version
# ---------------------------------------------------------
def find_skill_gaps(user_skills_raw, role_skills_raw, top_k: int = 10):
    """Compute gaps between role skills and user skills, returns top missing skills."""

    user_skills = normalize_list(user_skills_raw)
    role_skills = normalize_list(role_skills_raw)

    # If no role skills → no gaps
    if not role_skills:
        return []

    # If user has zero skills → return all role skills with score 0
    if not user_skills:
        return [{"skill": s, "match_score": 0.0} for s in role_skills]

    # Embed
    user_emb = embed_list(user_skills)
    role_emb = embed_list(role_skills)

    if user_emb is None or role_emb is None:
        return [{"skill": s, "match_score": 0.0} for s in role_skills]

    # Compute similarity safely
    try:
        cos_sim = util.pytorch_cos_sim(role_emb, user_emb).cpu().numpy()
    except Exception:
        return [{"skill": s, "match_score": 0.0} for s in role_skills]

    # Build gap list
    gaps = []
    for i, skill in enumerate(role_skills):
        row = cos_sim[i] if i < len(cos_sim) else []
        best_sim = float(np.max(row)) if hasattr(row, "size") and row.size > 0 else 0.0

        gaps.append({
            "skill": skill,
            "match_score": best_sim
        })

    # Sort: lowest similarity = biggest gap
    return sorted(gaps, key=lambda x: x["match_score"])[:top_k]

# ---------------------------------------------------------
# REQUIRED EXPORT — FIX FOR FASTAPI IMPORT ERROR
# ---------------------------------------------------------
def analyze_skill_gap(user_skills, target_role_skills):
    """Wrapper used by FastAPI. Must exist at top level."""
    return find_skill_gaps(user_skills, target_role_skills)


# Debug test
if __name__ == "__main__":
    print(analyze_skill_gap(["React", "Node.js"], ["Docker", "Kubernetes", "React"]))



