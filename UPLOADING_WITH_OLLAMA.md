# 📤 Uploading PDFs with Ollama Embeddings

Complete guide for uploading PDFs with the correct embedding dimensions (768).

---

## ✅ Good News!

**Both Gemini and Ollama use 768 dimensions!**

| Model | Dimensions |
|-------|------------|
| Gemini embedding-001 | 768 |
| Ollama nomic-embed-text | 768 |

This means you can **mix and match**:
- Upload some PDFs with Gemini
- Upload others with Ollama
- They all work together!

---

## 🔍 Step 1: Check Your Current Embeddings

Run this script to verify what you have:

```powershell
python check_embeddings.py
```

**Expected output:**
```
🔍 Checking Embedding Dimensions in Supabase
============================================================
✅ Found document with embedding
   Source: your_file.pdf
   Embedding Dimension: 768

🎉 Perfect! Your embeddings are 768 dimensions
   ✅ Compatible with Ollama's nomic-embed-text
   ✅ No changes needed!
============================================================
```

If you see **768** → You're all set! ✅

---

## 📤 Step 2: Upload PDFs with Ollama

### Option A: Use Existing Test Script (Modified)

Create `test_upload_ollama.py`:

```python
"""
Upload PDFs using Ollama embeddings
"""

import os
import sys
from pathlib import Path

from rag_agent_ollama import RAGAgentOllama
from config import PDF_UPLOAD_FOLDER


def upload_pdf_with_ollama(pdf_path: str):
    """Upload a single PDF with Ollama embeddings"""
    
    print("\n" + "="*60)
    print("📤 Uploading PDF with Ollama Embeddings")
    print("="*60)
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"✅ PDF found: {pdf_path}")
    
    # Initialize RAG agent with Ollama
    print("\n🤖 Initializing RAG agent with Ollama...")
    agent = RAGAgentOllama()
    
    # Process PDF
    result = agent.process_pdf(pdf_path)
    
    if result["status"] == "success":
        print("\n✅ Upload Complete!")
        print(f"   File: {result['source_file']}")
        print(f"   Pages: {result['num_pages']}")
        print(f"   Chunks: {result['num_chunks']}")
        print(f"   Stored: {result['num_stored']}")
        print(f"   Embedding Model: nomic-embed-text (768 dims)")
        return True
    else:
        print("❌ Upload failed")
        return False


def upload_all_pdfs_in_folder(folder: str = PDF_UPLOAD_FOLDER):
    """Upload all PDFs in a folder"""
    
    pdf_files = list(Path(folder).glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  No PDF files found in {folder}")
        return
    
    print(f"\n📄 Found {len(pdf_files)} PDF file(s)")
    
    # Initialize agent once
    agent = RAGAgentOllama()
    
    # Process each PDF
    for pdf_path in pdf_files:
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path.name}")
        print(f"{'='*60}")
        
        try:
            result = agent.process_pdf(str(pdf_path))
            print(f"✅ {pdf_path.name} uploaded successfully!")
        except Exception as e:
            print(f"❌ Failed to upload {pdf_path.name}: {str(e)}")
    
    print(f"\n{'='*60}")
    print("✅ Batch upload complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Upload specific PDF
        pdf_path = sys.argv[1]
        upload_pdf_with_ollama(pdf_path)
    else:
        # Upload all PDFs in folder
        upload_all_pdfs_in_folder()
```

**Usage:**

```powershell
# Upload specific PDF
python test_upload_ollama.py pdfs/myfile.pdf

# Upload all PDFs in pdfs/ folder
python test_upload_ollama.py
```

### Option B: Use Python Directly

```python
from rag_agent_ollama import RAGAgentOllama

# Initialize agent
agent = RAGAgentOllama()

# Upload PDF
result = agent.process_pdf("path/to/your/file.pdf")

print(f"Uploaded {result['num_chunks']} chunks with 768-dim embeddings")
```

---

## 🔄 What If You Have MIXED Dimensions?

### Scenario: Some PDFs with different dimensions

**Check what you have:**

```sql
-- Run in Supabase SQL Editor
SELECT 
    metadata->>'source' as source_file,
    array_length(embedding, 1) as dimension,
    COUNT(*) as num_chunks
FROM documents
GROUP BY metadata->>'source', array_length(embedding, 1)
ORDER BY source_file;
```

**If you see different dimensions:**

```
source_file     | dimension | num_chunks
----------------|-----------|------------
old_file.pdf    | 384       | 25
new_file.pdf    | 768       | 30
```

