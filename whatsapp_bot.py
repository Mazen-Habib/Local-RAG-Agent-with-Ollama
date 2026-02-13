"""
WhatsApp RAG Bot - FastAPI Application
Main webhook server for receiving and responding to WhatsApp messages
"""

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
from typing import Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
# from rag_agent import RAGAgent
from whatsapp_client import WhatsAppClient
from session_manager import SessionManager
from whatsapp_config import (
    WEBHOOK_VERIFY_TOKEN,
    WELCOME_MESSAGE,
    NO_DOCUMENTS_MESSAGE,
    ERROR_MESSAGE,
    validate_whatsapp_config,
)
from config import validate_config
# new changes
import os
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"

if USE_OLLAMA:
    from rag_agent_ollama import RAGAgentOllama as RAGAgent
else:
    from rag_agent import RAGAgent

    
# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp RAG Bot",
    description="RAG-powered AI assistant for WhatsApp",
    version="1.0.0"
)

# Global instances
rag_agent: RAGAgent = None
whatsapp_client: WhatsAppClient = None
session_manager: SessionManager = None
executor = ThreadPoolExecutor(max_workers=5)


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    global rag_agent, whatsapp_client, session_manager
    
    print("\n" + "="*60)
    print("🚀 Starting WhatsApp RAG Bot")
    print("="*60)
    
    # Validate configurations
    print("\n1️⃣ Validating configurations...")
    if not validate_config():
        raise Exception("Configuration validation failed")
    
    if not validate_whatsapp_config():
        raise Exception("WhatsApp configuration validation failed")
    
    # Initialize RAG agent
    print("\n2️⃣ Initializing RAG agent...")
    rag_agent = RAGAgent()
    
    # Check document count
    doc_count = rag_agent.get_document_count()
    if doc_count == 0:
        print("⚠️  Warning: No documents in database!")
        print("   Upload PDFs using: python test_upload.py")
    
    # Initialize WhatsApp client
    print("\n3️⃣ Initializing WhatsApp client...")
    whatsapp_client = WhatsAppClient()
    
    # Initialize session manager
    print("\n4️⃣ Initializing session manager...")
    session_manager = SessionManager()
    
    print("\n" + "="*60)
    print("✅ WhatsApp RAG Bot Ready!")
    print("="*60)
    print(f"📊 Documents in database: {doc_count}")
    print("🌐 Webhook URL: http://your-server-url/webhook")
    print("="*60 + "\n")


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "running",
        "service": "WhatsApp RAG Bot",
        "version": "1.0.0",
        "documents": rag_agent.get_document_count() if rag_agent else 0,
        "active_sessions": session_manager.get_active_sessions_count() if session_manager else 0
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_agent": "ready" if rag_agent else "not initialized",
        "whatsapp_client": "ready" if whatsapp_client else "not initialized",
        "session_manager": "ready" if session_manager else "not initialized"
    }


