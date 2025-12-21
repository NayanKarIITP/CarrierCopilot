# # resume_parser.py
# import os
# from typing import Dict, Any
# from utils.pdf_reader import read_pdf_text
# from utils.text_cleaner import clean_text, extract_paragraphs
# from llm_engine import parse_with_llm
# import json

# # ---------------------------------------------------------
# # PROMPTS
# # ---------------------------------------------------------

# EXTRACTION_PROMPT = """
# You are an advanced resume parser. Extract the following JSON from the resume text:
# - full_name (if present)
# - emails (list)
# - phones (list)
# - skills (list of single-word or short phrases)
# - education (list of degree+school)
# - experience (list of {title, company, start, end, bullets})
# - projects (list of project short descriptions)

# Return only valid JSON, no explanation.
# Resume text:
# """

# ANALYZE_PROMPT = """
# Given the user's extracted fields (skills, experience, education), rate their resume from 0-100 and provide:
# - resume_score: integer
# - high_level_feedback: list of short suggestions
# Return JSON only.
# """

# # ---------------------------------------------------------
# # FILE PARSER
# # ---------------------------------------------------------

# def parse_resume_from_file(path: str) -> Dict[str, Any]:
#     raw = read_pdf_text(path)
#     cleaned = clean_text(raw)

#     prompt = EXTRACTION_PROMPT + cleaned[:4500]

#     # 💡 Call LLM to extract JSON
#     try:
#         result_text = parse_with_llm(prompt)
#     except Exception:
#         result_text = '{"skills": [], "education": [], "experience": [], "full_name": null, "emails": [], "phones": [], "projects": []}'

#     # Parse JSON safely
#     try:
#         parsed = json.loads(result_text)
#     except:
#         parsed = _fallback_parse(cleaned)

#     # Analyze resume quality
#     analysis = _analyze_resume(parsed)

#     return {
#         "parsed": parsed,
#         "analysis": analysis,
#         "raw_text_preview": cleaned[:2000]
#     }

# # ---------------------------------------------------------
# # TEXT-ONLY PARSER (Required by FastAPI)
# # ---------------------------------------------------------

# def parse_resume_text(text: str) -> Dict[str, Any]:
#     cleaned = clean_text(text)

#     prompt = EXTRACTION_PROMPT + cleaned[:4500]

#     # LLM extraction
#     try:
#         result_text = parse_with_llm(prompt)
#     except:
#         result_text = '{"skills": [], "education": [], "experience": [], "full_name": null, "emails": [], "phones": [], "projects": []}'

#     # JSON parse
#     try:
#         parsed = json.loads(result_text)
#     except:
#         parsed = _fallback_parse(cleaned)

#     # Quality analysis
#     analysis = _analyze_resume(parsed)

#     # SAFETY: ensure skills always exists
#     skills = parsed.get("skills", [])

#     return {
#         "skills": skills,                 
#         "parsed": parsed,
#         "analysis": analysis,
#         "raw_text_preview": cleaned[:2000]
#     }


# # ---------------------------------------------------------
# # FALLBACK LOGIC (Used when LLM fails)
# # ---------------------------------------------------------

# def _fallback_parse(cleaned_text: str):
#     paragraphs = extract_paragraphs(cleaned_text)

#     skills_hint = []
#     for p in paragraphs:
#         if "skills" in p.lower() and len(p) < 300:
#             skills_hint = [
#                 s.strip() for s in p.split(":")[-1].split(",") if s.strip()
#             ]
#             break

#     return {
#         "raw_text": cleaned_text,
#         "skills": skills_hint,
#         "education": [],
#         "experience": [],
#         "projects": [],
#         "emails": [],
#         "phones": []
#     }
# # ---------------------------------------------------------
# # ANALYSIS LOGIC
# # ---------------------------------------------------------

# def _analyze_resume(parsed):
#     try:
#         analysis = parse_with_llm(ANALYZE_PROMPT + str(parsed))
#         return json.loads(analysis)
#     except:
#         return {"resume_score": None, "high_level_feedback": []}

# # ✔ REQUIRED EXPORT ALIAS (IMPORTANT)
# parse_resume_file = parse_resume_from_file

# # ---------------------------------------------------------
# # CLI TESTING
# # ---------------------------------------------------------

# if __name__ == "__main__":
#     import sys
#     path = sys.argv[1]
#     out = parse_resume_from_file(path)
#     print(json.dumps(out, indent=2))








# # resume_parser.py (FIXED VERSION)
# import os
# import re
# from typing import Dict, Any
# from utils.pdf_reader import read_pdf_text
# from utils.text_cleaner import clean_text, extract_paragraphs
# from llm_engine import parse_with_llm
# import json

# # ---------------------------------------------------------
# # PROMPTS
# # ---------------------------------------------------------

# EXTRACTION_PROMPT = """
# You are an advanced resume parser. Extract the following JSON from the resume text:
# - full_name (if present)
# - emails (list)
# - phones (list)
# - skills (list of single-word or short phrases)
# - education (list of degree+school)
# - experience (list of {title, company, start, end, bullets})
# - projects (list of project short descriptions)

