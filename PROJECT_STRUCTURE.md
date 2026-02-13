# 📁 RAG Agent Project Structure

## 📁 Complete Project Structure

```
New RAg/
│
├── 🚀 STEP 1: Gemini + Supabase RAG
│   ├── 📄 config.py                    # Configuration and settings
│   ├── 🤖 rag_agent.py                 # Core RAG agent (Gemini)
│   ├── 🧪 test_upload.py               # Test PDF upload
│   ├── 🧪 test_qa.py                   # Test Q&A
│   ├── 🗄️ supabase_setup.sql          # Database setup SQL
│   ├── 📚 STEP1_SETUP_GUIDE.md        # Setup instructions
│   │
│   ├── 🚀 STEP 2: WhatsApp Integration
│   ├── 📱 whatsapp_bot.py              # Main WhatsApp bot server
│   ├── 🔗 whatsapp_client.py           # WhatsApp API client
│   ├── ⚙️  whatsapp_config.py          # WhatsApp configuration
│   ├── 🪝 webhook_handler.py           # Webhook handling
│   ├── 💾 session_manager.py           # Session management
│   ├── 📊 track_messages.py            # Message tracking
│   ├── 🔍 diagnose_whatsapp.py         # Troubleshooting tool
│   ├── 📚 STEP2_SETUP_GUIDE.md        # WhatsApp setup
│   │
│   ├── 🚀 STEP 3: Ollama Integration
│   ├── 🤖 rag_agent_ollama.py          # RAG agent with Ollama
│   ├── ⚙️  ollama_config.py            # Ollama configuration
│   ├── 📤 UPLOADING_WITH_OLLAMA.md     # Ollama usage guide
│   ├── 📚 STEP3_SETUP_GUIDE.md        # Ollama setup
│   │
│   ├── 📋 requirements_step1.txt       # Python dependencies
│   ├── 🔍 check_embedding_dims.py      # Verify embedding dimensions
│   ├── 🔍 check_embeddings.py          # Check embeddings
│   ├── 🔍 check_models.py              # Verify model setup
│   ├── 📖 PROJECT_STRUCTURE.md         # This file
│   ├── 📖 QUICK_REFERENCE.md           # Command reference
│   │
│   ├── pdfs/                           # Your PDF files
│   │
│   ├── venv/                           # Virtual environment
│   │
│   └── .env                            # Your credentials (git ignored)
```

---

## 🎯 File Descriptions

### STEP 1: RAG Agent Files

**config.py**
- Central configuration management
- Loads environment variables (.env)
- Validates settings and credentials
- Displays current configuration
- Contains customizable parameters

**rag_agent.py**
- Main RAG agent with Gemini
- PDF loading and processing
- Document chunking
- Embedding generation (Gemini embeddings)
- Vector storage in Supabase
- Similarity search and retrieval
- Question answering pipeline

**test_upload.py**
- Test PDF upload functionality
- Process single or multiple PDFs
- Verify Supabase storage
- Create sample PDFs for testing

**test_qa.py**
- Test question answering system
- Interactive Q&A mode
- Single question testing
- Display source documents

**supabase_setup.sql**
- Enable pgvector extension
- Create documents table
- Create vector similarity function
- Comprehensive documentation

**requirements_step1.txt**
- All Python dependencies
- LangChain packages
- Gemini integration
- Supabase client
- PDF processing tools

### STEP 2: WhatsApp Integration Files

**whatsapp_bot.py**
- Main FastAPI WhatsApp bot server
- Webhook endpoints for incoming messages
- Async message handling
- Integrates with RAG agent
- Response routing

**whatsapp_client.py**
- WhatsApp Business API client
- Send messages
- Send media files
- Handle API requests/responses
- Error handling

**whatsapp_config.py**
- WhatsApp configuration settings
- Phone number ID
- Access tokens
- Webhook settings

**webhook_handler.py**
- Webhook request validation
- Signature verification
- Message parsing
- Status callbacks

**session_manager.py**
- User session management
- Conversation context tracking
- Session persistence

**track_messages.py**
- Message logging and tracking
- Database storage
- Message history management

**diagnose_whatsapp.py**
- Troubleshooting tool
- Connection testing
- Configuration validation

### STEP 3: Ollama Integration Files

**rag_agent_ollama.py**
- RAG agent with local Ollama
- Ollama embeddings
- Llama 3.1 LLM integration
- Offline inference

**ollama_config.py**
- Ollama configuration
- Model settings
- Performance tuning

**UPLOADING_WITH_OLLAMA.md**
- Guide for using Ollama
- Model management
- Performance tips

### Diagnostic & Reference Files

**check_embedding_dims.py**
- Verify embedding dimensions match

**check_embeddings.py**
- Test embedding generation

**check_models.py**
- Verify model availability

**STEP1_SETUP_GUIDE.md**
- Complete STEP 1 setup instructions
- Supabase configuration
- Testing procedures

**STEP2_SETUP_GUIDE.md**
- WhatsApp integration setup
- Meta Business account configuration
- Webhook setup

**STEP3_SETUP_GUIDE.md**
- Ollama installation and setup
- Model downloading
- Configuration

