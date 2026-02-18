import os
import sys

print(" STARTING DIAGNOSTIC ")

# 1. TEST ENVIRONMENT VARIABLES
try:
    from dotenv import load_dotenv
    load_dotenv()
    print(" python-dotenv is installed.")
    
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print(" CRITICAL: GEMINI_API_KEY is missing from .env file!")
    else:
        # Security: Print only first 5 and last 3 chars
        print(f" API Key found: {key[:5]}...{key[-3:]} (Format looks valid)")
except ImportError:
    print(" CRITICAL: 'python-dotenv' library is missing. Run: pip install python-dotenv")

# 2. TEST AI CONNECTION
try:
    #  FIX: Correct import for the Python SDK
    import google.generativeai as genai
    print(" google-generativeai is installed.")
    
    if key:
        genai.configure(api_key=key)
        
        #  FIX: Use a stable model name
        model_name = 'gemini-flash-latest'
        model = genai.GenerativeModel(model_name)
        
        print(f"⏳ Testing AI connection with model '{model_name}'...")
        response = model.generate_content("Say 'System Operational' if you can hear me.")
        
        if response and response.text:
            print(f" AI Success! Response: {response.text.strip()}")
        else:
            print(" AI returned empty response (Check API Quota).")

except ImportError:
    print(" LIBRARY ERROR: 'google-generativeai' not installed.")
    print("   -> Run: pip install google-generativeai")
except Exception as e:
    print(f" AI CONNECTION FAILED: {e}")
    print("   -> Tip: Check if your API Key is active in Google Cloud Console.")

# 3. TEST COMPUTER VISION (The 0% issue)
try:
    import cv2
    import mediapipe as mp
    import numpy as np
    print(" OpenCV, MediaPipe, & Numpy are installed.")
    
    # Deep check: Try to actually initialize the Face Mesh (often fails if DLLs are missing)
    try:
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        print(" MediaPipe FaceMesh initialized successfully (Visual AI is ready).")
        face_mesh.close()
    except Exception as e:
        print(f" MediaPipe installed but failed to initialize: {e}")
        print("   -> This usually causes the '0% Clarity' issue.")

except ImportError as e:
    print(f" VISUAL LIBRARY MISSING: {e.name}")
    print("   -> Run: pip install mediapipe opencv-python numpy")

print("  DIAGNOSTIC COMPLETE  ")