# Return only valid JSON, no explanation.
# Resume text:
# """

# ANALYZE_PROMPT = """
# Given the user's extracted fields (skills, experience, education), rate their resume from 0-100 and provide:
# - resume_score: integer
# - high_level_feedback: list of short suggestions
# Return JSON only.
# """

# # Common tech skills to look for
# COMMON_SKILLS = [
#     'python', 'javascript', 'java', 'react', 'node', 'angular', 'vue',
#     'typescript', 'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql',
#     'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'jenkins',
#     'django', 'flask', 'express', 'spring', 'fastapi', 'rest', 'graphql',
#     'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn',
#     'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'
# ]

# # ---------------------------------------------------------
# # FILE PARSER
# # ---------------------------------------------------------

# def parse_resume_from_file(path: str) -> Dict[str, Any]:
#     print(f"📄 Reading PDF: {path}")
#     raw = read_pdf_text(path)
#     cleaned = clean_text(raw)
    
#     print(f"📝 Extracted {len(cleaned)} characters")

#     prompt = EXTRACTION_PROMPT + cleaned[:4500]

#     # 💡 Call LLM to extract JSON
#     parsed = None
#     try:
#         print("🤖 Calling LLM for parsing...")
#         result_text = parse_with_llm(prompt)
#         parsed = json.loads(result_text)
#         print("✅ LLM parsing successful")
#     except Exception as e:
#         print(f"⚠️ LLM failed: {e}. Using fallback parser...")
#         parsed = _fallback_parse(cleaned)

#     # Analyze resume quality
#     analysis = _analyze_resume(parsed)
    
#     # Add score and feedback from analysis
#     score = analysis.get("resume_score", 0)
#     feedback = analysis.get("high_level_feedback", [])
    
#     # If no score from LLM, calculate basic score
#     if score == 0 or score is None:
#         score = _calculate_basic_score(parsed)
#         feedback = _generate_basic_feedback(parsed)
    
#     # Add score and feedback to parsed data
#     parsed["score"] = score
#     parsed["feedback"] = feedback
#     parsed["raw_text"] = cleaned

#     return {
#         "parsed": parsed,
#         "analysis": analysis,
#         "raw_text_preview": cleaned[:2000]
#     }

# # ---------------------------------------------------------
# # TEXT-ONLY PARSER (Required by FastAPI)
# # ---------------------------------------------------------

# def parse_resume_text(text: str) -> Dict[str, Any]:
#     cleaned = clean_text(text)

#     prompt = EXTRACTION_PROMPT + cleaned[:4500]

#     # LLM extraction
#     try:
#         result_text = parse_with_llm(prompt)
#         parsed = json.loads(result_text)
#     except Exception as e:
#         print(f"⚠️ LLM failed: {e}. Using fallback...")
#         parsed = _fallback_parse(cleaned)

#     # Quality analysis
#     analysis = _analyze_resume(parsed)
    
#     # Calculate score
#     score = analysis.get("resume_score", 0)
#     feedback = analysis.get("high_level_feedback", [])
    
#     if score == 0 or score is None:
#         score = _calculate_basic_score(parsed)
#         feedback = _generate_basic_feedback(parsed)
    
#     parsed["score"] = score
#     parsed["feedback"] = feedback
#     parsed["raw_text"] = cleaned

#     return {
#         "skills": parsed.get("skills", []),
#         "parsed": parsed,
#         "analysis": analysis,
#         "raw_text_preview": cleaned[:2000]
#     }


# # ---------------------------------------------------------
# # IMPROVED FALLBACK LOGIC
# # ---------------------------------------------------------

# def _fallback_parse(cleaned_text: str):
#     print("🔧 Using fallback parser...")
    
#     paragraphs = extract_paragraphs(cleaned_text)
#     text_lower = cleaned_text.lower()
    
#     # Extract skills
#     skills = _extract_skills_fallback(text_lower)
    
#     # Extract education
#     education = _extract_education_fallback(cleaned_text)
    
#     # Extract experience
#     experience = _extract_experience_fallback(cleaned_text)
    
#     # Extract emails
#     emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cleaned_text)
    
#     # Extract phones
#     phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', cleaned_text)
    
#     print(f"✅ Fallback extracted: {len(skills)} skills, {len(education)} education, {len(experience)} experience")
    
#     return {
#         "raw_text": cleaned_text,
#         "skills": skills,
#         "education": education,
#         "experience": experience,
#         "projects": [],
#         "emails": emails,
#         "phones": phones,
#         "full_name": None
#     }

# def _extract_skills_fallback(text_lower: str):
#     """Extract skills by looking for common tech keywords"""
#     found_skills = []
#     for skill in COMMON_SKILLS:
#         if skill in text_lower:
#             found_skills.append(skill.capitalize())
#     return list(set(found_skills))  # Remove duplicates

