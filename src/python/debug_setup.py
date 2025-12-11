import os
import sys
from dotenv import load_dotenv 

load_dotenv()

print("--- 🔍 STARTING DIAGNOSTIC ---")

# 1. TEST ENVIRONMENT VARIABLES
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ python-dotenv is installed.")
    
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("❌ CRITICAL: GEMINI_API_KEY is missing from .env file!")
    else:
        print(f"✅ API Key found: {key[:5]}... (looks valid)")
except ImportError:
    print("❌ CRITICAL: 'python-dotenv' library is missing. Run: pip install python-dotenv")

# 2. TEST AI CONNECTION
try:
    import google.generativeai as genai
    print("✅ google-generativeai is installed.")
    
    if key:
        genai.configure(api_key=key)
        # Use a model we KNOW works
        model = genai.GenerativeModel('gemini-flash-latest') 
        print("⏳ Testing AI connection (this might take 2 seconds)...")
        response = model.generate_content("Say 'Hello' if you can hear me.")
        if response and response.text:
            print(f"✅ AI Success! Response: {response.text.strip()}")
        else:
            print("❌ AI returned empty response.")
except Exception as e:
    print(f"❌ AI CONNECTION FAILED: {e}")
    print("   -> Did you fix the model name in llm_engine.py?")

# 3. TEST COMPUTER VISION (The 0% issue)
try:
    import cv2
    import mediapipe
    import numpy
    print("✅ OpenCV & MediaPipe are installed (Visuals should work).")
except ImportError as e:
    print(f"❌ VISUAL LIBRARY MISSING: {e}")
    print("   -> Run this command: pip install mediapipe opencv-python numpy")

print("--- 🏁 DIAGNOSTIC COMPLETE ---")