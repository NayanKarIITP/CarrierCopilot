import os
# Import find_dotenv to search for the file in parent folders
from dotenv import load_dotenv, find_dotenv

# 1. This command searches up the directory tree (src -> python -> app) 
#    to find the .env file and load it.
load_dotenv(find_dotenv())

# 2. Now you can get the key securely
api_key = os.environ.get("HF_API_KEY")

# --- Debugging Check ---
if api_key:
    print(f"✅ Success! Loaded API Key: {api_key[:4]}...****")
else:
    print("❌ Error: Could not find HF_API_KEY. Check if .env exists in the 'app' folder.")
