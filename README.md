# 🚀 RAG Agent: Intelligent Document Q&A with WhatsApp Integration

A production-ready **Retrieval-Augmented Generation (RAG)** system that answers questions about your documents using AI. Includes WhatsApp bot integration and support for local Ollama models.

**Features**: PDF processing • Vector embeddings • Semantic search • WhatsApp bot • Gemini/Ollama support • Supabase storage

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📋 Quick Overview

### What Does It Do?

1. **Upload PDFs** → System extracts and stores document chunks as vector embeddings
2. **Ask Questions** → System finds relevant document sections and generates answers using AI
3. **WhatsApp Integration** → Chat with your documents via WhatsApp Business API
4. **Multiple LLMs** → Use Gemini (cloud) or Ollama (local/free)

### Architecture

```
PDFs → Document Chunks → Vector Embeddings → Supabase Storage
                                                    ↓
                                            Semantic Search
                                                    ↓
                                        Gemini/Ollama LLM
                                                    ↓
                                            Generated Answer
```

---

## 🎯 Three Implementation Steps

### ✅ STEP 1: RAG Agent (Gemini + Supabase)
- Upload and process PDFs
- Generate embeddings with Gemini
- Store vectors in Supabase PgVector
- Ask questions and get answers
- **Time to setup**: ~15 minutes

### ✅ STEP 2: WhatsApp Bot Integration
- Connect to WhatsApp Business API
- Send/receive messages
- Maintain conversation context
- Deploy with ngrok for testing
- **Time to setup**: ~30 minutes

### ✅ STEP 3: Ollama Integration (Optional)
- Replace Gemini with local Llama 3.1
- No API costs, no rate limits
- Works offline
- Perfect for privacy-sensitive documents
- **Time to setup**: ~20 minutes

---

## 🔧 Prerequisites

### Requirements

- **Python 3.9+** (check: `python --version`)
- **8GB RAM minimum** (16GB+ for Ollama)
- **10GB disk space** (20GB+ for Ollama)
- **Google Account** (for Gemini API)
- **Meta Business Account** (for WhatsApp - optional)

### Accounts to Create

