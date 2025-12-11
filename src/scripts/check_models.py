import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Paste your API Key here directly
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")