**QUICK_REFERENCE.md**
- Common commands cheat sheet
- Quick troubleshooting

**PROJECT_STRUCTURE.md**
- This file - project overview

---

## 🚀 Complete Workflow

### STEP 1: RAG Setup (One-time)

```bash
# 1. Install dependencies
pip install -r requirements_step1.txt

# 2. Create .env file
# Add your GOOGLE_API_KEY and Supabase credentials

# 3. Run Supabase SQL setup
# Copy supabase_setup.sql to Supabase SQL Editor

# 4. Verify configuration
python config.py

# 5. Test with sample question
python test_qa.py "What is in the documents?"
```

### STEP 2: WhatsApp Integration

```bash
# Start the WhatsApp bot server
python whatsapp_bot.py

# The server runs on http://localhost:8000
# Use ngrok to expose webhook: ngrok http 8000
```

### STEP 3: Switch to Ollama (Optional)

```bash
# 1. Install Ollama from https://ollama.com
# 2. Download model: ollama pull llama3.1
# 3. Use rag_agent_ollama.py instead of rag_agent.py
```

---

## 🚀 Quick Start Workflow

### 1. Setup (One-time)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements_step1.txt

# 3. Create .env file with your credentials
# GOOGLE_API_KEY=...
# SUPABASE_URL=...
# SUPABASE_SERVICE_KEY=...

# 4. Run Supabase SQL setup
# Copy supabase_setup.sql contents to Supabase SQL Editor and run

# 5. Verify configuration
python config.py
```

### 2. Upload PDFs

```bash
# Create pdfs folder
mkdir pdfs

# Place your PDF files in pdfs/

# Process all PDFs in folder
python test_upload.py

# Or process a single PDF
python test_upload.py pdfs/your_file.pdf
```

### 3. Ask Questions (Local Testing)

```bash
# Interactive mode
python test_qa.py

# Single question
python test_qa.py "What is this document about?"
```

### 4. Deploy WhatsApp Bot (Optional)

```bash
# Start the bot
python whatsapp_bot.py

# Expose to internet (in another terminal)
ngrok http 8000

# Add webhook URL to Meta Developer Dashboard
```

### 5. Switch to Ollama (Optional)

```bash
# 1. Install Ollama
# 2. Download model
ollama pull llama3.1

# 3. Use Ollama RAG agent instead
python rag_agent_ollama.py
```

---

## 🔧 Customization

### Change Chunk Size

Edit `config.py`:
```python
CHUNK_SIZE = 500      # Make chunks larger
CHUNK_OVERLAP = 100   # Increase overlap
```

### Change Model

Edit `config.py`:
```python
GEMINI_MODEL = "gemini-1.5-pro"  # Use more powerful model
```

### Change Number of Retrieved Documents

Edit `config.py`:
```python
TOP_K_DOCUMENTS = 10  # Retrieve more context
```

### Modify System Prompt

Edit `config.py`:
```python
SYSTEM_PROMPT = """Your custom prompt here..."""
```

---

## 📊 Data Flow

### PDF Upload Flow
```
PDF File → load_pdf()
    ↓
Document Pages → split_documents()
    ↓
Text Chunks → generate_embeddings()
    ↓
Embeddings → store_in_supabase()
    ↓
Supabase documents table
```

### Question Answering Flow
```
User Question → generate_embeddings()
    ↓
Query Embedding → similarity_search()
    ↓
Retrieve Top-K Documents → answer_question()
    ↓
Context + Question → Gemini LLM
    ↓
Generated Answer with Sources
```

---

## 🗄️ Supabase Table Schema

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(768)
);

-- Metadata structure:
{
    "source": "filename.pdf",
    "page": 1,
    ... other fields
}
```

---

## 🎯 Next Steps

After completing STEP 1:

**STEP 2: WhatsApp Integration**
- Connect to WhatsApp Business API
- Handle incoming messages
- Send responses
- Maintain conversation context

**STEP 3: Ollama Integration**
- Replace Gemini with local Ollama
- Use llama3.1 model
- Update embeddings to Ollama

---

## 📝 Notes

### Important Files to NOT Commit to Git

- `.env` (contains secrets)
- `venv/` (virtual environment)
- `pdfs/` (your documents)
- `__pycache__/` (Python cache)

### Files to Keep in Version Control

- All `.py` files
- `.sql` files
- `.md` documentation
- `requirements_step1.txt`

---

## 🔒 Security

**Never commit these to Git:**
- GOOGLE_API_KEY
- SUPABASE_SERVICE_KEY
- Any `.env` file with real credentials

**Use `.gitignore`:**
```
.env
venv/
__pycache__/
*.pyc
pdfs/
```

---

## 💡 Tips

1. **Test incrementally**: Test each component separately before running the full pipeline
2. **Start small**: Test with small PDFs first (1-5 pages)
3. **Check logs**: Always check console output for errors
4. **Use virtual environment**: Keeps dependencies isolated
5. **Monitor Supabase**: Check table size in Supabase dashboard
6. **Rate limits**: Be aware of Gemini free tier limits

---

**Ready to start? Follow STEP1_SETUP_GUIDE.md! 🚀**
