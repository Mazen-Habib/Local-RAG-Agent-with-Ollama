"""
Check available embedding models in Google Gemini API
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GEMINI_API_KEY:
    print("❌ GOOGLE_API_KEY not found in environment variables!")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# List all available models
print("=" * 80)
print("Available Models in Google Gemini API")
print("=" * 80)

try:
    models = genai.list_models()
    
    # Filter for embedding models
    embedding_models = []
    all_models_info = []
    
    for model in models:
        model_name = model.name
        capabilities = model.supported_generation_config if hasattr(model, 'supported_generation_config') else []
        
        # Check if model supports embedding
        if 'embedContent' in dir(model) or 'embed' in model_name.lower() or 'embedding' in model_name.lower():
            embedding_models.append({
                'name': model_name,
                'display_name': model.display_name if hasattr(model, 'display_name') else model_name,
            })
        
        all_models_info.append({
            'name': model_name,
            'display_name': model.display_name if hasattr(model, 'display_name') else model_name,
        })
    
    print("\n✅ EMBEDDING MODELS:")
    print("-" * 80)
    if embedding_models:
        for model in embedding_models:
            print(f"  • {model['name']}")
            print(f"    Display: {model['display_name']}")
            print()
    else:
        print("  No dedicated embedding models found in list.")
        print("  Checking all available models for embedding capability...")
        print()
    
    print("\n📋 ALL AVAILABLE MODELS:")
    print("-" * 80)
    for model in all_models_info:
        print(f"  • {model['name']}")
    
    print("\n" + "=" * 80)
    print("Try using one of these models for embeddings:")
    print("  - models/text-embedding-004  (Latest)")
    print("  - models/embedding-001")
    print("=" * 80)

except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nTroubleshooting:")
    print("  1. Check that GOOGLE_API_KEY is valid")
    print("  2. Ensure google-generativeai package is installed")
    print("  3. Check API quota and permissions")
