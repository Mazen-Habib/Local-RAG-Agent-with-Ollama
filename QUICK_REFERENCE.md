# 🚀 Quick Reference Card

## ⚡ STEP 1: RAG Agent Setup

### Initial Setup (One-time)
```bash
# 1. Install dependencies
pip install -r requirements_step1.txt

# 2. Create .env file with credentials
# Add: GOOGLE_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_KEY

# 3. Verify setup
python config.py

# 4. Test embedding (optional)
python check_embeddings.py
```

### Upload PDFs
```bash
# All PDFs in pdfs/ folder
python test_upload.py

# Single PDF
python test_upload.py path/to/file.pdf
```

### Ask Questions (Local)
```bash
# Interactive mode
python test_qa.py

# Single question
python test_qa.py "your question here"
```

### Diagnostics
```bash
# Verify embedding dimensions
python check_embedding_dims.py

# Check models available
python check_models.py

# Verify embeddings working
python check_embeddings.py
```

---

## ⚡ STEP 2: WhatsApp Bot Integration

### Start Bot Server
```bash
# Start WhatsApp bot (FastAPI)
python whatsapp_bot.py

# Server runs on: http://localhost:8000
```

### Expose to Internet (Testing)
```bash
# In another terminal, install ngrok
pip install pyngrok

# Or use: ngrok http 8000
```

### Configure Webhook (Meta Dashboard)
```
Webhook URL: https://your-ngrok-url.ngrok.io/webhook/whatsapp
Verify Token: (whatever you set in .env)
```

### Diagnostics
```bash
# Test WhatsApp connection
python diagnose_whatsapp.py

# Check message tracking
python track_messages.py
```

---

## ⚡ STEP 3: Ollama Integration

### Install Ollama
```bash
# Windows: Download from https://ollama.com or
# winget install Ollama.Ollama

# Linux: curl -fsSL https://ollama.com/install.sh | sh

# macOS: brew install ollama
```

### Download Model
```bash
# Pull Llama 3.1 (main LLM)
ollama pull llama3.1

# Pull embedding model (if using separate embeddings)
ollama pull nomic-embed-text
```

### Use Ollama RAG Agent
```bash
# Start the Ollama RAG agent
python rag_agent_ollama.py

# Ask questions with Ollama
python test_qa.py "your question"

# Upload PDFs with Ollama embeddings
python test_upload.py
```

### Check Ollama Status
```bash
# Verify Ollama is running
ollama list

# Check model size
ollama show llama3.1
```

---

## 📋 Environment Variables (.env)

### STEP 1 (Gemini + Supabase)
```env
GOOGLE_API_KEY=AIza...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJh...
```

### STEP 2 (WhatsApp)
```env
WHATSAPP_PHONE_NUMBER_ID=1234567890
WHATSAPP_ACCESS_TOKEN=EAAx...
WHATSAPP_VERIFY_TOKEN=your_verify_token
WEBHOOK_URL=https://your-ngrok-url.ngrok.io
```

### STEP 3 (Ollama)
```env
OLLAMA_MODEL=llama3.1
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 🎯 Configuration (config.py)

### Most Useful Settings
```python
# Gemini Model
GEMINI_MODEL = "gemini-1.5-flash"          # Fast & free tier
# GEMINI_MODEL = "gemini-1.5-pro"          # Better quality

# Chunking
CHUNK_SIZE = 200                            # Smaller = more chunks
CHUNK_OVERLAP = 50                          # Context preservation

# Retrieval
TOP_K_DOCUMENTS = 5                         # More = more context
```

### Ollama Settings (ollama_config.py)
```python
OLLAMA_MODEL = "llama3.1"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"
```

### WhatsApp Settings (whatsapp_config.py)
```python
PHONE_NUMBER_ID = "your_phone_id"
ACCESS_TOKEN = "your_access_token"
VERIFY_TOKEN = "your_verify_token"
```

---

## 🧪 Testing Checklist

### STEP 1
- [ ] `python config.py` → ✅ All config validated
- [ ] `python check_embeddings.py` → ✅ Embeddings working
- [ ] `python test_upload.py` → ✅ PDF uploaded to Supabase
- [ ] `python test_qa.py` → ✅ Q&A working

### STEP 2
- [ ] `python diagnose_whatsapp.py` → ✅ Connection OK
- [ ] `python whatsapp_bot.py` → ✅ Server running
- [ ] Webhook verified in Meta Dashboard → ✅
- [ ] Test message sent → ✅ Response received

### STEP 3 (Ollama)
- [ ] `ollama pull llama3.1` → ✅ Model downloaded
- [ ] `ollama list` → ✅ Model showing
- [ ] Switch config to use Ollama → ✅
- [ ] `python test_qa.py` with Ollama → ✅ Working

---

## 🐛 Quick Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements_step1.txt
```