# def _extract_education_fallback(text: str):
#     """Look for education keywords"""
#     education = []
#     edu_keywords = ['bachelor', 'master', 'phd', 'b.s.','b.s.c.', 'm.s.c.', 'm.s.', 'b.tech', 'm.tech', 'university', 'college', 'degree']
    
#     lines = text.split('\n')
#     for i, line in enumerate(lines):
#         if any(keyword in line.lower() for keyword in edu_keywords):
#             education.append({
#                 "degree": line.strip(),
#                 "institution": lines[i+1].strip() if i+1 < len(lines) else "",
#                 "year": ""
#             })
    
#     return education[:3]  # Limit to 3 entries

# def _extract_experience_fallback(text: str):
#     """Look for experience keywords"""
#     experience = []
#     exp_keywords = ['engineer', 'developer', 'analyst', 'manager', 'intern', 'consultant']
    
#     lines = text.split('\n')
#     for line in lines:
#         if any(keyword in line.lower() for keyword in exp_keywords):
#             experience.append({
#                 "title": line.strip(),
#                 "company": "",
#                 "duration": "",
#                 "description": ""
#             })
    
#     return experience[:5]  # Limit to 5 entries

# # ---------------------------------------------------------
# # SCORE CALCULATION
# # ---------------------------------------------------------

# def _calculate_basic_score(parsed: dict) -> int:
#     """Calculate a basic score from parsed data"""
#     score = 0
    
#     skills = parsed.get("skills", [])
#     education = parsed.get("education", [])
#     experience = parsed.get("experience", [])
    
#     # Score components
#     if len(skills) > 0:
#         score += min(30, len(skills) * 3)  # Up to 30 points for skills
    
#     if len(education) > 0:
#         score += 20  # 20 points for education
    
#     if len(experience) > 0:
#         score += min(40, len(experience) * 10)  # Up to 40 points for experience
    
#     # Bonus for completeness
#     if len(parsed.get("raw_text", "")) > 500:
#         score += 10
    
#     return min(score, 100)  # Cap at 100

# def _generate_basic_feedback(parsed: dict) -> list:
#     """Generate basic feedback from parsed data"""
#     feedback = []
    
#     skills = parsed.get("skills", [])
#     education = parsed.get("education", [])
#     experience = parsed.get("experience", [])
    
#     if len(skills) == 0:
#         feedback.append("No technical skills detected. Add relevant skills like programming languages, frameworks, and tools.")
#     elif len(skills) < 5:
#         feedback.append("Add more technical skills to strengthen your resume. Aim for 8-12 relevant skills.")
    
#     if len(education) == 0:
#         feedback.append("No education information found. Include your degree, institution, and graduation year.")
    
#     if len(experience) == 0:
#         feedback.append("No work experience detected. Add your professional experience with quantifiable achievements.")
#     elif len(experience) < 2:
#         feedback.append("Consider adding more details about your work experience and accomplishments.")
    
#     if len(feedback) == 0:
#         feedback.append("Good structure! Consider adding quantifiable metrics to showcase your impact.")
    
#     return feedback

# # ---------------------------------------------------------
# # ANALYSIS LOGIC
# # ---------------------------------------------------------

# def _analyze_resume(parsed):
#     try:
#         analysis = parse_with_llm(ANALYZE_PROMPT + str(parsed))
#         return json.loads(analysis)
#     except:
#         return {
#             "resume_score": _calculate_basic_score(parsed),
#             "high_level_feedback": _generate_basic_feedback(parsed)
#         }

# # ✔ REQUIRED EXPORT ALIAS (IMPORTANT)
# parse_resume_file = parse_resume_from_file

# # ---------------------------------------------------------
# # CLI TESTING
# # ---------------------------------------------------------

# if __name__ == "__main__":
#     import sys
#     path = sys.argv[1]
#     out = parse_resume_from_file(path)
#     print(json.dumps(out, indent=2))








# # resume_parser.py
# import os
# import re
# import json
# from typing import Dict, Any
# from utils.pdf_reader import read_pdf_text
# from utils.text_cleaner import clean_text, extract_paragraphs
# from llm_engine import parse_with_llm

# # ---------------------------------------------------------
# # PROMPTS
# # ---------------------------------------------------------

# EXTRACTION_PROMPT = """
# You are an advanced resume parser. Extract the following JSON from the resume text:
# - full_name (string)
# - emails (list of strings)
# - phones (list of strings)
# - skills (list of strings)
# - education (list of objects with degree, school, year)
# - experience (list of objects with title, company, dates, bullets)
# - projects (list of objects with name, description)

# Return ONLY valid JSON. No Markdown. No Intro.
# Resume Text:
# """

# # ✅ IMPROVED: Explicitly asks for 'feedback' key to match frontend
# ANALYZE_PROMPT = """
# You are a career coach. Analyze this parsed resume JSON and provide a score (0-100) and specific feedback.
# Return ONLY valid JSON with this exact structure:
# {
#     "resume_score": 85,
#     "feedback": [
#         "Suggestion 1",
#         "Suggestion 2",
#         "Suggestion 3"
#     ]
# }

