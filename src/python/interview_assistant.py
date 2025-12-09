# # interview_assistant.py
# from llm_engine import parse_with_llm
# from typing import Dict, Any
# import json

# QUESTION_PROMPT = """
# You are an interviewer. Provide a single behavioral or technical interview question appropriate for mid-senior engineers.
# Return JSON: {"question": "...", "follow_up": "...", "difficulty": "mid"}
# """

# ANALYZE_PROMPT = """
# Analyze the transcript of an answer for metrics:
# - filler_words_count: dict of filler -> count
# - confidence_estimate: 0-100 (approx)
# - strengths: list
# - improvements: list

# Return JSON only.
# """


# # ---------------------------------------------------------
# # QUESTION GENERATOR (accepts optional argument)
# # ---------------------------------------------------------
# def sample_question(_ignored=None):
#     try:
#         raw = parse_with_llm(QUESTION_PROMPT)
#         return json.loads(raw)
#     except Exception:
#         return {
#             "question": "Tell me about a time you disagreed with a teammate and how you handled it.",
#             "follow_up": "What did you learn?",
#             "difficulty": "mid"
#         }


# # ---------------------------------------------------------
# # ANSWER ANALYZER
# # ---------------------------------------------------------
# def analyze_transcript(transcript: str):
#     prompt = ANALYZE_PROMPT + "\nTranscript:\n" + transcript[:3000]
#     try:
#         raw = parse_with_llm(prompt)
#         return json.loads(raw)
#     except Exception:
#         return {
#             "filler_words_count": {"um": 3, "like": 1},
#             "confidence_estimate": 70,
#             "strengths": ["clear communication", "structured answer"],
#             "improvements": ["quantify achievements", "reduce fillers"]
#         }


# # ---------------------------------------------------------
# # EXPORTS FOR FASTAPI
# # ---------------------------------------------------------
# generate_question = sample_question
# analyze_answer = analyze_transcript










# # interview_assistant.py
# from llm_engine import parse_with_llm
# from typing import Dict, Any
# import json

# QUESTION_PROMPT = """
# You are an interviewer. Provide a single behavioral or technical interview question appropriate for mid-senior engineers.
# Return JSON: {"question": "...", "follow_up": "...", "difficulty": "mid"}
# """

# ANALYZE_PROMPT = """
# Analyze the transcript of an answer for metrics:
# - filler_words_count: dict of filler -> count
# - confidence_estimate: 0-100 (approx)
# - strengths: list
# - improvements: list

# Return JSON only.
# """


# # ---------------------------------------------------------
# # QUESTION GENERATOR (accepts optional argument)
# # ---------------------------------------------------------
# def sample_question(_ignored=None):
#     try:
#         raw = parse_with_llm(QUESTION_PROMPT)
#         return json.loads(raw)
#     except Exception:
#         return {
#             "question": "Tell me about a time you disagreed with a teammate and how you handled it.",
#             "follow_up": "What did you learn?",
#             "difficulty": "mid"
#         }


# # ---------------------------------------------------------
# # ANSWER ANALYZER  (UPDATED with clarity_score)
# # ---------------------------------------------------------
# def analyze_transcript(transcript: str):
#     prompt = ANALYZE_PROMPT + "\nTranscript:\n" + transcript[:3000]

#     # Run LLM
#     try:
#         raw = parse_with_llm(prompt)
#         result = json.loads(raw)
#     except Exception:
#         # default fallback
#         result = {
#             "filler_words_count": {"um": 3, "like": 1},
#             "confidence_estimate": 70,
#             "strengths": ["clear communication", "structured answer"],
#             "improvements": ["quantify achievements", "reduce fillers"]
#         }

#     # -----------------------------
#     # NEW: CALCULATE CLARITY SCORE
#     # -----------------------------
#     filler_words = result.get("filler_words_count", {})
#     confidence = result.get("confidence_estimate", 60)

#     # Simple clarity formula
#     clarity_score = 100 - (sum(filler_words.values()) * 5)
#     clarity_score = int(max(0, min(100, clarity_score)))   # clamp 0–100

