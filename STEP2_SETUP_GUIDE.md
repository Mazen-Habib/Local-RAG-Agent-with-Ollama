# 🚀 STEP 2: WhatsApp Integration Setup Guide

Complete guide for integrating your RAG agent with WhatsApp Business API.

### Related Files
- **whatsapp_bot.py** - Main FastAPI server
- **whatsapp_client.py** - WhatsApp API client
- **whatsapp_config.py** - Configuration settings
- **webhook_handler.py** - Webhook request handling
- **session_manager.py** - User session management
- **track_messages.py** - Message logging
- **diagnose_whatsapp.py** - Troubleshooting tool

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Meta Business Account Setup](#meta-business-account-setup)
3. [WhatsApp Business API Setup](#whatsapp-business-api-setup)
4. [Configuration](#configuration)
5. [Running the Bot](#running-the-bot)
6. [Webhook Setup](#webhook-setup)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### From Step 1 (Must be working)
- ✅ RAG agent initialized
- ✅ Supabase connected
- ✅ Documents uploaded
- ✅ Q&A working locally

### New Requirements
- Meta Business Account
- WhatsApp Business phone number
- Server with public URL (we'll use ngrok for testing)

---

## 📱 Meta Business Account Setup

### Step 1: Create Meta Business Account

1. **Go to**: https://business.facebook.com/
2. **Click**: "Create Account"
3. **Fill in**: Business details
4. **Verify**: Email and identity

### Step 2: Set Up WhatsApp Business

1. **Go to**: https://business.facebook.com/wa/manage/home
2. **Click**: "Get Started" or "Add WhatsApp"
3. **Follow**: Setup wizard

---

## 🔑 WhatsApp Business API Setup

### Step 1: Get API Credentials

1. **Go to**: https://developers.facebook.com/
2. **Click**: "My Apps" → "Create App"
3. **Select**: "Business" type
4. **Add**: WhatsApp product
5. **Go to**: WhatsApp → API Setup

You'll see:
- **Phone Number ID** (copy this)
- **WhatsApp Business Account ID**
- **Temporary Access Token** (we'll generate permanent one)

### Step 2: Generate Permanent Access Token

**Option A: Use Temporary Token (Quick Test)**
- Valid for 24 hours
- Good for initial testing
- Copy from API Setup page

**Option B: Create System User Token (Production)**

1. **Go to**: Business Settings → System Users
2. **Click**: "Add" → Create system user
3. **Give**: Admin role
4. **Click**: "Generate New Token"
5. **Select permissions**:
   - whatsapp_business_messaging
   - whatsapp_business_management
6. **Copy**: The token (save it securely!)

### Step 3: Add Phone Number

1. **In WhatsApp API Setup**:
   - Click "Add phone number"
   - Verify your phone number
   - **Note**: Can't use personal WhatsApp number

2. **For Testing**:
   - Use test number provided by Meta
   - Can send to 5 test numbers (add yours)

3. **For Production**:
   - Need business verification
   - Get dedicated phone number

---

## ⚙️ Configuration

### Step 1: Update .env File

Add WhatsApp credentials to your `.env`:

```env
# WhatsApp Business API
WHATSAPP_API_TOKEN=EAAxxxxxxxxx  # Your access token
WHATSAPP_PHONE_NUMBER_ID=123456789  # Phone number ID from API setup
WHATSAPP_BUSINESS_PHONE=+1234567890  # Your WhatsApp number
WEBHOOK_VERIFY_TOKEN=my_secret_token_xyz  # Any random string you choose
```

### Step 2: Verify Configuration

```powershell
python whatsapp_config.py
```

Should show:
```
✅ WhatsApp configuration validated
```

---

## 🚀 Running the Bot

### Step 1: Install Additional Dependencies

```powershell
pip install fastapi uvicorn
```

### Step 2: Start the Server

```powershell
python whatsapp_bot.py
```

You should see:
```
🚀 Starting WhatsApp RAG Bot
============================================================
1️⃣ Validating configurations...
✅ Configuration validated successfully
✅ WhatsApp configuration validated

2️⃣ Initializing RAG agent...
✅ RAG Agent ready!

3️⃣ Initializing WhatsApp client...
✅ WhatsApp client initialized

4️⃣ Initializing session manager...
✅ Session manager initialized

============================================================
✅ WhatsApp RAG Bot Ready!
============================================================
📊 Documents in database: 25
🌐 Webhook URL: http://your-server-url/webhook
============================================================

🌐 Starting server on 0.0.0.0:8000
📱 Webhook URL: http://0.0.0.0:8000/webhook
```

---

## 🌐 Webhook Setup (Expose to Internet)

WhatsApp needs a **public URL** to send messages to your bot. We'll use **ngrok** for testing.

### Option 1: Using ngrok (Recommended for Testing)

#### Install ngrok

1. **Download**: https://ngrok.com/download
2. **Extract**: The zip file
3. **Sign up**: Create free ngrok account
4. **Get auth token**: From ngrok dashboard
5. **Configure**:
   ```powershell
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

#### Start ngrok Tunnel

**In a NEW terminal** (keep your bot running):

```powershell
ngrok http 8000
```

You'll see:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the `https://abc123.ngrok.io` URL** - this is your public webhook URL!

### Option 2: Using Production Server

For production, deploy to:
- Heroku
- AWS EC2
- DigitalOcean
- Railway
- Render
- etc.

**Requirements**:
- HTTPS (required by WhatsApp)
- Public IP/domain
- Port 443 or 80

---

## 📲 Configure Webhook in Meta

### Step 1: Add Webhook URL

1. **Go to**: WhatsApp → Configuration in Meta Business
2. **Click**: "Edit" next to Webhook
3. **Enter**:
   - **Callback URL**: `https://your-ngrok-url.ngrok.io/webhook`
   - **Verify Token**: Same as `WEBHOOK_VERIFY_TOKEN` in your `.env`
4. **Click**: "Verify and Save"

### Step 2: Subscribe to Webhook Fields

After verification succeeds:

1. **Click**: "Manage" button
2. **Subscribe to**:
   - ✅ messages
3. **Save**

---

## 🧪 Testing

### Test 1: Send Test Message via API

```powershell
# Test sending a message
python whatsapp_client.py
```

Enter your WhatsApp number when prompted. You should receive a test message!

### Test 2: Send Message to Bot

1. **Send a WhatsApp message** to your business number
2. **Check your bot terminal** - you should see:
   ```
   📥 Webhook received: whatsapp_business_account
   📨 Received message from 923335231335: Hello!
   ============================================================
   💬 Processing message from User (923335231335)
      Message: Hello!
   ============================================================
   🔍 Searching for: 'Hello!'
   ✅ Found 5 relevant documents
   🤖 Generating answer...
   ✅ Response sent to User
   ```

3. **You should receive** a response on WhatsApp!

### Test 3: Check Health Endpoint

Open in browser:
```
http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "rag_agent": "ready",
  "whatsapp_client": "ready",
  "session_manager": "ready"
}
```

---

## 🎯 Bot Commands

Your users can send:

| Command | Action |
|---------|--------|
| `Hi` / `Hello` / `/start` | Get welcome message |
| `/clear` | Clear conversation history |
| Any question | Get AI-powered answer from your documents |

---

## 📊 Monitoring

### View Active Sessions

```powershell
# In browser or curl
curl http://localhost:8000/sessions
```

### Cleanup Expired Sessions

```powershell
curl -X POST http://localhost:8000/sessions
```

---

## 🐛 Troubleshooting

### Issue: Webhook Verification Fails

**Check**:
1. Is your server running? (`python whatsapp_bot.py`)
2. Is ngrok running? Check the forwarding URL
3. Is `WEBHOOK_VERIFY_TOKEN` in .env same as in Meta?
4. Check bot terminal for verification logs

**Test webhook manually**:
```powershell
# Should return the challenge
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=test123"
```

### Issue: Not Receiving Messages

**Check**:
1. Webhook subscribed to "messages" field?
2. Bot server running and ngrok active?
3. Check Meta webhook logs (in Configuration)
4. Check your bot terminal for errors

**Test**:
```powershell
# Send test webhook payload
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{test_payload}'
```

### Issue: "Failed to send message"

**Check**:
1. Is `WHATSAPP_API_TOKEN` valid?
2. Is `WHATSAPP_PHONE_NUMBER_ID` correct?
3. Is recipient number added as test number (for test mode)?
4. Check Meta API logs

**Debug**:
```python
python whatsapp_client.py
# Try sending test message
```

### Issue: "No documents found" responses

**Check**:
1. Are documents uploaded in Supabase?
   ```sql
   SELECT COUNT(*) FROM documents;
   ```
2. Is RAG agent connected to Supabase?
3. Try uploading more PDFs

### Issue: Rate Limits

**Gemini**:
- 15 requests/min (free tier)
- Use Ollama to avoid limits

**WhatsApp**:
- Different limits based on business verification
- Check Meta Business Suite for your limits

---

## 🔒 Security Best Practices

### Production Checklist

- [ ] Use permanent access token (not temporary)
- [ ] Store tokens in environment variables
- [ ] Use HTTPS (required)
- [ ] Implement rate limiting
- [ ] Add authentication for admin endpoints
- [ ] Monitor webhook logs
- [ ] Set up error alerting
- [ ] Regular security audits

### Protect Your Tokens

```powershell
# Never commit .env to git
echo ".env" >> .gitignore

# Use environment variables in production
# Don't hardcode tokens
```

---

## 📈 Production Deployment

### Recommended Setup

1. **Server**: Cloud provider (AWS, Azure, GCP, etc.)
2. **HTTPS**: Use Let's Encrypt or cloud provider SSL
3. **Process Manager**: PM2 or systemd
4. **Monitoring**: Set up logging and monitoring
5. **Scaling**: Load balancer if needed

### Example: Deploy to Railway

1. Create account on Railway.app
2. Connect GitHub repo
3. Add environment variables
4. Deploy
5. Use Railway's provided HTTPS URL for webhook

---

## 🎉 Success Checklist

Before considering Step 2 complete:

- [ ] ✅ WhatsApp Business API credentials obtained
- [ ] ✅ Bot server running locally
- [ ] ✅ Webhook verified in Meta
- [ ] ✅ Can send test messages via API
- [ ] ✅ Can receive messages from WhatsApp
- [ ] ✅ Bot responds with RAG answers
- [ ] ✅ Session management working
- [ ] ✅ No errors in logs

---

## ⏭️ What's Next?

**STEP 3: Ollama Integration**
- Replace Gemini with local Llama 3.1
- No more API limits!
- Faster responses
- Complete privacy

---

## 📚 Additional Resources

- **WhatsApp Business API Docs**: https://developers.facebook.com/docs/whatsapp
- **Meta Business Suite**: https://business.facebook.com/
- **ngrok Docs**: https://ngrok.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

**Your WhatsApp RAG bot is ready! 🎊 Test it out and let me know when you're ready for Step 3 (Ollama)!**