- 🔑 [Google Cloud](https://console.cloud.google.com) → Get Gemini API key
- 🗄️ [Supabase](https://supabase.com) → Free PostgreSQL + PgVector
- 📱 [Meta Developer](https://developers.facebook.com) → WhatsApp API (optional)

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Local-RAG-Agent-with-Ollama.git
cd Local-RAG-Agent-with-Ollama
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements_step1.txt
```

### 4. Create Environment File

```bash
# Create .env file with your credentials
# Required variables:
GOOGLE_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key_here

# Optional (for WhatsApp)
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_VERIFY_TOKEN=your_verify_token
```

---

## 🚀 Quick Start

### Test Locally (STEP 1)

```bash
# Verify configuration
python config.py
# ✅ Should show all settings validated

# Upload a PDF
python test_upload.py
# Add PDFs to pdfs/ folder first

# Ask a question
python test_qa.py
# Interactive mode - type your question

# Single question
python test_qa.py "What is this document about?"
```

### Deploy WhatsApp Bot (STEP 2)

```bash
# Start the bot server
python whatsapp_bot.py
# Runs on http://localhost:8000

# In another terminal, expose with ngrok
ngrok http 8000

# Add webhook URL to Meta Developer Dashboard
# https://your-ngrok-url/webhook/whatsapp
```

### Use Local Ollama (STEP 3 - Optional)

```bash
# Install Ollama from https://ollama.com
# Then:
ollama pull llama3.1

# Use Ollama RAG agent instead
python rag_agent_ollama.py

# Everything else works the same!
```

---

## 📁 Project Structure

```
Local-RAG-Agent-with-Ollama/
│
├── 📚 STEP 1: RAG Agent
│   ├── config.py                 # Configuration & settings
│   ├── rag_agent.py              # Main RAG implementation (Gemini)
│   ├── test_upload.py            # Upload PDFs
│   ├── test_qa.py                # Ask questions
│   └── supabase_setup.sql        # Database setup
│
├── 📱 STEP 2: WhatsApp Bot
│   ├── whatsapp_bot.py           # FastAPI server
│   ├── whatsapp_client.py        # API client
│   ├── whatsapp_config.py        # Settings
│   ├── webhook_handler.py        # Webhook handler
│   ├── session_manager.py        # Session tracking
│   └── diagnose_whatsapp.py      # Troubleshooting
│
├── 🤖 STEP 3: Ollama Integration
│   ├── rag_agent_ollama.py       # RAG with Ollama
│   ├── ollama_config.py          # Ollama settings
│   └── UPLOADING_WITH_OLLAMA.md  # Ollama guide
│
├── 🔍 Diagnostic Tools
│   ├── check_embeddings.py
│   ├── check_models.py
│   └── check_embedding_dims.py
│
├── 📋 requirements_step1.txt     # Dependencies
├── 📖 PROJECT_STRUCTURE.md       # Detailed overview
├── 📖 QUICK_REFERENCE.md         # Command cheat sheet
│
└── 📚 Setup Guides
    ├── STEP1_SETUP_GUIDE.md      # Detailed STEP 1
    ├── STEP2_SETUP_GUIDE.md      # Detailed STEP 2
    └── STEP3_SETUP_GUIDE.md      # Detailed STEP 3
```

---

## 📖 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet, most useful settings
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Complete file overview
- **[STEP1_SETUP_GUIDE.md](STEP1_SETUP_GUIDE.md)** - Detailed RAG setup
- **[STEP2_SETUP_GUIDE.md](STEP2_SETUP_GUIDE.md)** - WhatsApp integration
- **[STEP3_SETUP_GUIDE.md](STEP3_SETUP_GUIDE.md)** - Ollama installation
- **[UPLOADING_WITH_OLLAMA.md](UPLOADING_WITH_OLLAMA.md)** - Ollama usage guide

---

## 🎯 Configuration

### Model Settings (config.py)

```python
# LLM Model (Gemini)
GEMINI_MODEL = "gemini-1.5-flash"  # Fast & free tier
# GEMINI_MODEL = "gemini-1.5-pro"  # Better quality

# Chunk size (smaller = more chunks)
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

# Number of documents to retrieve
TOP_K_DOCUMENTS = 5
```

### Switch to Ollama (ollama_config.py)

```python
OLLAMA_MODEL = "llama3.1"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"
```

---

## 📊 Key Features

### STEP 1: RAG Agent
✅ PDF processing and chunking  
✅ Vector embeddings (Gemini or Ollama)  
✅ Semantic search in Supabase  
✅ Context-aware question answering  
✅ Source document tracking  
✅ Batch PDF upload  

### STEP 2: WhatsApp Bot
✅ FastAPI server with webhooks  
✅ WhatsApp Business API integration  
✅ Async message handling  
✅ User session management  
✅ Message logging and tracking  
✅ Conversation context preservation  

### STEP 3: Ollama
✅ Local LLM (Llama 3.1)  
✅ Local embeddings (nomic-embed-text)  
✅ No API costs or rate limits  
✅ Works completely offline  
✅ Privacy-friendly  
✅ Custom model support  

---

## 🧪 Testing

### Test STEP 1 (RAG Agent)

```bash
# Verify everything is working
python config.py               # ✅ Should show validation passed
python check_embeddings.py     # ✅ Should show embedding size
python test_upload.py          # ✅ Upload test PDFs
python test_qa.py              # ✅ Ask test questions
```

### Test STEP 2 (WhatsApp)

```bash
python diagnose_whatsapp.py    # ✅ Check configuration
python whatsapp_bot.py         # ✅ Start server
# Then send test message via WhatsApp
```

### Test STEP 3 (Ollama)

```bash
ollama list                    # ✅ Check models installed
python check_models.py         # ✅ Verify in Python
python test_qa.py              # ✅ Test question answering
```

---

## 🐛 Troubleshooting

### "Module not found"
```bash
pip install -r requirements_step1.txt
```

### "Supabase connection failed"
- Verify SUPABASE_URL and SUPABASE_SERVICE_KEY are correct
- Use **service_role** key (not anon key)
- Check Supabase project status

### "Gemini API error"
- Verify GOOGLE_API_KEY in .env
- Check API quota: https://console.cloud.google.com
- Ensure Generative Language API is enabled

### "WhatsApp webhook not connected"
- Verify ngrok is running: `ngrok http 8000`
- Check webhook URL in Meta Dashboard
- Verify verify token matches

### "Ollama connection refused"
- Ensure Ollama is running: `ollama serve`
- Check OLLAMA_BASE_URL in config
- Verify port 11434 is open

### "Embedding dimensions mismatch"
```bash
python check_embedding_dims.py
# Update EMBEDDING_DIMENSION in config.py to match
```

---

## 🔐 Security

### Don't Commit to Git
- `.env` (your secrets)
- `venv/` (virtual environment)
- `pdfs/` (your documents)
- `__pycache__/` (Python cache)

### Use `.gitignore` (already provided)
```
.env
.env.local
venv/
__pycache__/
pdfs/
```

### Best Practices
- ✅ Use environment variables for secrets
- ✅ Use service_role key for Supabase (bypasses RLS)
- ✅ Rotate API keys regularly
- ✅ Never commit .env files
- ✅ Use private GitHub repos for sensitive projects

---

## 📈 Performance Tips

### For Large Documents
```python
CHUNK_SIZE = 500          # Larger chunks = fewer embeddings
CHUNK_OVERLAP = 100       # More context
TOP_K_DOCUMENTS = 10      # Get more similar docs
```

### For Speed
```python
CHUNK_SIZE = 150          # Smaller chunks = faster search
GEMINI_MODEL = "gemini-1.5-flash"  # Faster model
TOP_K_DOCUMENTS = 3       # Retrieve fewer docs
```

### For Quality
```python
GEMINI_MODEL = "gemini-1.5-pro"    # Better understanding
CHUNK_SIZE = 300          # Balance coverage & relevance
TOP_K_DOCUMENTS = 5       # More context
```

### Ollama Optimization
```python
OLLAMA_MODEL = "llama3.1:8b"   # Smaller = faster
# Or larger models if you have GPU:
OLLAMA_MODEL = "llama3.1:70b"  # Better quality
```

---

## 🚀 Deployment

### Local Testing
```bash
python whatsapp_bot.py
ngrok http 8000
```

### Cloud Deployment (Coming Soon)
- Docker containerization
- Deploy to Render/Heroku
- Scale with Kubernetes

---

## 📚 Technology Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | Google Gemini or Ollama (Llama 3.1) |
| **Embeddings** | Gemini Embeddings or nomic-embed-text |
| **Vector DB** | Supabase (PostgreSQL + PgVector) |
| **Web Framework** | FastAPI |
| **Document Processing** | PyPDF |
| **Python Version** | 3.9+ |

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙋 Support

### Getting Help

1. **Check docs**: Browse the [documentation files](.)
2. **Check troubleshooting**: See STEP guides for common issues
3. **Run diagnostics**: Use `check_*.py` scripts to verify setup
4. **Open an issue**: Report bugs on GitHub

### Useful Links

- 🔗 [Gemini API](https://ai.google.dev)
- 🔗 [Supabase Docs](https://supabase.com/docs)
- 🔗 [FastAPI Docs](https://fastapi.tiangolo.com)
- 🔗 [Ollama](https://ollama.com)
- 🔗 [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)

---

## 🎯 Roadmap

- [ ] Web UI dashboard
- [ ] Multiple document sources (URLs, YouTube, etc.)
- [ ] Chat history persistence
- [ ] Multi-user support
- [ ] Advanced RAG techniques (reranking, query expansion)
- [ ] Docker containerization
- [ ] Deployment templates (Render, Heroku, AWS)
- [ ] Analytics and logging

---

## 📞 Contact

For questions or suggestions, open an issue on GitHub.

---

**Built with ❤️ for intelligent document Q&A**

**Star ⭐ this repo if it's helpful!**
