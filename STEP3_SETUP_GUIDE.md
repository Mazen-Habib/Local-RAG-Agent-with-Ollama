# 🚀 STEP 3: Ollama Integration (Local LLM)

Complete guide for switching from Gemini to Ollama (Llama 3.1) for local, unlimited AI inference.

### Related Files
- **rag_agent_ollama.py** - RAG agent using Ollama
- **ollama_config.py** - Ollama configuration
- **UPLOADING_WITH_OLLAMA.md** - Ollama usage guide

---

## 📋 Table of Contents

1. [Why Ollama?](#why-ollama)
2. [Installation](#installation)
3. [Download Models](#download-models)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Update WhatsApp Bot](#update-whatsapp-bot)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Why Ollama?

### Benefits

✅ **No Rate Limits** - Use as much as you want
✅ **Completely Free** - No API costs ever
✅ **Private** - Your data never leaves your machine
✅ **Fast** - No network latency
✅ **Offline** - Works without internet
✅ **No Quotas** - Generate unlimited embeddings

### Requirements

**Minimum:**
- 8GB RAM
- 10GB free disk space

**Recommended:**
- 16GB+ RAM
- NVIDIA GPU (optional, for faster inference)
- 20GB free disk space

---

## 💻 Installation

### Windows

**Option 1: Download Installer (Easiest)**

1. **Go to**: https://ollama.com/download
2. **Click**: Download for Windows
3. **Run**: The installer
4. **Done!** Ollama runs in the background

**Option 2: Using winget**

```powershell
winget install Ollama.Ollama
```

**Verify Installation:**

```powershell
ollama --version
```

Should show: `ollama version 0.x.x`

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Start Ollama service:**

```bash
ollama serve
```

### macOS

```bash
# Download from website
open https://ollama.com/download

# Or use Homebrew
brew install ollama
```

---

## 📥 Download Models

### Step 1: Download Llama 3.1 (Main LLM)

```powershell
ollama pull llama3.1
```

**This downloads ~4.7GB**. Wait for it to complete.

**Alternative models** (if llama3.1 is too large):
```powershell
# Smaller, faster
ollama pull llama3.1:8b

# Better quality (needs ~40GB RAM)
ollama pull llama3.1:70b

# Or use Mistral (good alternative)
ollama pull mistral
```

### Step 2: Download Embedding Model

```powershell
ollama pull nomic-embed-text
```

**This downloads ~274MB**.

**Why nomic-embed-text?**
- ✅ 768 dimensions (same as Gemini!)
- ✅ No Supabase schema changes needed
- ✅ High quality embeddings
- ✅ Fast inference

**Alternative embedding models:**
```powershell
# Smaller, faster (384 dims - requires schema change)
ollama pull all-minilm

# Higher quality (1024 dims - requires schema change)
ollama pull mxbai-embed-large
```

### Step 3: Verify Models

```powershell
ollama list
```

Should show:
```
NAME                    SIZE
llama3.1:latest        4.7 GB
nomic-embed-text:latest  274 MB
```

---

## ⚙️ Configuration

### Step 1: No .env Changes Needed!

Ollama runs locally, so no API keys required. Your `.env` stays the same.

### Step 2: Check Ollama is Running

**Windows**: Check system tray - you should see Ollama icon

**Linux/Mac**:
```bash
# Check if running
ps aux | grep ollama

# If not running, start it
ollama serve
```

### Step 3: Test Ollama API

```powershell
# Test LLM
ollama run llama3.1 "Say hello in 5 words"

# Test embedding
python -c "from langchain_community.embeddings import OllamaEmbeddings; e = OllamaEmbeddings(model='nomic-embed-text'); print(len(e.embed_query('test')))"
```

Should output: `768` (embedding dimension)

---

## 🧪 Testing

### Test 1: Verify Ollama Configuration

```powershell
python ollama_config.py
```

Expected output:
```
🔍 Validating Ollama Configuration
============================================================
1️⃣ Checking Ollama server at http://localhost:11434...
✅ Ollama server is running

2️⃣ Available models (2):
   - llama3.1:latest
   - nomic-embed-text:latest

3️⃣ Checking required models...
✅ LLM model 'llama3.1' found
✅ Embedding model 'nomic-embed-text' found
============================================================
```

### Test 2: Test RAG Agent with Ollama

```powershell
python rag_agent_ollama.py
```

Expected output:
```
🚀 Initializing RAG Agent with Ollama...
✅ Ollama embeddings initialized (nomic-embed-text)
✅ Ollama LLM initialized (llama3.1)
✅ Supabase client initialized
✅ Text splitter initialized (chunk_size=200)
✅ RAG Agent ready!

✅ Supabase connection successful
📊 Total documents in database: 25
```

### Test 3: Upload PDF with Ollama

Create a test script:

```powershell
# Create test_upload_ollama.py
```

```python
from rag_agent_ollama import RAGAgentOllama

agent = RAGAgentOllama()
result = agent.process_pdf("pdfs/your_file.pdf")
print(f"✅ Processed {result['num_chunks']} chunks")
```

Run it:
```powershell
python test_upload_ollama.py
```

### Test 4: Ask Questions with Ollama

Create a test script:

```powershell
# Create test_qa_ollama.py
```

```python
from rag_agent_ollama import RAGAgentOllama

agent = RAGAgentOllama()
result = agent.answer_question("What is this document about?")
print(f"Answer: {result['answer']}")
```

Run it:
```powershell
python test_qa_ollama.py
```

---

## 🔄 Update WhatsApp Bot

### Option 1: Quick Switch (Modify Existing)

**Edit `whatsapp_bot.py`:**

Change line 15:
```python
# OLD:
from rag_agent import RAGAgent

# NEW:
from rag_agent_ollama import RAGAgentOllama as RAGAgent
```

That's it! Your WhatsApp bot now uses Ollama!

### Option 2: Keep Both (Recommended)

You can switch between Gemini and Ollama by using environment variable:

**Edit `whatsapp_bot.py`** at the top:

```python
import os
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"

if USE_OLLAMA:
    from rag_agent_ollama import RAGAgentOllama as RAGAgent
    print("🤖 Using Ollama (Local LLM)")
else:
    from rag_agent import RAGAgent
    print("🌐 Using Gemini (Cloud API)")
```

**Add to `.env`:**
```env
USE_OLLAMA=true  # Set to false to use Gemini
```

### Restart WhatsApp Bot

```powershell
# Stop the current bot (Ctrl+C)

# Restart with Ollama
python whatsapp_bot.py
```

You should see:
```
🤖 Using Ollama (Local LLM)
🚀 Initializing RAG Agent with Ollama...
```

---

## ⚡ Performance Optimization

### For Faster Responses

**Edit `ollama_config.py`:**

```python
# Reduce max tokens for faster generation
OLLAMA_MAX_TOKENS = 512  # Instead of 2048

# Use smaller context
OLLAMA_CONTEXT_LENGTH = 2048  # Instead of 4096

# Lower temperature for more focused answers
OLLAMA_TEMPERATURE = 0.3  # Instead of 0.7
```

### For Better Quality

```python
# Use more tokens
OLLAMA_MAX_TOKENS = 4096

# Higher context
OLLAMA_CONTEXT_LENGTH = 8192

# More creative
OLLAMA_TEMPERATURE = 0.8
```

### GPU Acceleration (NVIDIA Only)

If you have an NVIDIA GPU:

**Edit `ollama_config.py`:**

```python
# Use all GPU layers
OLLAMA_NUM_GPU = -1
```

This makes inference **10-50x faster**!

**Check GPU usage:**
```powershell
nvidia-smi
```

---

## 📊 Comparison: Ollama vs Gemini

| Feature | Gemini | Ollama |
|---------|--------|--------|
| **Cost** | Free tier (limited) | Completely free |
| **Rate Limits** | 15 req/min | Unlimited |
| **Speed** | Fast (cloud) | Varies (local) |
| **Privacy** | Data sent to Google | 100% private |
| **Offline** | ❌ No | ✅ Yes |
| **Quality** | Excellent | Very good |
| **Setup** | Easy (API key) | Requires install |
| **Requirements** | Internet | 8GB+ RAM |

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Ollama server"

**Check if Ollama is running:**

Windows:
- Look for Ollama icon in system tray
- If not there, start Ollama app

Linux/Mac:
```bash
ollama serve
```

**Test connection:**
```powershell
curl http://localhost:11434/api/tags
```

Should return list of models.

### Issue: "Model not found"

**List installed models:**
```powershell
ollama list
```

**Install missing model:**
```powershell
ollama pull llama3.1
ollama pull nomic-embed-text
```

### Issue: "Out of memory"

**Solutions:**

1. **Use smaller model:**
   ```powershell
   ollama pull llama3.1:8b
   ```

2. **Reduce context:**
   ```python
   # In ollama_config.py
   OLLAMA_CONTEXT_LENGTH = 2048
   ```

3. **Close other applications**

4. **Upgrade RAM** (if possible)

### Issue: "Slow responses"

**Causes & Solutions:**

1. **CPU-only inference** (no GPU)
   - Expected on CPU
   - Consider using GPU or smaller model

2. **Large model**
   - Use `llama3.1:8b` instead of `llama3.1:70b`

3. **High context length**
   - Reduce `OLLAMA_CONTEXT_LENGTH`

**Benchmark:**
```powershell
# Time a query
python -c "import time; from rag_agent_ollama import RAGAgentOllama; agent = RAGAgentOllama(); start = time.time(); agent.answer_question('test'); print(f'Time: {time.time()-start:.2f}s')"
```

### Issue: "Embeddings dimension mismatch"

If you use a different embedding model:

**Check dimension:**
```python
from langchain_community.embeddings import OllamaEmbeddings
e = OllamaEmbeddings(model='your-model')
print(len(e.embed_query('test')))
```

**Update Supabase:**
```sql
-- If dimension is different from 768
ALTER TABLE documents 
ALTER COLUMN embedding TYPE vector(NEW_DIMENSION);
```

---

## 🎯 Model Recommendations

### For Limited RAM (8GB)

```powershell
ollama pull llama3.1:8b  # Smaller version
ollama pull all-minilm   # Lighter embedding
```

### For Better Quality (16GB+)

```powershell
ollama pull llama3.1     # Default (best balance)
ollama pull nomic-embed-text
```

### For Maximum Quality (32GB+)

```powershell
ollama pull llama3.1:70b
ollama pull mxbai-embed-large
```

### For Code/Technical Docs

```powershell
ollama pull codellama
ollama pull nomic-embed-text
```

---

## ✅ Success Checklist

- [ ] ✅ Ollama installed and running
- [ ] ✅ llama3.1 model downloaded
- [ ] ✅ nomic-embed-text model downloaded
- [ ] ✅ ollama_config.py validation passes
- [ ] ✅ Can process PDFs with Ollama
- [ ] ✅ Can answer questions with Ollama
- [ ] ✅ WhatsApp bot updated to use Ollama
- [ ] ✅ No rate limit errors
- [ ] ✅ Responses are good quality

---

## 🎉 Benefits You Now Have

✅ **Unlimited Usage** - No more rate limits!
✅ **No API Costs** - Completely free forever
✅ **Privacy** - All data stays local
✅ **Offline** - Works without internet
✅ **Fast** - No network latency
✅ **Flexible** - Switch models anytime

---

## 📚 Additional Resources

- **Ollama Website**: https://ollama.com/
- **Ollama GitHub**: https://github.com/ollama/ollama
- **Model Library**: https://ollama.com/library
- **Llama 3.1 Docs**: https://ollama.com/library/llama3.1

---

**Congratulations! 🎊 You now have a complete, production-ready RAG system with:**
- ✅ Local LLM (Ollama)
- ✅ Vector Database (Supabase)  
- ✅ WhatsApp Integration
- ✅ No API costs or limits!

**Your RAG agent is complete! 🚀**