# Parsed Resume Data:
# """

# # Common tech skills (used for fallback/scoring)
# COMMON_SKILLS = [
#     'python', 'javascript', 'java', 'react', 'node', 'angular', 'vue',
#     'typescript', 'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql',
#     'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'jenkins',
#     'django', 'flask', 'express', 'spring', 'fastapi', 'rest', 'graphql',
#     'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn',
#     'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'
# ]

# # ---------------------------------------------------------
# # FILE PARSER
# # ---------------------------------------------------------

# def parse_resume_from_file(path: str) -> Dict[str, Any]:
#     print(f"📄 Reading PDF: {path}")
#     raw = read_pdf_text(path)
#     cleaned = clean_text(raw)
    
#     print(f"📝 Extracted {len(cleaned)} characters")

#     # 1. Extract Data
#     prompt = EXTRACTION_PROMPT + cleaned[:4000]
#     parsed = None
    
#     try:
#         print("🤖 Calling LLM for extraction...")
#         result_text = parse_with_llm(prompt)
#         parsed = json.loads(result_text)
#         print("✅ Extraction successful")
#     except Exception as e:
#         print(f"⚠️ Extraction failed: {e}. Using fallback...")
#         parsed = _fallback_parse(cleaned)

#     # 2. Analyze Data (Score & Feedback)
#     print("🤖 Calling LLM for analysis...")
#     analysis = _analyze_resume(parsed)
    
#     # 3. CRITICAL FIX: Ensure Feedback exists everywhere
#     # Get the raw feedback from analysis
#     raw_feedback = analysis.get("feedback", [])
#     if not raw_feedback:
#          raw_feedback = analysis.get("high_level_feedback", [])
    
#     # If LLM gave nothing, generate fallback feedback
#     if not raw_feedback:
#         print("⚠️ No LLM feedback found. Generating basic feedback...")
#         raw_feedback = _generate_basic_feedback(parsed)

#     # 4. FORCE COPY: Put the data in all possible keys
#     # This ensures server.js finds it whether it looks at 'parsed' or 'analysis'
#     # and whether it looks for 'feedback' or 'high_level_feedback'
    
#     # Update Analysis Object
#     analysis["feedback"] = raw_feedback
#     analysis["high_level_feedback"] = raw_feedback
#     analysis["resume_score"] = analysis.get("resume_score", 0)

#     # Update Parsed Object
#     parsed["score"] = analysis["resume_score"]
#     parsed["feedback"] = raw_feedback
#     parsed["high_level_feedback"] = raw_feedback # Legacy support
#     parsed["raw_text"] = cleaned

#     return {
#         "parsed": parsed,
#         "analysis": analysis,
#         "raw_text_preview": cleaned[:500]
#     }
# # ---------------------------------------------------------
# # TEXT PARSER (For API)
# # ---------------------------------------------------------

# def parse_resume_text(text: str) -> Dict[str, Any]:
#     cleaned = clean_text(text)
#     prompt = EXTRACTION_PROMPT + cleaned[:4000]

#     try:
#         result_text = parse_with_llm(prompt)
#         parsed = json.loads(result_text)
#     except Exception as e:
#         print(f"⚠️ LLM failed: {e}. Using fallback...")
#         parsed = _fallback_parse(cleaned)

#     analysis = _analyze_resume(parsed)
    
#     parsed["score"] = analysis.get("resume_score", 0)
#     parsed["feedback"] = analysis.get("feedback", [])
#     parsed["raw_text"] = cleaned

#     return {
#         "skills": parsed.get("skills", []),
#         "parsed": parsed,
#         "analysis": analysis
#     }

# # ---------------------------------------------------------
# # ANALYSIS LOGIC (FIXED)
# # ---------------------------------------------------------

# def _analyze_resume(parsed_data: dict) -> dict:
#     """
#     Sends the structured data back to LLM to get a score and feedback.
#     """
#     try:
#         # Create a smaller summary to save tokens (don't send raw text again)
#         summary = {
#             "skills": parsed_data.get("skills", []),
#             "experience_count": len(parsed_data.get("experience", [])),
#             "education_count": len(parsed_data.get("education", [])),
#             "experience_titles": [e.get("title", "") for e in parsed_data.get("experience", [])],
#         }

#         # ✅ CRITICAL FIX: Use json.dumps to send valid JSON string, not Python string
#         prompt = ANALYZE_PROMPT + json.dumps(summary, indent=2)
        
#         result_text = parse_with_llm(prompt)
        
#         # Parse the result
#         analysis = json.loads(result_text)
        
#         # Ensure keys exist
#         if "resume_score" not in analysis: analysis["resume_score"] = 50
#         if "feedback" not in analysis: analysis["feedback"] = []
        
#         print(f"✅ Analysis Score: {analysis['resume_score']}")
#         return analysis