#     # Store in result
#     result["clarity_score"] = clarity_score

#     return result


# # ---------------------------------------------------------
# # EXPORTS FOR FASTAPI
# # ---------------------------------------------------------
# generate_question = sample_question
# analyze_answer = analyze_transcript







# # interview_assistant.py
# import json
# import re
# import os
# import sys
# import random

# # Try to import from llm_engine, fix path if needed
# try:
#     from llm_engine import parse_with_llm
# except ImportError:
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     from llm_engine import parse_with_llm

# # ---------------------------------------------------------
# # DYNAMIC PROMPTS
# # ---------------------------------------------------------

# # We use {role} and {level} as placeholders
# QUESTION_PROMPT_TEMPLATE = """
# You are an expert technical interviewer conducting a {level} level interview for a {role} position.
# Generate ONE challenging, relevant interview question appropriate for a {level} candidate.

# - If Junior: Focus on fundamentals and definitions.
# - If Senior: Focus on system design, architecture, or complex scenarios.

# Return ONLY valid JSON in this specific format:
# {{
#     "question": "The interview question text",
#     "follow_up": "A probing follow-up question",
#     "difficulty": "{level}"
# }}
# Do not add markdown formatting like ```json. Just return the raw JSON.
# """

# ANALYZE_PROMPT = """
# You are an interview coach. Analyze this transcript.
# Return valid JSON:
# {
#     "filler_words_count": {"um": 0, "like": 0},
#     "confidence_estimate": 85,
#     "strengths": ["point 1", "point 2"],
#     "improvements": ["point 1", "point 2"]
# }
# Transcript:
# """

# # ---------------------------------------------------------
# # FALLBACK TEMPLATES (If AI Fails)
# # ---------------------------------------------------------
# FALLBACK_TEMPLATES = [
#     {
#         "question": "Can you describe a challenging project you worked on as a {role}?",
#         "follow_up": "What specific technical challenges did you overcome?",
#         "difficulty": "mid"
#     },
#     {
#         "question": "Explain a complex concept in {role} to someone without a technical background.",
#         "follow_up": "How do you ensure they understood the core message?",
#         "difficulty": "easy"
#     },
#     {
#         "question": "Tell me about a time you made a mistake in your role as a {role}.",
#         "follow_up": "How did you handle it and what did you learn?",
#         "difficulty": "mid"
#     },
#     {
#         "question": "What are the most critical skills for a {role} to succeed today?",
#         "follow_up": "How have you demonstrated these skills in your past work?",
#         "difficulty": "hard"
#     }
# ]

# # ---------------------------------------------------------
# # HELPER: CLEAN JSON
# # ---------------------------------------------------------
# def clean_json_output(text: str) -> str:
#     """Removes markdown markers to prevent JSON parse errors."""
#     if not text: return "{}"
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
#     start = text.find('{')
#     end = text.rfind('}')
#     if start != -1 and end != -1:
#         return text[start : end + 1]
#     return text.strip()

# # ---------------------------------------------------------
# # 1. DYNAMIC QUESTION GENERATOR (Updated with Level)
# # ---------------------------------------------------------
# def generate_question(role="Software Engineer", level="Mid-Level"):
#     """
#     Generates a unique question tailored to the specific role and level.
#     """
#     # 1. Safety Checks
#     if not role or not isinstance(role, str):
#         role = "Software Engineer"
#     if not level or not isinstance(level, str):
#         level = "Mid-Level"
    
#     print(f"🤖 Generating {level} AI question for role: {role}...")

#     try:
#         # 2. Inject role AND level into the prompt
#         prompt = QUESTION_PROMPT_TEMPLATE.format(role=role, level=level)
        
#         # 3. Call LLM
#         raw_response = parse_with_llm(prompt, max_length=256)
        
#         # 4. Clean & Parse
#         cleaned_json = clean_json_output(raw_response)
#         data = json.loads(cleaned_json)
        
#         # 5. Return Dynamic Data
#         return data

