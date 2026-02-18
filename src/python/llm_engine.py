
# src/python/llm_engine.py
import os
import re
import json
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types 

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# CONFIGURATION

API_KEY = os.getenv("GEMINI_API_KEY")

#  Use a valid model name (2.5 does not exist yet)
DEFAULT_MODEL = "gemini-flash-latest" 
AI_AVAILABLE = False
client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        AI_AVAILABLE = True
        logger.info(f" Gemini Client Initialized (Model: {DEFAULT_MODEL})")
    except Exception as e:
        logger.error(f" Gemini client init failed: {e}")
else:
    logger.warning(" GEMINI_API_KEY not found in environment variables.")

# HELPER FUNCTIONS

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
        logger.error(" Invalid JSON returned by LLM")
        return "{}"

# MAIN LLM FUNCTION

def parse_with_llm(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
    """
    Sends a prompt to Gemini and returns a cleaned JSON string.
    """
    if not AI_AVAILABLE or not client:
        logger.error(" Gemini client not available.")
        return "{}"

    try:
        # Updated Syntax for google-genai SDK
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
        logger.error(f" Gemini API error: {e}")
        return "{}"

# TEST EXECUTION

if __name__ == "__main__":
    test_prompt = """
    Return a JSON object with a single key "message"
    and value "Hello from Gemini".
    """
    print("Response:", parse_with_llm(test_prompt))