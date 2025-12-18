
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






# #interview_assistant.py
# import json
# import re
# import os
# import sys
# import random

# # ---------------------------------------------------------
# # 🔧 SETUP PATHS & IMPORTS
# # ---------------------------------------------------------
# current_dir = os.path.dirname(os.path.abspath(__file__))
# if current_dir not in sys.path:
#     sys.path.append(current_dir)

# try:
#     from llm_engine import parse_with_llm
# except ImportError:
#     print("⚠️ Warning: llm_engine not found. Using mock mode.")
#     def parse_with_llm(prompt, model_name=None): return "{}"

# # ---------------------------------------------------------
# # 🧠 DYNAMIC PROMPTS
# # ---------------------------------------------------------

# QUESTION_PROMPT_TEMPLATE = """
# You are an expert Technical Interviewer for a FAANG company.
# Generate ONE behavioral or technical interview question for a {level} {role} position.

# CONTEXT:
# - Difficulty: {level_desc}
# - Previous Questions (DO NOT REPEAT): {history_str}

# OUTPUT FORMAT (Strict JSON, No Markdown):
# {{
#     "question": "The question text here",
#     "follow_up": "A probing follow-up question",
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
#     },
#     {
#         "question": "Tell me about a time you had a conflict with a team member.",
#         "follow_up": "How did you resolve it and what was the outcome?",
#         "difficulty": "Behavioral"
#     }
# ]

# # ---------------------------------------------------------
# # 🛠️ HELPER: CLEAN JSON
# # ---------------------------------------------------------
# def clean_json_output(text: str) -> str:
#     if not text: return "{}"
#     # Remove markdown code blocks if present
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
    
#     # Find the first { and last }
#     start = text.find('{')
#     end = text.rfind('}')
    
#     if start != -1 and end != -1:
#         return text[start : end + 1]
#     return text.strip()

# # ---------------------------------------------------------
# # 1. GENERATE QUESTION
# # ---------------------------------------------------------
# def generate_question(role="Software Engineer", level="Mid-Level", history=None):
#     if history is None:
#         history = []

#     level_desc = "Focus on fundamentals."
#     if "Senior" in level: level_desc = "Focus on system design and leadership."
#     if "Junior" in level: level_desc = "Focus on core concepts and learning."

#     # Convert history list to string for prompt
#     history_str = ", ".join([h.get('text', '') for h in history]) if history else "None"

#     try:
#         prompt = QUESTION_PROMPT_TEMPLATE.format(
#             role=role, 
#             level=level, 
#             level_desc=level_desc,
#             history_str=history_str
#         )
        
#         raw_response = parse_with_llm(prompt)
        
#         # DEBUG: Print what the AI actually sent back
#         # print(f"DEBUG (generate_question): AI Raw Response: {raw_response[:100]}...") 

#         cleaned_json = clean_json_output(raw_response)
        
#         if not cleaned_json or cleaned_json == "{}": 
#             raise Exception("Empty AI response received.")

#         data = json.loads(cleaned_json)
        
#         return {
#             "question": data.get("question", f"Tell me about your experience as a {role}."),
#             "follow_up": data.get("follow_up", "Can you elaborate on that?"),
#             "difficulty": level
#         }

#     except Exception as e:
#         print(f"⚠️ Question Generation Failed: {e}")
#         # Use Fallback if AI fails
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
#             "strengths": ["N/A"], "improvements": ["Answer too short or missing"],
#             "confidence_estimate": 0, "clarity_score": 0, "filler_words_count": {}
#         }

#     try:
#         prompt = ANALYZE_PROMPT.format(transcript=transcript, question=question_context)
        
#         raw_response = parse_with_llm(prompt)
#         cleaned_json = clean_json_output(raw_response)
        
#         if not cleaned_json or cleaned_json == "{}": 
#             raise Exception("Empty AI response received.")

#         result = json.loads(cleaned_json)
        
#         # Ensure defaults exist
#         if "clarity_score" not in result: result["clarity_score"] = 70
#         if "confidence_estimate" not in result: result["confidence_estimate"] = 75
        
#         return result

#     except Exception as e:
#         print(f"⚠️ Analysis Failed: {e}")
#         return {
#             "filler_words_count": {}, 
#             "confidence_estimate": 0,
#             "strengths": ["Analysis failed (Technical Error)"], 
#             "improvements": ["Please try again."], 
#             "clarity_score": 0
#         }

# # ---------------------------------------------------------
# # ✅ MAIN EXECUTION
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     # Test Question Gen
#     print("--- Testing Question Generation ---")
#     q = generate_question("DevOps", "Senior")
#     print(json.dumps(q, indent=2))
    
#     # Test Analysis
#     print("\n--- Testing Answer Analysis ---")
#     a = analyze_answer("I think basically I am good at coding.", "Tell me about yourself.")
#     print(json.dumps(a, indent=2))







#interview_assistant.py
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
    from python.llm_engine import parse_with_llm
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
# 🛡️ FALLBACK TEMPLATES (Backup Questions)
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
    },
    {
        "question": "Tell me about a time you had a conflict with a team member.",
        "follow_up": "How did you resolve it and what was the outcome?",
        "difficulty": "Behavioral"
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
def generate_question(role="Software Engineer", level="Mid-Level", history=None):
    if history is None:
        history = []

    level_desc = "Focus on fundamentals."
    if "Senior" in level: level_desc = "Focus on system design and leadership."
    if "Junior" in level: level_desc = "Focus on core concepts and learning."

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
        
        # ✅ CRITICAL FIX: If AI returns empty, raise error immediately to trigger fallback
        if not cleaned_json or cleaned_json == "{}": 
            raise Exception("Empty AI response received (Rate Limit or Network Error).")

        data = json.loads(cleaned_json)
        
        return {
            "question": data.get("question", f"Tell me about your experience as a {role}."),
            "follow_up": data.get("follow_up", "Can you elaborate on that?"),
            "difficulty": level
        }

    except Exception as e:
        print(f"⚠️ Question Generation Failed: {e}")
        print("🔄 Switching to FALLBACK TEMPLATE to prevent crash.")
        
        # ✅ FALLBACK LOGIC: Pick a random backup question
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
        
        if not cleaned_json or cleaned_json == "{}": 
            raise Exception("Empty AI response received.")

        result = json.loads(cleaned_json)
        
        if "clarity_score" not in result: result["clarity_score"] = 70
        if "confidence_estimate" not in result: result["confidence_estimate"] = 75
        
        return result

    except Exception as e:
        print(f"⚠️ Analysis Failed: {e}")
        # FALLBACK: Return dummy analysis so frontend doesn't break
        return {
            "filler_words_count": {}, 
            "confidence_estimate": 70,
            "strengths": ["Good effort", "Clear communication"], 
            "improvements": ["Add more technical details", "Structure your answer better"], 
            "clarity_score": 70
        }

# ---------------------------------------------------------
# ✅ MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    print(json.dumps(generate_question("DevOps", "Senior"), indent=2))