#     except Exception as e:
#         print(f"⚠️ Question generation failed: {e}")
#         # Dynamic Fallback: Pick a random template
#         template = random.choice(FALLBACK_TEMPLATES)
#         return {
#             "question": template["question"].format(role=role),
#             "follow_up": template["follow_up"],
#             "difficulty": level # Use the requested level
#         }

# # ---------------------------------------------------------
# # 2. ANSWER ANALYZER
# # ---------------------------------------------------------
# def analyze_answer(transcript: str):
#     if not transcript or len(transcript) < 5:
#         return {"error": "Transcript too short"}

#     try:
#         print(f"🤖 Analyzing transcript...")
#         prompt = ANALYZE_PROMPT + f'"{transcript}"'
        
#         raw_response = parse_with_llm(prompt, max_length=512)
#         cleaned_json = clean_json_output(raw_response)
#         result = json.loads(cleaned_json)
        
#         # Calculate Clarity Score logic
#         fillers = result.get("filler_words_count", {})
#         total_fillers = sum(fillers.values())
#         clarity_score = max(0, 100 - (total_fillers * 5))
        
#         result["clarity_score"] = clarity_score
#         return result

#     except Exception as e:
#         print(f"⚠️ Analysis failed: {e}")
#         return {
#             "filler_words_count": {"um": 0},
#             "confidence_estimate": 0,
#             "strengths": ["Could not analyze audio"],
#             "improvements": ["Please check microphone quality"],
#             "clarity_score": 0
#         }

# if __name__ == "__main__":
#     # Test it
#     print(json.dumps(generate_question("Data Scientist", "Senior"), indent=2))









# import json
# import re
# import os
# import sys
# import random

# # Ensure we can find llm_engine
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Try to import
# try:
#     from llm_engine import parse_with_llm
# except ImportError:
#     print("⚠️ Warning: Could not import llm_engine. AI features will be disabled.")
#     def parse_with_llm(prompt, model_name=None): return "{}"

# # ---------------------------------------------------------
# # 🧠 DYNAMIC PROMPTS
# # ---------------------------------------------------------

# QUESTION_PROMPT_TEMPLATE = """
# You are an expert Technical Interviewer for a FAANG company.
# Generate ONE behavioral or technical interview question for a {level} {role} position.

# CRITERIA:
# - {level} Level: {level_desc}
# - Role: {role}
# - Question Type: Challenging, open-ended, real-world scenario.

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "question": "The question text here",
#     "follow_up": "A probing follow-up question to dig deeper",
#     "difficulty": "{level}"
# }}
# """

# ANALYZE_PROMPT = """
# You are an expert Interview Coach. Analyze this candidate's answer.

# TRANSCRIPT: "{transcript}"
# QUESTION CONTEXT: "{question}"

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "filler_words_count": {{ "um": 0, "like": 0, "basically": 0 }},
#     "confidence_estimate": 85,
#     "strengths": ["Strength 1", "Strength 2"],
#     "improvements": ["Improvement 1", "Improvement 2"],
#     "clarity_score": 80
# }}
# """

# # ---------------------------------------------------------
# # 🛡️ FALLBACK TEMPLATES (Safety Net)
# # ---------------------------------------------------------
# FALLBACK_TEMPLATES = [
#     {
#         "question": "Describe a challenging project you worked on as a {role}.",
#         "follow_up": "What specific technical trade-offs did you have to make?",
#         "difficulty": "Mid-Level"
#     },
#     {
#         "question": "How do you stay updated with the latest trends in {role}?",
#         "follow_up": "Can you give an example of a new technology you recently applied?",
#         "difficulty": "Junior"
#     },
#     {
#         "question": "Tell me about a time you disagreed with a team member's technical decision.",
#         "follow_up": "How did you resolve the conflict and what was the outcome?",
#         "difficulty": "Senior"
#     }
# ]