#     except Exception as e:
#         print(f"⚠️ Analysis failed: {e}")
#         # Return fallback if LLM fails
#         return {
#             "resume_score": _calculate_basic_score(parsed_data),
#             "feedback": _generate_basic_feedback(parsed_data)
#         }

# # ---------------------------------------------------------
# # FALLBACK / SCORING LOGIC
# # ---------------------------------------------------------

# def _calculate_basic_score(parsed: dict) -> int:
#     score = 0
#     skills = parsed.get("skills", [])
#     if len(skills) > 0: score += min(30, len(skills) * 3)
#     if len(parsed.get("education", [])) > 0: score += 20
#     if len(parsed.get("experience", [])) > 0: score += min(40, len(parsed["experience"]) * 10)
#     if len(parsed.get("raw_text", "")) > 500: score += 10
#     return min(score, 100)

# def _generate_basic_feedback(parsed: dict) -> list:
#     feedback = []
#     skills = parsed.get("skills", [])
    
#     if not skills:
#         feedback.append("No technical skills detected. Add specific hard skills.")
#     elif len(skills) < 5:
#         feedback.append(f"You only have {len(skills)} skills listed. Aim for 8-12 core skills.")
        
#     if not parsed.get("experience"):
#         feedback.append("No experience section found. Add internships or projects.")
    
#     if not feedback:
#         feedback.append("Resume structure looks good. Focus on adding quantifiable metrics (numbers/%) to your bullet points.")
#         feedback.append("Ensure your contact information is clearly visible at the top.")

#     return feedback

# def _fallback_parse(cleaned_text: str):
#     print("🔧 Running Fallback Parser...")
#     text_lower = cleaned_text.lower()
    
#     # Simple extraction
#     skills = [s.capitalize() for s in COMMON_SKILLS if s in text_lower]
#     emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cleaned_text)
#     phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', cleaned_text)
    
#     return {
#         "raw_text": cleaned_text,
#         "skills": list(set(skills)),
#         "education": [],
#         "experience": [],
#         "projects": [],
#         "emails": emails,
#         "phones": phones,
#         "full_name": "Candidate"
#     }

# # Export Alias
# parse_resume_file = parse_resume_from_file

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) > 1:
#         print(json.dumps(parse_resume_from_file(sys.argv[1]), indent=2))








# # src/python/resume_parser.py
# import os
# import re
# import json
# from typing import Dict, Any
# from utils.pdf_reader import read_pdf_text
# from utils.text_cleaner import clean_text, extract_paragraphs
# from llm_engine import parse_with_llm

# # ---------------------------------------------------------
# # PROMPTS
# # ---------------------------------------------------------

# EXTRACTION_PROMPT = """
# You are an advanced resume parser. Extract the following JSON from the resume text:
# - full_name (string)
# - emails (list of strings)
# - phones (list of strings)
# - skills (list of strings)
# - education (list of objects with degree, school, year)
# - experience (list of objects with title, company, dates, bullets)
# - projects (list of objects with name, description)

# Return ONLY valid JSON. No Markdown. No Intro.
# Resume Text:
# """

# ANALYZE_PROMPT = """
# You are a career coach. Analyze this parsed resume JSON and provide a score (0-100) and specific feedback.
# Return ONLY valid JSON with this exact structure:
# {
#     "resume_score": 85,
#     "feedback": [
#         "Suggestion 1",
#         "Suggestion 2",
#         "Suggestion 3"
#     ]
# }

# Parsed Resume Data:
# """

# COMMON_SKILLS = [
#     'python', 'javascript', 'java', 'react', 'node', 'angular', 'vue',
#     'typescript', 'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql',
#     'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'jenkins',
#     'django', 'flask', 'express', 'spring', 'fastapi', 'rest', 'graphql',
#     'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn',
#     'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'
# ]

# # ---------------------------------------------------------
# # FILE PARSER (MAIN)
# # ---------------------------------------------------------

# def parse_resume_from_file(path: str) -> Dict[str, Any]:
#     print(f"📄 Reading PDF: {path}")
#     raw = read_pdf_text(path)
#     cleaned = clean_text(raw)
    
#     print(f"📝 Extracted {len(cleaned)} characters")

#     # 1. Extract Data
#     prompt = EXTRACTION_PROMPT + cleaned[:4000]
#     parsed = None
    
#     try:
#         print("🤖 Calling LLM for extraction...")
#         result_text = parse_with_llm(prompt)
#         parsed = json.loads(result_text)
#         print("✅ Extraction successful")
#     except Exception as e:
#         print(f"⚠️ Extraction failed: {e}. Using fallback...")
#         parsed = _fallback_parse(cleaned)

#     # 2. Analyze Data (Score & Feedback)
#     print("🤖 Calling LLM for analysis...")
#     analysis = _analyze_resume(parsed)
    
#     # 3. CRITICAL FIX: Smart Feedback Retrieval
#     # Look for 'feedback' OR 'high_level_feedback'
#     raw_feedback = analysis.get("feedback", [])
#     if not raw_feedback:
#          raw_feedback = analysis.get("high_level_feedback", [])
    
