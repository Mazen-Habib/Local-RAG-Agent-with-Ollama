# 🚀 STEP 1: RAG Agent with Gemini & Supabase

Complete setup guide for building a RAG (Retrieval-Augmented Generation) agent using Gemini AI and Supabase vector database.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Supabase Setup](#supabase-setup)
3. [Python Environment Setup](#python-environment-setup)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Usage](#usage)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Accounts

- ✅ **Google Account** (for Gemini API)
- ✅ **Supabase Account** (you already have this)

### Software Requirements

- ✅ Python 3.9 or higher
- ✅ pip (Python package manager)
- ✅ Virtual environment (recommended)

**Check your Python version:**
```bash
python --version
# or
python3 --version
```

---

## 🗄️ Supabase Setup

### Step 1: Verify Your Supabase Project

You mentioned your Supabase is already set up from n8n. Let's verify:

1. **Log in to Supabase**: https://supabase.com/dashboard
2. **Select your project**
3. **Go to**: Project Settings > API

### Step 2: Get Your Credentials

You need two things:

#### A. Supabase URL
- Found in: **Settings > API > Project URL**
- Format: `https://xxxxxxxxxxxxx.supabase.co`
- Copy this!

#### B. Supabase Service Role Key
- Found in: **Settings > API > Project API keys**
- Look for: **service_role** key (NOT the anon key) 
- ⚠️ **Important**: Use service_role key for vector operations
- This key bypasses Row Level Security (needed for vector ops)
- Copy this!

### Step 3: Set Up Database (SQL Editor)

1. **Go to**: SQL Editor in Supabase Dashboard
2. **Click**: "+ New query"
3. **Copy and paste** the contents of `supabase_setup.sql`
4. **Run** the query

This will:
- ✅ Enable pgvector extension
- ✅ Verify your documents table
- ✅ Create vector index for fast searches
- ✅ Create similarity search function

**Verify it worked:**
```sql
-- Run this in SQL Editor
SELECT * FROM match_documents(
    (SELECT embedding FROM documents LIMIT 1),
    5
);
```

If this query runs without errors, you're good! ✅

### Step 4: Understanding Your Table Structure

Your `documents` table has:

| Column | Type | Description |
|--------|------|-------------|
| `id` | int8 | Auto-incrementing ID |
| `content` | text | The actual text chunk |
| `metadata` | jsonb | Source file, page number, etc. |
| `embedding` | vector(768) | 768-dimensional Gemini embedding |

**Important**: Gemini's `embedding-001` model outputs 768-dimensional vectors. Make sure your vector column is `vector(768)`.

---

## 💻 Python Environment Setup

### Step 1: Create Project Directory

```bash
# Create and navigate to your project folder
mkdir rag-agent
cd rag-agent
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**This installs:**
- LangChain (for RAG orchestration)
- Google Gemini (LLM and embeddings)
- Supabase Python client
- PDF processing tools
- Utilities

**Installation time**: ~2-5 minutes depending on your internet

### Step 4: Verify Installation

```bash
python -c "import langchain; import supabase; import google.generativeai; print('✅ All packages installed!')"
```

---

## ⚙️ Configuration

### Step 1: Create .env File

```bash
# Create a new .env file
# On Windows: Create a new file in your editor or notepad
# On macOS/Linux: nano .env
```

### Step 2: Add Your Credentials

Open the `.env` file and fill in:

```env
# Gemini API Key
# Get from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=AIza...your_actual_key_here

# Supabase Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhb...your_actual_service_key_here
```

**Getting Gemini API Key:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy and paste into `.env`

### Step 3: Verify Configuration

```bash
python config.py
```

You should see:
```
✅ Configuration validated successfully
📋 CURRENT CONFIGURATION
...
Gemini API Key: Set ✅
Supabase Key: Set ✅
```

---

## 🧪 Testing

### Test 1: Basic Connection Test

```bash
python rag_agent.py
```

**Expected output:**
```
🚀 Initializing RAG Agent...
✅ Gemini embeddings initialized
✅ Gemini LLM initialized
✅ Supabase client initialized
✅ Text splitter initialized
✅ RAG Agent ready!

✅ Supabase connection successful
📊 Total documents in database: X
```

### Test 2: Upload a PDF

**Option A - Use your own PDF:**
```bash
# Place your PDF in ./pdfs folder
mkdir -p pdfs
# Copy your PDF there

# Run test
python test_upload.py pdfs/your_file.pdf
```

**Option B - Create sample PDF:**
```bash
# First install reportlab
pip install reportlab

# Run test (will create sample PDF)
python test_upload.py
```

**Expected output:**
```
🧪 TEST: PDF Upload and Processing
============================================================
✅ PDF found: your_file.pdf
🚀 Initializing RAG Agent...
✅ Supabase connection successful
============================================================
🔄 Processing PDF: your_file.pdf
============================================================
📄 Loading PDF: your_file.pdf
✅ Loaded 5 pages from PDF
✂️  Splitting documents into chunks...
✅ Created 25 chunks
💾 Storing 25 chunks in Supabase...
🧮 Generating embeddings for 10 texts...
✅ Generated 10 embeddings
  ✅ Stored batch 1 (10 chunks)
...
✅ Successfully stored 25 chunks in Supabase
============================================================
✅ PDF Processing Complete!
   Pages: 5
   Chunks: 25
   Stored: 25
============================================================

✅ TEST PASSED!
```

### Test 3: Ask Questions

**Interactive Mode:**
```bash
python test_qa.py
```

Then choose option 1 for interactive Q&A.

**Single Question:**
```bash
python test_qa.py "What is this document about?"
```

**Expected output:**
```
🧪 TEST: Question Answering
============================================================
🚀 Initializing RAG Agent...
✅ RAG Agent ready!

📊 Total documents in database: 25
============================================================
❓ Question: What is this document about?
============================================================
🔍 Searching for: 'What is this document about?'
✅ Found 5 relevant documents
🤖 Generating answer...
============================================================
✅ Answer Generated
============================================================

This document discusses [answer from Gemini based on your PDFs]

📚 Used 5 source document(s)
============================================================

✅ TEST PASSED!
```

---

## 📖 Usage

### Upload PDFs

```python
from rag_agent import RAGAgent

agent = RAGAgent()

# Process a single PDF
result = agent.process_pdf("path/to/your/file.pdf")

print(f"Processed {result['num_pages']} pages")
print(f"Created {result['num_chunks']} chunks")
```

### Ask Questions

```python
from rag_agent import RAGAgent

agent = RAGAgent()

# Ask a question
result = agent.answer_question("What are the main topics?")

print(f"Answer: {result['answer']}")
print(f"Sources: {result['num_sources']}")

# Access source documents
for source in result['sources']:
    print(f"Content: {source['content']}")
    print(f"Similarity: {source['similarity']}")
```

### Batch Process Multiple PDFs

```python
from pathlib import Path
from rag_agent import RAGAgent

agent = RAGAgent()

# Process all PDFs in a folder
pdf_folder = Path("./pdfs")
for pdf_file in pdf_folder.glob("*.pdf"):
    print(f"Processing {pdf_file.name}...")
    result = agent.process_pdf(str(pdf_file))
    print(f"✅ Stored {result['num_chunks']} chunks")
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Supabase connection failed"

**Check:**
1. Is your SUPABASE_URL correct?
2. Are you using the **service_role** key (not anon key)?
3. Is your Supabase project running?

**Test connection:**
```bash
python -c "from supabase import create_client; import os; from dotenv import load_dotenv; load_dotenv(); client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY')); print('✅ Connected')"
```

### Issue: "Embedding dimension mismatch"

**Problem**: Your vector column might not be 768 dimensions.

**Check your table:**
```sql
SELECT column_name, udt_name 
FROM information_schema.columns 
WHERE table_name = 'documents' AND column_name = 'embedding';
```

**Should show**: `vector(768)`

**If different, recreate table or column:**
```sql
-- Backup first!
ALTER TABLE documents 
ALTER COLUMN embedding TYPE vector(768);
```

### Issue: "Rate limit exceeded"

**Gemini free tier limits:**
- 15 requests/minute (Flash model)
- 2 requests/minute (Pro model)

**Solution**: Wait a minute or upgrade to paid tier.

### Issue: "No documents found"

**Check if PDFs were uploaded:**
```sql
SELECT COUNT(*) FROM documents;
```

If 0, run `python test_upload.py` again.

### Issue: PDF processing fails

**Check:**
1. Is the PDF file readable?
2. Is it a valid PDF format?
3. Try with a simple PDF first

**Debug:**
```python
from rag_agent import RAGAgent

agent = RAGAgent()

# Test loading only
docs = agent.load_pdf("your_file.pdf")
print(f"Loaded {len(docs)} pages")

# Test chunking
chunks = agent.split_documents(docs)
print(f"Created {len(chunks)} chunks")
```

---

## 📊 Performance Tips

### For Large PDFs

Adjust chunk size in `config.py`:
```python
CHUNK_SIZE = 500  # Larger chunks
CHUNK_OVERLAP = 100
```

### For Better Answers

Use more context documents:
```python
TOP_K_DOCUMENTS = 10  # Retrieve more documents
```

### For Faster Processing

Process in larger batches:
```python
# In rag_agent.py
result = agent.store_in_supabase(chunks, source_file, batch_size=20)
```

---

## ✅ Success Checklist

Before moving to Step 2 (WhatsApp integration), verify:

- [ ] ✅ Supabase connection works
- [ ] ✅ Can upload and process PDFs
- [ ] ✅ Can ask questions and get answers
- [ ] ✅ Answers are relevant to uploaded PDFs
- [ ] ✅ No errors in console

**If all checks pass, you're ready for STEP 2!** 🎉

---

## 📚 What's Next?

After completing Step 1:
- **Step 2**: WhatsApp Integration
- **Step 3**: Switch to Ollama (local LLM)

---

## 🆘 Still Need Help?

1. Check error messages carefully
2. Verify all credentials in `.env`
3. Make sure Supabase setup SQL ran successfully
4. Test each component separately
5. Check Supabase logs in dashboard

---

**You've completed STEP 1 setup! Ready to test? 🚀**