# # ---------------------------------------------------------
# # 🛠️ HELPER: CLEAN JSON
# # ---------------------------------------------------------
# def clean_json_output(text: str) -> str:
#     """Removes markdown markers to prevent JSON parse errors."""
#     if not text: return "{}"
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
#     start = text.find('{')
#     end = text.rfind('}')
#     if start != -1 and end != -1:
#         return text[start : end + 1]
#     return text.strip()

# # ---------------------------------------------------------
# # 1. GENERATE QUESTION
# # ---------------------------------------------------------
# def generate_question(role="Software Engineer", level="Mid-Level"):
#     """Generates a unique question tailored to the specific role and level."""
    
#     # 1. Map Level to Description for better AI Context
#     level_desc = "Focus on fundamentals and problem solving."
#     if "Senior" in level: level_desc = "Focus on system design, scalability, and leadership."
#     if "Junior" in level: level_desc = "Focus on core concepts, algorithms, and learning ability."

#     print(f"🤖 Generating {level} question for {role}...")

#     try:
#         # 2. Build Prompt
#         prompt = QUESTION_PROMPT_TEMPLATE.format(
#             role=role, 
#             level=level, 
#             level_desc=level_desc
#         )
        
#         # 3. Call AI
#         raw_response = parse_with_llm(prompt)
        
#         # 4. Parse Response
#         cleaned_json = clean_json_output(raw_response)
#         data = json.loads(cleaned_json)
        
#         # 5. Return Data (with defaults just in case)
#         return {
#             "question": data.get("question", f"Tell me about your experience as a {role}."),
#             "follow_up": data.get("follow_up", "Can you elaborate on that?"),
#             "difficulty": level
#         }

#     except Exception as e:
#         print(f"⚠️ Generation Failed: {e}. Using Fallback.")
#         template = random.choice(FALLBACK_TEMPLATES)
#         return {
#             "question": template["question"].format(role=role),
#             "follow_up": template["follow_up"],
#             "difficulty": level
#         }

# # ---------------------------------------------------------
# # 2. ANALYZE ANSWER
# # ---------------------------------------------------------
# def analyze_answer(transcript: str, question_context: str = "General Interview"):
#     if not transcript or len(transcript) < 5:
#         return {
#             "strengths": ["N/A"], 
#             "improvements": ["Please provide a longer answer."],
#             "confidence_estimate": 0,
#             "clarity_score": 0
#         }

#     try:
#         print(f"🤖 Analyzing answer...")
#         prompt = ANALYZE_PROMPT.format(transcript=transcript, question=question_context)
        
#         raw_response = parse_with_llm(prompt)
#         cleaned_json = clean_json_output(raw_response)
#         result = json.loads(cleaned_json)
        
#         # Ensure mandatory fields exist
#         if "clarity_score" not in result: result["clarity_score"] = 75
#         if "confidence_estimate" not in result: result["confidence_estimate"] = 80
        
#         return result

#     except Exception as e:
#         print(f"⚠️ Analysis failed: {e}")
#         return {
#             "filler_words_count": {},
#             "confidence_estimate": 0,
#             "strengths": ["Could not analyze"],
#             "improvements": ["System error during analysis"],
#             "clarity_score": 0
#         }

# if __name__ == "__main__":
#     # Test Run
#     print(json.dumps(generate_question("DevOps Engineer", "Senior"), indent=2))







# import json
# import re
# import os
# import sys
# import random

# # Ensure we can find llm_engine regardless of how this script is run
# current_dir = os.path.dirname(os.path.abspath(__file__))
# if current_dir not in sys.path:
#     sys.path.append(current_dir)

# # Try to import
# try:
#     from llm_engine import parse_with_llm
# except ImportError:
#     print("⚠️ Warning: Could not import llm_engine. AI features will be disabled.")
#     # Mock function to prevent crash, returns empty JSON string
#     def parse_with_llm(prompt, model_name=None): return "{}"

# # ---------------------------------------------------------
# # 🧠 DYNAMIC PROMPTS
# # ---------------------------------------------------------

# QUESTION_PROMPT_TEMPLATE = """
# You are an expert Technical Interviewer for a FAANG company.
# Generate ONE behavioral or technical interview question for a {level} {role} position.