#     # If still empty, force generate basic feedback
#     if not raw_feedback:
#         print("⚠️ No LLM feedback found. Generating basic feedback...")
#         raw_feedback = _generate_basic_feedback(parsed)

#     # 4. Save Data (Ensure keys match what Server.js expects)
#     analysis["feedback"] = raw_feedback
#     analysis["high_level_feedback"] = raw_feedback
    
#     parsed["score"] = analysis.get("resume_score", 0)
#     parsed["feedback"] = raw_feedback
#     parsed["high_level_feedback"] = raw_feedback
#     parsed["raw_text"] = cleaned

#     return {
#         "parsed": parsed,
#         "analysis": analysis,
#         "raw_text_preview": cleaned[:500]
#     }

# # ---------------------------------------------------------
# # TEXT PARSER (For API)
# # ---------------------------------------------------------

# def parse_resume_text(text: str) -> Dict[str, Any]:
#     cleaned = clean_text(text)
#     prompt = EXTRACTION_PROMPT + cleaned[:4000]

#     try:
#         result_text = parse_with_llm(prompt)
#         parsed = json.loads(result_text)
#     except Exception as e:
#         print(f"⚠️ LLM failed: {e}. Using fallback...")
#         parsed = _fallback_parse(cleaned)

#     analysis = _analyze_resume(parsed)
    
#     raw_feedback = analysis.get("feedback", [])
#     if not raw_feedback:
#          raw_feedback = analysis.get("high_level_feedback", [])
#     if not raw_feedback:
#          raw_feedback = _generate_basic_feedback(parsed)

#     parsed["score"] = analysis.get("resume_score", 0)
#     parsed["feedback"] = raw_feedback
#     parsed["high_level_feedback"] = raw_feedback
#     parsed["raw_text"] = cleaned

#     return {
#         "skills": parsed.get("skills", []),
#         "parsed": parsed,
#         "analysis": analysis
#     }

# # ---------------------------------------------------------
# # ANALYSIS LOGIC
# # ---------------------------------------------------------

# def _analyze_resume(parsed_data: dict) -> dict:
#     try:
#         # Summarize data to save tokens
#         summary = {
#             "skills": parsed_data.get("skills", []),
#             "experience_count": len(parsed_data.get("experience", [])),
#             "education_count": len(parsed_data.get("education", [])),
#             "experience_titles": [e.get("title", "") for e in parsed_data.get("experience", [])],
#         }

#         prompt = ANALYZE_PROMPT + json.dumps(summary, indent=2)
        
#         result_text = parse_with_llm(prompt)
#         analysis = json.loads(result_text)
        
#         if "resume_score" not in analysis: analysis["resume_score"] = 50
#         if "feedback" not in analysis: analysis["feedback"] = []
        
#         return analysis

#     except Exception as e:
#         print(f"⚠️ Analysis failed: {e}")
#         return {
#             "resume_score": _calculate_basic_score(parsed_data),
#             "feedback": _generate_basic_feedback(parsed_data)
#         }

# # ---------------------------------------------------------
# # FALLBACKS
# # ---------------------------------------------------------

# def _calculate_basic_score(parsed: dict) -> int:
#     score = 0
#     skills = parsed.get("skills", [])
#     if len(skills) > 0: score += min(30, len(skills) * 3)
#     if len(parsed.get("education", [])) > 0: score += 20
#     if len(parsed.get("experience", [])) > 0: score += min(40, len(parsed["experience"]) * 10)
#     if len(parsed.get("raw_text", "")) > 500: score += 10
#     return min(score, 100)

# def _generate_basic_feedback(parsed: dict) -> list:
#     feedback = []
#     skills = parsed.get("skills", [])
    
#     if not skills:
#         feedback.append("No technical skills detected. Add specific hard skills.")
#     elif len(skills) < 5:
#         feedback.append(f"You only have {len(skills)} skills listed. Aim for 8-12 core skills.")
        
#     if not parsed.get("experience"):
#         feedback.append("No experience section found. Add internships or projects.")
    
#     if not feedback:
#         feedback.append("Resume structure looks good. Focus on adding quantifiable metrics (numbers/%) to your bullet points.")
#         feedback.append("Ensure your contact information is clearly visible at the top.")

#     return feedback

# def _fallback_parse(cleaned_text: str):
#     print("🔧 Running Fallback Parser...")
#     text_lower = cleaned_text.lower()
#     skills = [s.capitalize() for s in COMMON_SKILLS if s in text_lower]
#     emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cleaned_text)
#     phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', cleaned_text)
    
#     return {
#         "raw_text": cleaned_text,
#         "skills": list(set(skills)),
#         "education": [],
#         "experience": [],
#         "projects": [],
#         "emails": emails,
#         "phones": phones,
#         "full_name": "Candidate"
#     }

# parse_resume_file = parse_resume_from_file

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) > 1:
#         print(json.dumps(parse_resume_from_file(sys.argv[1]), indent=2))






