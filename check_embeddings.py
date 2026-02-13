"""
Check Embedding Dimensions in Supabase
Verify what dimension your existing embeddings are
"""

from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_SERVICE_KEY")

print("\n" + "="*60)
print("🔍 Checking Embedding Dimensions in Supabase")
print("="*60)

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Get one document with embedding
result = supabase.table("documents").select("embedding, metadata").limit(1).execute()

if not result.data:
    print("\n❌ No documents found in database")
    print("   Upload some PDFs first!")
else:
    doc = result.data[0]
    embedding = doc.get("embedding")
    metadata = doc.get("metadata", {})
    
    if embedding:
        dimension = len(embedding)
        print(f"\n✅ Found document with embedding")
        print(f"   Source: {metadata.get('source', 'Unknown')}")
        print(f"   Embedding Dimension: {dimension}")
        
        # Check if it matches
        if dimension == 768:
            print(f"\n🎉 Perfect! Your embeddings are 768 dimensions")
            print(f"   ✅ Compatible with Ollama's nomic-embed-text")
            print(f"   ✅ No changes needed!")
        else:
            print(f"\n⚠️  Warning: Your embeddings are {dimension} dimensions")
            print(f"   ❌ NOT compatible with nomic-embed-text (768 dims)")
            print(f"\n💡 Solutions:")
            print(f"   1. Delete all documents and re-upload with Ollama")
            print(f"   2. Use a different Ollama embedding model that matches {dimension} dims")
            print(f"   3. Change Supabase vector column to {dimension} dims")
    else:
        print("\n❌ Document has no embedding")
        print("   This shouldn't happen!")

# Check table structure
print(f"\n📊 Checking table structure...")
try:
    # Try to get column info using SQL
    result = supabase.rpc('exec_sql', {
        'query': """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'documents' 
        AND column_name = 'embedding'
        """
    }).execute()
    
    print(f"   Table column info retrieved")
except Exception as e:
    print(f"   Note: Cannot get column info directly")
    print(f"   This is normal - dimension check above is accurate")

print("="*60 + "\n")
