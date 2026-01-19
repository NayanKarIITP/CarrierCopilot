import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

print("--- 🔍 CHECKING AVAILABLE GEMINI MODELS ---")

# 1. Load Environment Variables
# find_dotenv() looks in parent folders if .env isn't in the same directory
load_dotenv(find_dotenv())

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit()

print(f"✅ API Key loaded: {api_key[:5]}...****")

# 2. Configure Google AI
try:
    genai.configure(api_key=api_key)

    # 3. List Available Models
    print("\n📋 Fetching model list from Google Cloud...")
    models = genai.list_models()
    
    found_flash = False
    print("\n--- AVAILABLE MODELS ---")
    for m in models:
        # We only care about models that can "generateContent" (chat models)
        if 'generateContent' in m.supported_generation_methods:
            print(f" • {m.name}")
            if "gemini-1.5-flash" in m.name:
                found_flash = True

    print("------------------------")

    # 4. Verification
    if found_flash:
        print("\n✅ SUCCESS: 'models/gemini-1.5-flash' is available!")
        print("   👉 Please ensure your python code uses: model = genai.GenerativeModel('gemini-1.5-flash')")
    else:
        print("\n⚠️ WARNING: 'gemini-1.5-flash' was not explicitly listed.")
        print("   This might be a region issue or API key restriction.")

except Exception as e:
    print(f"\n❌ CONNECTION ERROR: {e}")