### "Supabase connection failed"
- Check SUPABASE_URL in .env
- Use **service_role** key (not anon)
- Verify Supabase project is active

### "Gemini API error"
- Check GOOGLE_API_KEY is valid
- Check quota at: https://console.cloud.google.com
- Verify API is enabled

### "WhatsApp webhook not working"
- Check ngrok is running: `ngrok http 8000`
- Verify token in Meta Dashboard
- Check bot is running: `python whatsapp_bot.py`

### "Ollama connection failed"
- Verify Ollama is running: `ollama serve`
- Check OLLAMA_BASE_URL in config
- Verify port 11434 is open

### "Embedding dimensions mismatch"
```bash
python check_embedding_dims.py
# Update EMBEDDING_DIMENSION in config.py to match
```

---

## 📚 Documentation Files

- **PROJECT_STRUCTURE.md** - Overview of all files
- **STEP1_SETUP_GUIDE.md** - Detailed STEP 1 setup
- **STEP2_SETUP_GUIDE.md** - Detailed WhatsApp integration
- **STEP3_SETUP_GUIDE.md** - Detailed Ollama setup
- **UPLOADING_WITH_OLLAMA.md** - Ollama usage guide
- **QUICK_REFERENCE.md** - This file (command reference)
- Check GOOGLE_API_KEY in .env
- Verify key at https://makersuite.google.com
- Check rate limits (15 req/min)

### Error: "No documents found"
```bash
python test_upload.py  # Upload PDFs first
```

---

## 📊 Python Usage Examples

### Upload PDF
```python
from rag_agent import RAGAgent

agent = RAGAgent()
result = agent.process_pdf("file.pdf")
print(f"Stored {result['num_chunks']} chunks")
```

### Ask Question
```python
from rag_agent import RAGAgent

agent = RAGAgent()
result = agent.answer_question("What is this about?")
print(result['answer'])
```

### Check Database
```python
from rag_agent import RAGAgent

agent = RAGAgent()
count = agent.get_document_count()
print(f"Database has {count} documents")
```

---

## 🗄️ Supabase Quick Queries

```sql
-- Count documents
SELECT COUNT(*) FROM documents;

-- View recent uploads
SELECT metadata->>'source', COUNT(*) 
FROM documents 
GROUP BY metadata->>'source';

-- Delete all documents
DELETE FROM documents;

-- Delete specific file
DELETE FROM documents 
WHERE metadata->>'source' = 'filename.pdf';
```

---

## 🎨 Customization Quick Tips

### Use Better Model
```python
# In config.py
GEMINI_MODEL = "gemini-1.5-pro"
```

### Larger Chunks
```python
# In config.py
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
```

### More Context
```python
# In config.py
TOP_K_DOCUMENTS = 10
```

### Custom Prompt
```python
# In config.py
SYSTEM_PROMPT = """Your custom instructions here"""
```

---

## 📁 Folder Structure

```
rag-agent/
├── config.py              # ← Edit settings here
├── rag_agent.py           # ← Core logic
├── test_upload.py         # ← Upload PDFs
├── test_qa.py             # ← Ask questions
├── .env                   # ← Your keys here
├── pdfs/                  # ← Place PDFs here
└── venv/                  # ← Virtual env
```

---

## 🔥 Common Tasks

### Start Fresh
```bash
# Delete all documents in Supabase
# Run in Supabase SQL Editor:
DELETE FROM documents;

# Re-upload PDFs
python test_upload.py
```

### Batch Upload All PDFs
```bash
# Place all PDFs in pdfs/ folder
python test_upload.py
```

### Interactive Chat
```bash
python test_qa.py
# Choose option 1
```

### Test Specific Question
```bash
python test_qa.py "What are the main topics?"
```

---

## 💾 Backup & Restore

### Backup Documents
```sql
-- In Supabase SQL Editor
COPY documents TO '/path/to/backup.csv' CSV HEADER;
```

### Get Table Size
```sql
SELECT 
    pg_size_pretty(pg_total_relation_size('documents')) as total_size,
    COUNT(*) as total_rows
FROM documents;
```

---

## ⚠️ Important Notes

1. **Use service_role key** for Supabase (not anon key)
2. **Gemini free tier**: 15 requests/min (Flash), 2/min (Pro)
3. **Vector dimension**: Must be 768 for Gemini embeddings
4. **Never commit .env** to Git
5. **Activate venv** before running commands

---

## 🎯 Next Steps After STEP 1

1. Verify all tests pass ✅
2. Upload your actual PDFs
3. Test with real questions
4. Move to STEP 2 (WhatsApp) when ready

---

**Keep this card handy for quick reference! 📌**