# CRITERIA:
# - {level} Level: {level_desc}
# - Role: {role}
# - Question Type: Challenging, open-ended, real-world scenario.

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "question": "The question text here",
#     "follow_up": "A probing follow-up question to dig deeper",
#     "difficulty": "{level}"
# }}
# """

# ANALYZE_PROMPT = """
# You are an expert Interview Coach. Analyze this candidate's answer.

# TRANSCRIPT: "{transcript}"
# QUESTION CONTEXT: "{question}"

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "filler_words_count": {{ "um": 0, "like": 0, "basically": 0 }},
#     "confidence_estimate": 85,
#     "strengths": ["Strength 1", "Strength 2"],
#     "improvements": ["Improvement 1", "Improvement 2"],
#     "clarity_score": 80
# }}
# """

# # ---------------------------------------------------------
# # 🛡️ FALLBACK TEMPLATES (Safety Net)
# # ---------------------------------------------------------
# FALLBACK_TEMPLATES = [
#     {
#         "question": "Describe a challenging project you worked on as a {role}.",
#         "follow_up": "What specific technical trade-offs did you have to make?",
#         "difficulty": "Mid-Level"
#     },
#     {
#         "question": "How do you stay updated with the latest trends in {role}?",
#         "follow_up": "Can you give an example of a new technology you recently applied?",
#         "difficulty": "Junior"
#     },
#     {
#         "question": "Tell me about a time you disagreed with a team member's technical decision.",
#         "follow_up": "How did you resolve the conflict and what was the outcome?",
#         "difficulty": "Senior"
#     }
# ]

# # ---------------------------------------------------------
# # 🛠️ HELPER: CLEAN JSON
# # ---------------------------------------------------------
# def clean_json_output(text: str) -> str:
#     """Removes markdown markers to prevent JSON parse errors."""
#     if not text: return "{}"
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
#     start = text.find('{')
#     end = text.rfind('}')
#     if start != -1 and end != -1:
#         return text[start : end + 1]
#     return text.strip()

# # ---------------------------------------------------------
# # 1. GENERATE QUESTION
# # ---------------------------------------------------------
# def generate_question(role="Software Engineer", level="Mid-Level"):
#     """Generates a unique question tailored to the specific role and level."""
    
#     # 1. Map Level to Description for better AI Context
#     level_desc = "Focus on fundamentals and problem solving."
#     if "Senior" in level: level_desc = "Focus on system design, scalability, and leadership."
#     if "Junior" in level: level_desc = "Focus on core concepts, algorithms, and learning ability."

#     print(f"🤖 Generating {level} question for {role}...")

#     try:
#         # 2. Build Prompt
#         prompt = QUESTION_PROMPT_TEMPLATE.format(
#             role=role, 
#             level=level, 
#             level_desc=level_desc
#         )
        
#         # 3. Call AI
#         raw_response = parse_with_llm(prompt)
        
#         # 4. Parse Response
#         cleaned_json = clean_json_output(raw_response)
        
#         if not cleaned_json or cleaned_json == "{}":
#             raise ValueError("Empty response from AI")

#         data = json.loads(cleaned_json)
        
#         # 5. Return Data (with defaults just in case)
#         return {
#             "question": data.get("question", f"Tell me about your experience as a {role}."),
#             "follow_up": data.get("follow_up", "Can you elaborate on that?"),
#             "difficulty": level
#         }

#     except Exception as e:
#         print(f"⚠️ Generation Failed: {e}. Using Fallback.")
#         template = random.choice(FALLBACK_TEMPLATES)
#         return {
#             "question": template["question"].format(role=role),
#             "follow_up": template["follow_up"],
#             "difficulty": level
#         }

# # ---------------------------------------------------------
# # 2. ANALYZE ANSWER
# # ---------------------------------------------------------
# def analyze_answer(transcript: str, question_context: str = "General Interview"):
#     if not transcript or len(transcript) < 5:
#         return {
#             "strengths": ["N/A"], 
#             "improvements": ["Please provide a longer answer."],
#             "confidence_estimate": 0,
#             "clarity_score": 0,
#             "filler_words_count": {}
#         }