**Solutions:**

#### Option 1: Start Fresh (Recommended if you have few documents)

```sql
-- Delete all documents
DELETE FROM documents;
```

Then re-upload everything with Ollama:
```powershell
python test_upload_ollama.py
```

#### Option 2: Delete Only Non-768 Documents

```sql
-- Delete documents that don't have 768 dimensions
DELETE FROM documents
WHERE array_length(embedding, 1) != 768;
```

#### Option 3: Keep Separate Tables

Create a new table for 768-dim embeddings:

```sql
-- Create new table
CREATE TABLE documents_768 (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(768)
);

-- Create index
CREATE INDEX documents_768_embedding_idx 
ON documents_768 
USING hnsw (embedding vector_cosine_ops);

-- Create search function
CREATE OR REPLACE FUNCTION match_documents_768(
    query_embedding VECTOR(768),
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id BIGINT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        documents_768.id,
        documents_768.content,
        documents_768.metadata,
        1 - (documents_768.embedding <=> query_embedding) AS similarity
    FROM documents_768
    ORDER BY documents_768.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

Then update `config.py`:
```python
SUPABASE_TABLE_NAME = "documents_768"
SUPABASE_QUERY_NAME = "match_documents_768"
```

---

## 🧪 Verify Upload

After uploading with Ollama, verify:

```powershell
# Check embeddings
python check_embeddings.py

# Test query
python -c "from rag_agent_ollama import RAGAgentOllama; agent = RAGAgentOllama(); result = agent.answer_question('test'); print(result['answer'])"
```

---

## 📊 Embedding Model Comparison

### Ollama Models

| Model | Dimensions | Size | Speed | Quality |
|-------|------------|------|-------|---------|
| **nomic-embed-text** | **768** | 274MB | Fast | Good |
| all-minilm | 384 | 45MB | Very Fast | Okay |
| mxbai-embed-large | 1024 | 670MB | Slow | Best |

### Why nomic-embed-text is Recommended

✅ **768 dimensions** (same as Gemini!)
✅ **Good balance** of speed and quality
✅ **Small size** (274MB)
✅ **No schema changes** needed

---

## 🔧 If You Want to Use Different Embedding Model

### Example: Using all-minilm (384 dims)

**Step 1: Download model**
```powershell
ollama pull all-minilm
```

**Step 2: Update Supabase schema**
```sql
-- Change vector dimension
ALTER TABLE documents 
ALTER COLUMN embedding TYPE vector(384);

-- Recreate index
DROP INDEX IF EXISTS documents_embedding_idx;
CREATE INDEX documents_embedding_idx 
ON documents 
USING hnsw (embedding vector_cosine_ops);

-- Update function
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding VECTOR(384),  -- Changed from 768
    match_count INT DEFAULT 5
)
-- ... rest of function
```

**Step 3: Update config**
```python
# In ollama_config.py
OLLAMA_EMBEDDING_MODEL = "all-minilm"
EMBEDDING_DIMENSION = 384
```

**Step 4: Delete old documents and re-upload**
```sql
DELETE FROM documents;
```

```powershell
python test_upload_ollama.py
```

---

## ✅ Best Practice Workflow

**For New Projects:**
1. ✅ Choose one embedding model (nomic-embed-text recommended)
2. ✅ Set up Supabase with correct dimensions (768)
3. ✅ Upload all PDFs with same model
4. ✅ Stick with it!

**For Existing Projects:**
1. ✅ Check current dimensions (`python check_embeddings.py`)
2. ✅ If 768 → Continue using Ollama nomic-embed-text
3. ✅ If different → Decide to migrate or use different model

---

## 🎯 Quick Commands

```powershell
# Check what you have
python check_embeddings.py

# Upload single PDF with Ollama
python test_upload_ollama.py pdfs/myfile.pdf

# Upload all PDFs with Ollama
python test_upload_ollama.py

# Test query with Ollama
python -c "from rag_agent_ollama import RAGAgentOllama; agent = RAGAgentOllama(); print(agent.answer_question('test')['answer'])"
```

---

## 💡 Summary

**You're all set if:**
- ✅ Your existing embeddings are 768 dims
- ✅ You're using Ollama nomic-embed-text (768 dims)
- ✅ Just use `rag_agent_ollama.py` to upload new PDFs

**No changes needed to Supabase!** 🎉

---

**Need help? Let me know!** 🚀