# import os
# import re
# import json
# import sys
# from typing import Dict, Any

# # Ensure we can import local utils
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # 1. Try to import Google AI Library & Utils
# try:
#     import google.generativeai as genai
#     from utils.pdf_reader import read_pdf_text
#     from utils.text_cleaner import clean_text
#     AI_AVAILABLE = True
# except ImportError as e:
#     print(f"⚠️ Import Error: {e}")
#     AI_AVAILABLE = False

# # ---------------------------------------------------------
# # ⚙️ CONFIGURATION
# # ---------------------------------------------------------

# API_KEY = os.getenv("GEMINI_API_KEY")
# # API_KEY = "AIzaSy..." # Uncomment and paste key here if .env fails

# if AI_AVAILABLE and API_KEY:
#     genai.configure(api_key=API_KEY)

# MODEL_NAME = 'gemini-1.5-flash' 

# # ---------------------------------------------------------
# # 🧠 PROMPTS
# # ---------------------------------------------------------

# EXTRACTION_PROMPT = """
# You are an expert ATS Parser. 
# Extract the following from the resume text below into valid JSON:
# {
#     "full_name": "string",
#     "emails": ["string"],
#     "phones": ["string"],
#     "skills": ["string", "string"],
#     "education": [{ "degree": "string", "school": "string", "year": "string" }],
#     "experience": [{ "title": "string", "company": "string", "dates": "string", "bullets": ["string"] }],
#     "projects": [{ "name": "string", "description": "string" }]
# }
# Rules: Return ONLY raw JSON. No markdown.
# Resume Text:
# """

# ANALYZE_PROMPT = """
# You are a Senior Tech Recruiter.
# Analyze the resume data and provide specific feedback.
# Required JSON Structure:
# {
#     "resume_score": 85,
#     "feedback": ["Advice 1", "Advice 2"],
#     "strengths": ["Strength 1", "Strength 2"],
#     "weaknesses": ["Weakness 1", "Weakness 2"]
# }
# Parsed Data:
# """

# COMMON_SKILLS = ['python', 'javascript', 'java', 'react', 'node', 'aws', 'docker', 'sql', 'git']

# # ---------------------------------------------------------
# # 🛠️ HELPER
# # ---------------------------------------------------------

# def call_gemini(prompt: str) -> str:
#     if not AI_AVAILABLE or not API_KEY:
#         raise Exception("Google AI SDK not installed or API Key missing")
#     try:
#         model = genai.GenerativeModel(MODEL_NAME)
#         response = model.generate_content(prompt)
#         return response.text.replace("```json", "").replace("```", "").strip()
#     except Exception as e:
#         print(f"❌ Gemini API Error: {e}")
#         raise e

# # ---------------------------------------------------------
# # 🚀 MAIN PARSER LOGIC
# # ---------------------------------------------------------

# def parse_resume_from_file(path: str) -> Dict[str, Any]:
#     print(f"📄 Processing PDF: {path}")
    
#     try:
#         raw_text = read_pdf_text(path)
#         cleaned_text = clean_text(raw_text)
#     except Exception as e:
#         print(f"❌ PDF Read Error: {e}")
#         return _fallback_parse("")

#     # 1. Extraction
#     try:
#         print(f"🤖 Extracting data...")
#         json_str = call_gemini(EXTRACTION_PROMPT + cleaned_text[:10000])
#         parsed_data = json.loads(json_str)
#         parsed_data["raw_text"] = cleaned_text 
#     except Exception as e:
#         print(f"⚠️ Extraction Failed: {e}")
#         parsed_data = _fallback_parse(cleaned_text)

#     # 2. Analysis
#     try:
#         print("📊 Analyzing...")
#         analysis_payload = {
#             "skills": parsed_data.get("skills", []),
#             "exp_preview": [e.get("title", "") for e in parsed_data.get("experience", [])]
#         }
#         analysis_json = call_gemini(ANALYZE_PROMPT + json.dumps(analysis_payload))
#         analysis_data = json.loads(analysis_json)
#     except Exception as e:
#         print(f"⚠️ Analysis Failed: {e}")
#         analysis_data = {
#             "resume_score": _calculate_basic_score(parsed_data),
#             "feedback": _generate_basic_feedback(parsed_data),
#             "strengths": [],
#             "weaknesses": []
#         }

#     return {
#         "parsed": parsed_data,
#         "analysis": analysis_data,
#         "success": True
#     }

# # ---------------------------------------------------------
# # 🛡️ FALLBACKS
# # ---------------------------------------------------------

# def _fallback_parse(text: str) -> dict:
#     text_lower = text.lower()
#     found_skills = [s.capitalize() for s in COMMON_SKILLS if s in text_lower]
#     emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
#     return {
#         "full_name": "Candidate",
#         "emails": emails,
#         "skills": list(set(found_skills)),
#         "education": [],
#         "experience": [],
#         "raw_text": text
#     }