#     try:
#         print(f"🤖 Analyzing answer...")
#         prompt = ANALYZE_PROMPT.format(transcript=transcript, question=question_context)
        
#         raw_response = parse_with_llm(prompt)
#         cleaned_json = clean_json_output(raw_response)
        
#         if not cleaned_json or cleaned_json == "{}":
#              raise ValueError("Empty response from AI")

#         result = json.loads(cleaned_json)
        
#         # Ensure mandatory fields exist
#         if "clarity_score" not in result: result["clarity_score"] = 75
#         if "confidence_estimate" not in result: result["confidence_estimate"] = 80
        
#         return result

#     except Exception as e:
#         print(f"⚠️ Analysis failed: {e}")
#         return {
#             "filler_words_count": {},
#             "confidence_estimate": 0,
#             "strengths": ["Could not analyze"],
#             "improvements": ["System error during analysis"],
#             "clarity_score": 0
#         }

# if __name__ == "__main__":
#     # Test Run
#     print(json.dumps(generate_question("DevOps Engineer", "Senior"), indent=2))









# #interview_assistant.py
# import json
# import re
# import os
# import sys
# import random

# # ✅ FIX 1: Add current directory to sys.path so we can import llm_engine
# current_dir = os.path.dirname(os.path.abspath(__file__))
# if current_dir not in sys.path:
#     sys.path.append(current_dir)

# # ✅ FIX 2: Direct Import
# try:
#     from llm_engine import parse_with_llm
# except ImportError:
#     # Fallback to prevent crash if import fails
#     def parse_with_llm(prompt, model_name=None): return "{}"

# # ---------------------------------------------------------
# # 🧠 DYNAMIC PROMPTS
# # ---------------------------------------------------------

# QUESTION_PROMPT_TEMPLATE = """
# You are an expert Technical Interviewer for a FAANG company.
# Generate ONE behavioral or technical interview question for a {level} {role} position.

# CRITERIA:
# - {level} Level: {level_desc}
# - Role: {role}
# - Question Type: Challenging, open-ended, real-world scenario.

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "question": "The question text here",
#     "follow_up": "A probing follow-up question to dig deeper",
#     "difficulty": "{level}"
# }}
# """

# ANALYZE_PROMPT = """
# You are an expert Interview Coach. Analyze this candidate's answer.

# TRANSCRIPT: "{transcript}"
# QUESTION CONTEXT: "{question}"

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "filler_words_count": {{ "um": 0, "like": 0, "basically": 0 }},
#     "confidence_estimate": 85,
#     "strengths": ["Strength 1", "Strength 2"],
#     "improvements": ["Improvement 1", "Improvement 2"],
#     "clarity_score": 80
# }}
# """

# # ---------------------------------------------------------
# # 🛡️ FALLBACK TEMPLATES
# # ---------------------------------------------------------
# FALLBACK_TEMPLATES = [
#     {
#         "question": "Describe a challenging project you worked on as a {role}.",
#         "follow_up": "What specific technical trade-offs did you have to make?",
#         "difficulty": "Mid-Level"
#     },
#     {
#         "question": "How do you stay updated with the latest trends in {role}?",
#         "follow_up": "Can you give an example of a new technology you recently applied?",
#         "difficulty": "Junior"
#     }
# ]

# # ---------------------------------------------------------
# # 🛠️ HELPER: CLEAN JSON
# # ---------------------------------------------------------
# def clean_json_output(text: str) -> str:
#     if not text: return "{}"
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
#     start = text.find('{')
#     end = text.rfind('}')
#     if start != -1 and end != -1:
#         return text[start : end + 1]
#     return text.strip()

# # ---------------------------------------------------------
# # 1. GENERATE QUESTION
# # ---------------------------------------------------------
# def generate_question(role="Software Engineer", level="Mid-Level"):
#     level_desc = "Focus on fundamentals."
#     if "Senior" in level: level_desc = "Focus on system design and leadership."
#     if "Junior" in level: level_desc = "Focus on core concepts and learning."

