"""
Test embedding dimensions
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")

if not GEMINI_API_KEY:
    print("❌ GOOGLE_API_KEY not found!")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Test gemini-embedding-001
print("Testing gemini-embedding-001 dimensions...")
try:
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content="test text"
    )
    
    dimension = len(result['embedding'])
    
    print(f"✅ Model: models/gemini-embedding-001")
    print(f"   Dimensions: {dimension}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test text-embedding-004 if available
print("\nTesting text-embedding-004 dimensions...")
try:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content="test text"
    )
    
    dimension = len(result['embedding'])
    
    print(f"✅ Model: models/text-embedding-004")
    print(f"   Dimensions: {dimension}")
    
except Exception as e:
    print(f"⚠️  Error: {e}")