# def _calculate_basic_score(data: dict) -> int:
#     score = 0
#     if data.get("skills"): score += 30
#     if len(data.get("experience", [])) > 0: score += 40
#     return min(score, 75)

# def _generate_basic_feedback(data: dict) -> list:
#     feedback = []
#     if not data.get("skills"): feedback.append("Add a Skills section.")
#     return feedback

# # ✅ CRITICAL FIX: Alias for app.py compatibility
# parse_resume_file = parse_resume_from_file

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         print(json.dumps(parse_resume_from_file(sys.argv[1]), indent=2))







# src/python/resume_parser.py

import os
import re
import json
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# ---------------------------------------------------------
# LOAD ENV (SAFE FOR LOCAL + PROD)
# ---------------------------------------------------------
load_dotenv()  # harmless in prod, useful locally

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------
# LOGGING (stderr ONLY)
# ---------------------------------------------------------
def log_debug(message: str):
    try:
        sys.stderr.write(f"[PYTHON LOG] {message}\n")
        sys.stderr.flush()
    except:
        pass

# ---------------------------------------------------------
# SAFE IMPORTS
# ---------------------------------------------------------
try:
    import google.generativeai as genai
    from utils.pdf_reader import read_pdf_text
    from utils.text_cleaner import clean_text
    AI_LIB_AVAILABLE = True
except ImportError as e:
    log_debug(f"Import error: {e}")
    AI_LIB_AVAILABLE = False

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-flash-latest"

log_debug(f"GEMINI_API_KEY present: {bool(API_KEY)}")

AI_AVAILABLE = False
if AI_LIB_AVAILABLE and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        AI_AVAILABLE = True
        log_debug("Gemini enabled")
    except Exception as e:
        log_debug(f"Gemini config failed: {e}")

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------
EXTRACTION_PROMPT = """
Extract resume info into JSON:
{
  "skills": ["string"],
  "education": [],
  "experience": []
}
Resume:
"""

ANALYZE_PROMPT = """
Analyze resume JSON and return:
{
  "resume_score": 75,
  "feedback": [],
  "strengths": [],
  "weaknesses": []
}
Data:
"""

COMMON_SKILLS = ["python", "javascript", "react", "node", "sql", "aws"]

# ---------------------------------------------------------
# GEMINI CALL (SAFE)
# ---------------------------------------------------------
def call_gemini(prompt: str) -> str | None:
    if not AI_AVAILABLE:
        return None
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text = response.text or ""
        text = text.replace("```json", "").replace("```", "").strip()
        return text
    except Exception as e:
        log_debug(f"Gemini error: {e}")
        return None

# ---------------------------------------------------------
# FALLBACKS
# ---------------------------------------------------------
def fallback_parse(text: str) -> dict:
    text_lower = text.lower()
    skills = [s.capitalize() for s in COMMON_SKILLS if s in text_lower]
    return {
        "skills": skills,
        "education": [],
        "experience": [],
        "raw_text": text
    }

def fallback_analysis(parsed: dict) -> dict:
    score = 30 + (20 if parsed.get("skills") else 0)
    return {
        "resume_score": min(score, 70),
        "feedback": ["Improve resume formatting", "Add more projects"],
        "strengths": parsed.get("skills", []),
        "weaknesses": []
    }

# ---------------------------------------------------------
# CORE PIPELINE
# ---------------------------------------------------------
def process_resume_text(text: str) -> Dict[str, Any]:
    parsed = None
    analysis = None

    # ---- PARSE ----
    gemini_json = call_gemini(EXTRACTION_PROMPT + text[:8000])
    if gemini_json:
        try:
            parsed = json.loads(gemini_json)
        except Exception:
            parsed = None

    if not parsed:
        parsed = fallback_parse(text)

    # ---- ANALYZE ----
    gemini_analysis = call_gemini(ANALYZE_PROMPT + json.dumps(parsed))
    if gemini_analysis:
        try:
            analysis = json.loads(gemini_analysis)
        except Exception:
            analysis = None

    if not analysis:
        analysis = fallback_analysis(parsed)

    return {
        "success": True,
        "parsed": parsed,
        "analysis": analysis,
        "mode": "ai" if AI_AVAILABLE else "fallback"
    }

# ---------------------------------------------------------
# PUBLIC ENTRY (FILE)
# ---------------------------------------------------------
def parse_resume_from_file(file_path: str) -> Dict[str, Any]:
    try:
        text = read_pdf_text(file_path)
        text = clean_text(text)
        return process_resume_text(text)
    except Exception as e:
        log_debug(f"Resume read error: {e}")
        return {
            "success": True,
            "parsed": fallback_parse(""),
            "analysis": fallback_analysis({"skills": []}),
            "mode": "fallback"
        }

# ---------------------------------------------------------
# CLI ENTRYPOINT (NODE SPAWN)
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print(json.dumps({"success": False, "error": "No file path provided"}))
            sys.exit(0)

        file_path = sys.argv[1]
        result = parse_resume_from_file(file_path)

        # STRICT JSON OUTPUT
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "mode": "fallback"
        }))
