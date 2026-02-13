"""
Configuration file for RAG Agent
Store all your credentials and settings here
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# GEMINI API CONFIGURATION
# ============================================================================
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Gemini Models
GEMINI_MODEL = "gemini-2.5-flash"  # Fast and efficient
# GEMINI_MODEL = "gemini-1.5-pro"  # More capable, use if needed
GEMINI_TEMPERATURE = 0.7
GEMINI_EMBEDDING_MODEL = "models/gemini-embedding-001"  # Latest embedding model
# ============================================================================
# SUPABASE CONFIGURATION
# ============================================================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_API_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")  # Use service_role key for vector operations

# Supabase Vector Store Settings
SUPABASE_TABLE_NAME = "documents"
SUPABASE_QUERY_NAME = "match_documents"  # The RPC function for similarity search

# ============================================================================
# DOCUMENT PROCESSING CONFIGURATION
# ============================================================================
# Chunk size for splitting documents
CHUNK_SIZE = 200  # Matching your n8n settings
CHUNK_OVERLAP = 50  # Some overlap to preserve context

# PDF Upload folder
PDF_UPLOAD_FOLDER = "./pdfs"  # Local folder for PDFs
os.makedirs(PDF_UPLOAD_FOLDER, exist_ok=True)

# ============================================================================
# RAG AGENT CONFIGURATION
# ============================================================================
# System prompt for the RAG agent
SYSTEM_PROMPT = """You are a personal assistant who helps answer questions from a corpus of documents when you don't know the answer yourself.
Use the whole answer you get from the documents and use it to give an answer to user.
Don't include any variables or tags in your answer.
Be helpful, accurate, and concise."""

# Number of documents to retrieve for context
TOP_K_DOCUMENTS = 5

# ============================================================================
# VALIDATION
# ============================================================================
def validate_config():
    """Validate that all required configuration is present"""
    errors = []
    
    if not GEMINI_API_KEY:
        errors.append("❌ GOOGLE_API_KEY not set")
    
    if not SUPABASE_URL:
        errors.append("❌ SUPABASE_URL not set")
    
    if not SUPABASE_API_KEY:
        errors.append("❌ SUPABASE_SERVICE_KEY not set")
    
    if errors:
        print("\n" + "="*60)
        print("⚠️  CONFIGURATION ERRORS")
        print("="*60)
        for error in errors:
            print(error)
        print("\n📝 Please create a .env file with:")
        print("GOOGLE_API_KEY=your_gemini_key")
        print("SUPABASE_URL=your_supabase_url")
        print("SUPABASE_SERVICE_KEY=your_supabase_service_key")
        print("="*60 + "\n")
        return False
    
    print("✅ Configuration validated successfully")
    return True


# ============================================================================
# DISPLAY CONFIGURATION (for debugging)
# ============================================================================
def display_config():
    """Display current configuration (without sensitive data)"""
    print("\n" + "="*60)
    print("📋 CURRENT CONFIGURATION")
    print("="*60)
    print(f"Gemini Model: {GEMINI_MODEL}")
    print(f"Gemini Embedding: {GEMINI_EMBEDDING_MODEL}")
    print(f"Temperature: {GEMINI_TEMPERATURE}")
    print(f"Chunk Size: {CHUNK_SIZE}")
    print(f"Chunk Overlap: {CHUNK_OVERLAP}")
    print(f"Top K Documents: {TOP_K_DOCUMENTS}")
    print(f"PDF Upload Folder: {PDF_UPLOAD_FOLDER}")
    print(f"Supabase Table: {SUPABASE_TABLE_NAME}")
    print(f"Supabase URL: {SUPABASE_URL[:30]}..." if SUPABASE_URL else "Not set")
    print(f"Gemini API Key: {'Set ✅' if GEMINI_API_KEY else 'Not set ❌'}")
    print(f"Supabase Key: {'Set ✅' if SUPABASE_API_KEY else 'Not set ❌'}")
    print("="*60 + "\n")


if __name__ == "__main__":
    display_config()
    validate_config()