#     try:
#         prompt = QUESTION_PROMPT_TEMPLATE.format(
#             role=role, 
#             level=level, 
#             level_desc=level_desc
#         )
        
#         raw_response = parse_with_llm(prompt)
#         cleaned_json = clean_json_output(raw_response)
        
#         if not cleaned_json or cleaned_json == "{}": raise Exception("Empty AI response")

#         data = json.loads(cleaned_json)
        
#         return {
#             "question": data.get("question", f"Tell me about your experience as a {role}."),
#             "follow_up": data.get("follow_up", "Can you elaborate on that?"),
#             "difficulty": level
#         }

#     except Exception as e:
#         # print(f"⚠️ Generation Failed: {e}", file=sys.stderr)
#         template = random.choice(FALLBACK_TEMPLATES)
#         return {
#             "question": template["question"].format(role=role),
#             "follow_up": template["follow_up"],
#             "difficulty": level
#         }

# # ---------------------------------------------------------
# # 2. ANALYZE ANSWER
# # ---------------------------------------------------------
# def analyze_answer(transcript: str, question_context: str = "General Interview"):
#     if not transcript or len(transcript) < 5:
#         return {
#             "strengths": ["N/A"], "improvements": ["Answer too short"],
#             "confidence_estimate": 0, "clarity_score": 0, "filler_words_count": {}
#         }

#     try:
#         prompt = ANALYZE_PROMPT.format(transcript=transcript, question=question_context)
#         raw_response = parse_with_llm(prompt)
#         cleaned_json = clean_json_output(raw_response)
        
#         if not cleaned_json or cleaned_json == "{}": raise Exception("Empty AI response")

#         result = json.loads(cleaned_json)
        
#         # Defaults
#         if "clarity_score" not in result: result["clarity_score"] = 70
#         if "confidence_estimate" not in result: result["confidence_estimate"] = 75
        
#         return result

#     except Exception:
#         return {
#             "filler_words_count": {}, "confidence_estimate": 0,
#             "strengths": ["Analysis failed"], "improvements": ["System error"], "clarity_score": 0
#         }

# # ---------------------------------------------------------
# # ✅ MAIN EXECUTION (Handles Node.js Input)
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         # Check if input is piped via stdin
#         if not sys.stdin.isatty():
#             input_str = sys.stdin.read()
#             if input_str:
#                 data = json.loads(input_str)
#                 action = data.get("action")

#                 if action == "question":
#                     result = generate_question(data.get("role"), data.get("level"))
#                 elif action == "analyze":
#                     result = analyze_answer(data.get("transcript"), data.get("question", ""))
#                 else:
#                     result = {"error": "Unknown action"}
                
#                 print(json.dumps(result))
#             else:
#                 print(json.dumps({"error": "No input received"}))
#         else:
#             # Manual Test
#             print(json.dumps(generate_question("DevOps", "Senior"), indent=2))
            
#     except Exception as e:
#         print(json.dumps({"error": str(e)}))









import json
import re
import os
import sys
import random

# ---------------------------------------------------------
# 🔧 SETUP PATHS & IMPORTS
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from llm_engine import parse_with_llm
except ImportError:
    print("⚠️ Warning: llm_engine not found. Using mock mode.")
    def parse_with_llm(prompt, model_name=None): return "{}"

# ---------------------------------------------------------
# 🧠 DYNAMIC PROMPTS
# ---------------------------------------------------------

QUESTION_PROMPT_TEMPLATE = """
You are an expert Technical Interviewer for a FAANG company.
Generate ONE behavioral or technical interview question for a {level} {role} position.

CONTEXT:
- Difficulty: {level_desc}
- Previous Questions (DO NOT REPEAT): {history_str}

OUTPUT FORMAT (Strict JSON, No Markdown):
{{
    "question": "The question text here",
    "follow_up": "A probing follow-up question",
    "difficulty": "{level}"
}}
"""

