# import os
# import re
# import sys

# # 1. Try to import Google AI Library
# try:
#     import google.generativeai as genai
#     AI_AVAILABLE = True
# except ImportError:
#     print("⚠️ Google AI SDK not found. Run: pip install google-generativeai")
#     AI_AVAILABLE = False

# # ---------------------------------------------------------
# # CONFIGURATION
# # ---------------------------------------------------------

# # ✅ FIX 1: Variable name MUST be uppercase to match usage below
# # api_key = "AIzaSyDi2HIoJAS_urzrmDWSmR3vZteURUptPGs"

# api_key = os.getenv("GEMINI_API_KEY")

# if AI_AVAILABLE and api_key:
#     try:
#         genai.configure(api_key=api_key)
#     except Exception as e:
#         print(f"⚠️ Configuration Error: {e}")

# # ✅ FIX 2: Use the model explicitly listed in your terminal
# DEFAULT_MODEL = 'gemini-2.5-flash' 

# # ---------------------------------------------------------
# # HELPER FUNCTIONS
# # ---------------------------------------------------------

# def clean_json_output(text: str) -> str:
#     """
#     Real-World Cleaner: Removes Markdown formatting and finds the valid JSON block.
#     """
#     if not text: return "{}"
    
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
    
#     start_index = text.find('{')
#     end_index = text.rfind('}')
    
#     if start_index != -1 and end_index != -1:
#         return text[start_index : end_index + 1]
    
#     return text.strip()

# # ---------------------------------------------------------
# # MAIN LLM FUNCTION
# # ---------------------------------------------------------

# def parse_with_llm(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
#     if not AI_AVAILABLE:
#         print("❌ Error: AI Library missing.")
#         return "{}"

#     if not API_KEY:
#         print("❌ Error: API Key missing.")
#         return "{}"

#     try:
#         # print(f"🤖 Calling Gemini ({model_name})...")
#         model = genai.GenerativeModel(model_name)
#         response = model.generate_content(prompt)
#         return clean_json_output(response.text)

#     except Exception as e:
#         print(f"⚠️ Gemini API Failed: {e}")
#         return "{}"

# # ---------------------------------------------------------
# # TEST EXECUTION
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     test_prompt = "Return a JSON object with a greeting message."
#     print(parse_with_llm(test_prompt))






# #llm_engine.py
# import os
# import re
# import json
# import google.generativeai as genai
# from google.api_core import exceptions
# from dotenv import load_dotenv 

# load_dotenv()
# # ---------------------------------------------------------
# # CONFIGURATION
# # ---------------------------------------------------------

# # Try to get key from Environment (Best Practice)
# # If not found, you can fallback to a string, but AVOID committing it.
# API_KEY = os.getenv("GEMINI_API_KEY")

# # CORRECTED MODEL NAME: 'gemini-1.5-flash' is the current stable fast model.
# # 'gemini-2.0-flash-exp' is available for experimental use.
# DEFAULT_MODEL = 'gemini-flash-latest' 

# AI_AVAILABLE = False

# if API_KEY:
#     try:
#         genai.configure(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception as e:
#         print(f"⚠️ Configuration Error: {e}")
# else:
#     print("⚠️ Warning: GOOGLE_API_KEY not found in environment variables.")

# # ---------------------------------------------------------
# # HELPER FUNCTIONS
# # ---------------------------------------------------------

# def clean_json_output(text: str) -> str:
#     """
#     Removes Markdown formatting, finds the JSON block, and verifies validity.
#     """
#     if not text: return "{}"
    
#     # Remove markdown code blocks
#     text = re.sub(r"```json\s*", "", text)
#     text = re.sub(r"```", "", text)
    
#     # Extract substring between first { and last }
#     start_index = text.find('{')
#     end_index = text.rfind('}')
    
#     if start_index != -1 and end_index != -1:
#         cleaned_text = text[start_index : end_index + 1]
#     else:
#         cleaned_text = text.strip()

#     # Verify if it is valid JSON before returning
#     try:
#         json.loads(cleaned_text)
#         return cleaned_text
#     except json.JSONDecodeError:
#         print(f"⚠️ Error: LLM returned invalid JSON:\n{cleaned_text}")
#         return "{}"

# # ---------------------------------------------------------
# # MAIN LLM FUNCTION
# # ---------------------------------------------------------

# def parse_with_llm(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
#     if not AI_AVAILABLE:
#         print("❌ Error: AI Library missing or API Key invalid.")
#         return "{}"

#     try:
#         # print(f"🤖 Calling Gemini ({model_name})...")
#         model = genai.GenerativeModel(model_name)
        
#         # Generation config to force lower temperature (more deterministic for JSON)
#         generation_config = genai.types.GenerationConfig(temperature=0.1)
        
#         response = model.generate_content(prompt, generation_config=generation_config)
        
#         return clean_json_output(response.text)

#     except exceptions.NotFound:
#         print(f"❌ Error: Model '{model_name}' not found. Check availability.")
#         return "{}"
#     except Exception as e:
#         print(f"⚠️ Gemini API Failed: {e}")
#         return "{}"

# # ---------------------------------------------------------
# # TEST EXECUTION
# # ---------------------------------------------------------
# if __name__ == "__main__":
#     # How to run:
#     # Windows: set GOOGLE_API_KEY=your_key_here && python llm_engine.py
#     # Mac/Linux: export GOOGLE_API_KEY=your_key_here && python llm_engine.py
    
#     test_prompt = "Return a JSON object with a greeting message key 'message'."
#     print(f"Response: {parse_with_llm(test_prompt)}")






# src/python/llm_engine.py
import os
import re
import json
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types  # ✅ Required for strict config

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Use a valid model name (2.5 does not exist yet)
DEFAULT_MODEL = "gemini-flash-latest" 
AI_AVAILABLE = False
client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        AI_AVAILABLE = True
        logger.info(f"✅ Gemini Client Initialized (Model: {DEFAULT_MODEL})")
    except Exception as e:
        logger.error(f"⚠️ Gemini client init failed: {e}")
else:
    logger.warning("⚠️ GEMINI_API_KEY not found in environment variables.")

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def clean_json_output(text: str) -> str:
    """
    Removes Markdown formatting, extracts JSON, and validates it.
    """
    if not text:
        return "{}"

    # Remove markdown code blocks
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text)

    # Extract JSON block
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    # Validate JSON
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        logger.error("⚠️ Invalid JSON returned by LLM")
        return "{}"

# ---------------------------------------------------------
# MAIN LLM FUNCTION
# ---------------------------------------------------------

def parse_with_llm(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
    """
    Sends a prompt to Gemini and returns a cleaned JSON string.
    """
    if not AI_AVAILABLE or not client:
        logger.error("❌ Gemini client not available.")
        return "{}"

    try:
        # ✅ Updated Syntax for google-genai SDK
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
        )
        
        # Verify response structure
        if not response.text:
            return "{}"

        return clean_json_output(response.text)

    except Exception as e:
        logger.error(f"⚠️ Gemini API error: {e}")
        return "{}"

# ---------------------------------------------------------
# TEST EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":
    test_prompt = """
    Return a JSON object with a single key "message"
    and value "Hello from Gemini".
    """
    print("Response:", parse_with_llm(test_prompt))