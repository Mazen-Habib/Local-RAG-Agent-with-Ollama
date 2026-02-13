"""
Ollama Configuration
Settings for local LLM with Ollama
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# OLLAMA CONFIGURATION
# ============================================================================

# Ollama API endpoint (default local installation)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Ollama Models
OLLAMA_LLM_MODEL = "llama3.1"  # Main chat model
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"  # Embedding model (768 dimensions)

# Alternative models you can use:
# LLM Models:
# - llama3.1:8b (recommended - good balance)
# - llama3.1:70b (better quality, needs more RAM)
# - llama2 (older, still good)
# - mistral (fast, good quality)
# - codellama (for code-related tasks)

# Embedding Models:
# - nomic-embed-text (768 dims - matches Gemini, recommended)
# - all-minilm (384 dims - smaller, faster)
# - mxbai-embed-large (1024 dims - higher quality)

# ============================================================================
# OLLAMA MODEL SETTINGS
# ============================================================================

# Temperature (0.0 = deterministic, 1.0 = creative)
OLLAMA_TEMPERATURE = 0.7

# Maximum tokens to generate
OLLAMA_MAX_TOKENS = 2048

# Context window size
OLLAMA_CONTEXT_LENGTH = 4096

# Number of tokens to predict
OLLAMA_NUM_PREDICT = 512

# Top-p sampling
OLLAMA_TOP_P = 0.9

# Top-k sampling
OLLAMA_TOP_K = 40

# ============================================================================
# EMBEDDING SETTINGS
# ============================================================================

# Embedding dimensions (must match your Supabase vector column)
# nomic-embed-text = 768 (same as Gemini - no schema change needed!)
# all-minilm = 384
# mxbai-embed-large = 1024
EMBEDDING_DIMENSION = 768

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Number of GPU layers to use (0 = CPU only)
# Set to -1 to use all available GPU layers
# Requires NVIDIA GPU with CUDA
OLLAMA_NUM_GPU = 0  # Change to -1 if you have GPU

# Number of threads for CPU inference
OLLAMA_NUM_THREAD = 4  # Adjust based on your CPU cores

# ============================================================================
# SYSTEM PROMPT (same as before)
# ============================================================================

OLLAMA_SYSTEM_PROMPT = """You are a personal assistant who helps answer questions from a corpus of documents when you don't know the answer yourself.
Use the whole answer you get from the documents and use it to give an answer to user.
Don't include any variables or tags in your answer.
Be helpful, accurate, and concise."""

# ============================================================================
# VALIDATION
# ============================================================================

def validate_ollama_config():
    """Validate Ollama configuration and connection"""
    import requests
    
    print("\n" + "="*60)
    print("🔍 Validating Ollama Configuration")
    print("="*60)
    
    # Check if Ollama is running
    print(f"\n1️⃣ Checking Ollama server at {OLLAMA_BASE_URL}...")
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"✅ Ollama server is running")
            
            # List available models
            models = response.json().get("models", [])
            print(f"\n2️⃣ Available models ({len(models)}):")
            
            llm_found = False
            embed_found = False
            
            for model in models:
                model_name = model.get("name", "")
                print(f"   - {model_name}")
                
                if OLLAMA_LLM_MODEL in model_name:
                    llm_found = True
                if OLLAMA_EMBEDDING_MODEL in model_name:
                    embed_found = True
            
            # Check required models
            print(f"\n3️⃣ Checking required models...")
            if llm_found:
                print(f"✅ LLM model '{OLLAMA_LLM_MODEL}' found")
            else:
                print(f"❌ LLM model '{OLLAMA_LLM_MODEL}' NOT found")
                print(f"   Install with: ollama pull {OLLAMA_LLM_MODEL}")
            
            if embed_found:
                print(f"✅ Embedding model '{OLLAMA_EMBEDDING_MODEL}' found")
            else:
                print(f"❌ Embedding model '{OLLAMA_EMBEDDING_MODEL}' NOT found")
                print(f"   Install with: ollama pull {OLLAMA_EMBEDDING_MODEL}")
            
            print("="*60 + "\n")
            return llm_found and embed_found
            
        else:
            print(f"❌ Ollama server returned error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Ollama server")
        print(f"\n💡 Is Ollama running?")
        print(f"   - Windows: Check if Ollama app is running")
        print(f"   - Linux/Mac: Run 'ollama serve' in terminal")
        print("="*60 + "\n")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def display_ollama_config():
    """Display Ollama configuration"""
    print("\n" + "="*60)
    print("🤖 OLLAMA CONFIGURATION")
    print("="*60)
    print(f"Base URL: {OLLAMA_BASE_URL}")
    print(f"LLM Model: {OLLAMA_LLM_MODEL}")
    print(f"Embedding Model: {OLLAMA_EMBEDDING_MODEL}")
    print(f"Temperature: {OLLAMA_TEMPERATURE}")
    print(f"Max Tokens: {OLLAMA_MAX_TOKENS}")
    print(f"Context Length: {OLLAMA_CONTEXT_LENGTH}")
    print(f"Embedding Dimension: {EMBEDDING_DIMENSION}")
    print(f"GPU Layers: {OLLAMA_NUM_GPU}")
    print(f"CPU Threads: {OLLAMA_NUM_THREAD}")
    print("="*60 + "\n")


if __name__ == "__main__":
    display_ollama_config()
    validate_ollama_config()