ANALYZE_PROMPT = """
You are an expert Interview Coach. Analyze this candidate's answer.

TRANSCRIPT: "{transcript}"
QUESTION CONTEXT: "{question}"

OUTPUT FORMAT (Strict JSON, No Markdown):
{{
    "filler_words_count": {{ "um": 0, "like": 0, "basically": 0 }},
    "confidence_estimate": 85,
    "strengths": ["Strength 1", "Strength 2"],
    "improvements": ["Improvement 1", "Improvement 2"],
    "clarity_score": 80
}}
"""

# ---------------------------------------------------------
# 🛡️ FALLBACK TEMPLATES
# ---------------------------------------------------------
FALLBACK_TEMPLATES = [
    {
        "question": "Describe a challenging project you worked on as a {role}.",
        "follow_up": "What specific technical trade-offs did you have to make?",
        "difficulty": "Mid-Level"
    },
    {
        "question": "How do you stay updated with the latest trends in {role}?",
        "follow_up": "Can you give an example of a new technology you recently applied?",
        "difficulty": "Junior"
    }
]

# ---------------------------------------------------------
# 🛠️ HELPER: CLEAN JSON
# ---------------------------------------------------------
def clean_json_output(text: str) -> str:
    if not text: return "{}"
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text)
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return text[start : end + 1]
    return text.strip()

# ---------------------------------------------------------
# 1. GENERATE QUESTION
# ---------------------------------------------------------
# ✅ FIX: Added 'history' parameter to match app.py call signature
def generate_question(role="Software Engineer", level="Mid-Level", history=None):
    if history is None:
        history = []

    level_desc = "Focus on fundamentals."
    if "Senior" in level: level_desc = "Focus on system design and leadership."
    if "Junior" in level: level_desc = "Focus on core concepts and learning."

    # Convert history list to string for prompt
    history_str = ", ".join([h.get('text', '') for h in history]) if history else "None"

    try:
        prompt = QUESTION_PROMPT_TEMPLATE.format(
            role=role, 
            level=level, 
            level_desc=level_desc,
            history_str=history_str
        )
        
        raw_response = parse_with_llm(prompt)
        cleaned_json = clean_json_output(raw_response)
        
        if not cleaned_json or cleaned_json == "{}": raise Exception("Empty AI response")

        data = json.loads(cleaned_json)
        
        return {
            "question": data.get("question", f"Tell me about your experience as a {role}."),
            "follow_up": data.get("follow_up", "Can you elaborate on that?"),
            "difficulty": level
        }

    except Exception as e:
        # print(f"⚠️ Generation Failed: {e}", file=sys.stderr)
        template = random.choice(FALLBACK_TEMPLATES)
        return {
            "question": template["question"].format(role=role),
            "follow_up": template["follow_up"],
            "difficulty": level
        }

# ---------------------------------------------------------
# 2. ANALYZE ANSWER
# ---------------------------------------------------------
def analyze_answer(transcript: str, question_context: str = "General Interview"):
    if not transcript or len(transcript) < 5:
        return {
            "strengths": ["N/A"], "improvements": ["Answer too short"],
            "confidence_estimate": 0, "clarity_score": 0, "filler_words_count": {}
        }

    try:
        prompt = ANALYZE_PROMPT.format(transcript=transcript, question=question_context)
        raw_response = parse_with_llm(prompt)
        cleaned_json = clean_json_output(raw_response)
        
        if not cleaned_json or cleaned_json == "{}": raise Exception("Empty AI response")

        result = json.loads(cleaned_json)
        
        # Defaults
        if "clarity_score" not in result: result["clarity_score"] = 70
        if "confidence_estimate" not in result: result["confidence_estimate"] = 75
        
        return result

    except Exception:
        return {
            "filler_words_count": {}, "confidence_estimate": 0,
            "strengths": ["Analysis failed"], "improvements": ["System error"], "clarity_score": 0
        }

# ---------------------------------------------------------
# ✅ MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    # Simple test if run directly
    print(json.dumps(generate_question("DevOps", "Senior"), indent=2))