@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Webhook verification endpoint
    Meta will call this to verify your webhook
    """
    # Get query parameters
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    print(f"🔍 Webhook verification request received")
    print(f"   Mode: {mode}")
    print(f"   Token: {token}")
    
    # Verify the webhook
    if mode and token:
        result = whatsapp_client.verify_webhook(
            mode=mode,
            token=token,
            challenge=challenge,
            verify_token=WEBHOOK_VERIFY_TOKEN
        )
        
        if result:
            return PlainTextResponse(content=result, status_code=200)
    
    # Verification failed
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def webhook_handler(request: Request):
    """
    Main webhook endpoint for receiving WhatsApp messages
    """
    try:
        # Get webhook data
        data = await request.json()
        
        # Log incoming webhook
        print(f"\n📥 Webhook received: {data.get('object', 'unknown')}")
        
        # Process in background to respond quickly
        asyncio.create_task(process_whatsapp_message(data))
        
        # Respond immediately to Meta
        return Response(status_code=200)
        
    except Exception as e:
        print(f"❌ Error in webhook handler: {str(e)}")
        return Response(status_code=200)  # Still return 200 to Meta


async def process_whatsapp_message(webhook_data: Dict[str, Any]):
    """
    Process incoming WhatsApp message
    Runs in background to avoid blocking webhook response
    """
    try:
        # Parse the message
        message_data = whatsapp_client.parse_webhook_message(webhook_data)
        
        if not message_data:
            print("⚠️  No message data found in webhook")
            return
        
        # Extract message details
        user_id = message_data["from"]
        user_name = message_data["name"]
        message_text = message_data.get("text", "")
        message_id = message_data["message_id"]
        
        # Skip unsupported messages
        if message_data.get("unsupported"):
            print(f"⚠️  Unsupported message type from {user_id}")
            whatsapp_client.send_message(
                to=user_id,
                message="Sorry, I can only process text messages at the moment."
            )
            return
        
        # Mark message as read
        whatsapp_client.mark_as_read(message_id)
        
        # Add to session
        session_manager.add_user_message(user_id, message_text, user_name)
        
        print(f"\n{'='*60}")
        print(f"💬 Processing message from {user_name} ({user_id})")
        print(f"   Message: {message_text[:100]}...")
        print(f"{'='*60}")
        
        # Handle special commands
        if message_text.lower() in ['/start', 'hi', 'hello', 'hey']:
            response = WELCOME_MESSAGE
            session_manager.add_assistant_message(user_id, response)
            whatsapp_client.send_message(to=user_id, message=response)
            return
        
        if message_text.lower() == '/clear':
            session_manager.clear_session(user_id)
            response = "🗑️ Conversation history cleared! Starting fresh."
            whatsapp_client.send_message(to=user_id, message=response)
            return
        
        # Send typing indicator (simulate)
        whatsapp_client.send_typing_indicator(user_id, duration=2)
        
        # Process with RAG agent in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            rag_agent.answer_question,
            message_text
        )
        
        # Get the answer
        answer = result.get("answer", ERROR_MESSAGE)
        
        # Check if we found relevant documents
        if result.get("num_sources", 0) == 0:
            answer = NO_DOCUMENTS_MESSAGE
        
        # Add assistant response to session
        session_manager.add_assistant_message(user_id, answer)
        
        # Send response
        send_result = whatsapp_client.send_message(
            to=user_id,
            message=answer
        )
        
        if send_result["success"]:
            print(f"✅ Response sent to {user_name}")
            
            # Send a thumbs up reaction to original message
            whatsapp_client.send_reaction(
                to=user_id,
                message_id=message_id,
                emoji="✅"
            )
        else:
            print(f"❌ Failed to send response to {user_name}")
        
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error processing message: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Try to send error message to user
        try:
            if 'user_id' in locals():
                whatsapp_client.send_message(
                    to=user_id,
                    message=ERROR_MESSAGE
                )
        except:
            pass


@app.post("/send-message")
async def send_message_endpoint(request: Request):
    """
    Endpoint to send messages programmatically
    For testing purposes
    """
    data = await request.json()
    
    to = data.get("to")
    message = data.get("message")
    
    if not to or not message:
        raise HTTPException(status_code=400, detail="Missing 'to' or 'message'")
    
    result = whatsapp_client.send_message(to=to, message=message)
    
    return result


@app.get("/sessions")
async def get_sessions():
    """Get information about all active sessions"""
    return {
        "total_sessions": session_manager.get_active_sessions_count(),
        "sessions": session_manager.get_all_sessions_info()
    }


@app.delete("/sessions/{user_id}")
async def delete_session(user_id: str):
    """Delete a specific user session"""
    session_manager.delete_session(user_id)
    return {"status": "deleted", "user_id": user_id}


@app.post("/cleanup-sessions")
async def cleanup_sessions():
    """Cleanup expired sessions"""
    session_manager.cleanup_expired_sessions()
    return {
        "status": "cleaned",
        "active_sessions": session_manager.get_active_sessions_count()
    }


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the FastAPI server
    
    Args:
        host: Host to bind to
        port: Port to listen on
    """
    print(f"\n🌐 Starting server on {host}:{port}")
    print(f"📱 Webhook URL: http://{host}:{port}/webhook")
    print(f"📊 Health check: http://{host}:{port}/health")
    print(f"\n⚠️  Make sure to expose this server to the internet using ngrok or similar")
    print(f"   Example: ngrok http {port}\n")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    run_server()
