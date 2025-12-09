import google.generativeai as genai
import os

# Paste your API Key here directly
api_key = "AIzaSyCCs3_htORG197m0bz6SeVjqERnlfco5I4" 

genai.configure(api_key=api_key)

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")