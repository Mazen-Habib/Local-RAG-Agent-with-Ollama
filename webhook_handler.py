"""
WhatsApp Status Webhook Handler
Receive delivery status updates from Meta
"""

from fastapi import FastAPI, Request, HTTPException
import json
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "my_secret_token_xyz")

app = FastAPI()

# Store delivery status
delivery_status = {}


@app.get("/webhook")
async def webhook_verify(
    mode: str = None,
    token: str = None,
    challenge: str = None
):
    """
    Webhook verification - Meta calls this first
    """
    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        print("✅ Webhook verified!")
        return challenge
    else:
        print("❌ Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def webhook_receive(request: Request):
    """
    Receive webhook events from WhatsApp
    This is where delivery status updates come in
    """
    
    try:
        data = await request.json()
        
        # Print the raw webhook data
        print("\n" + "="*80)
        print("📨 WEBHOOK RECEIVED")
        print("="*80)
        print(json.dumps(data, indent=2))
        print("="*80 + "\n")
        
        # Parse the webhook
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        
        # Check for status updates (delivery notifications)
        statuses = value.get("statuses", [])
        if statuses:
            for status in statuses:
                wamid = status.get("id")
                status_value = status.get("status")
                timestamp = status.get("timestamp")
                
                delivery_status[wamid] = {
                    "status": status_value,
                    "timestamp": timestamp,
                    "received_at": datetime.now().isoformat()
                }
                
                print(f"📊 STATUS UPDATE:")
                print(f"   wamid: {wamid}")
                print(f"   Status: {status_value}")
                print(f"   Timestamp: {timestamp}\n")
                
                # Log the recipient who received status
                recipient = status.get("recipient_id")
                if recipient:
                    print(f"   🔔 Recipient: {recipient}\n")
                
                # Check for errors
                errors = status.get("errors", [])
                if errors:
                    for error in errors:
                        print(f"   ❌ Error: {error.get('message', 'Unknown')}")
                        print(f"      Code: {error.get('code', 'N/A')}\n")
        
        # Check for incoming messages
        messages = value.get("messages", [])
        if messages:
            for msg in messages:
                print(f"📥 INCOMING MESSAGE")
                print(f"   From: {msg.get('from')}")
                print(f"   Type: {msg.get('type')}")
                if msg.get("type") == "text":
                    print(f"   Text: {msg.get('text', {}).get('body')}\n")
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/delivery-status/{wamid}")
async def get_delivery_status(wamid: str):
    """
    Get the last known delivery status for a message
    """
    if wamid in delivery_status:
        return delivery_status[wamid]
    else:
        return {"status": "unknown", "message": f"No status found for wamid: {wamid}"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "webhook": "ready",
        "messages_tracked": len(delivery_status)
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("🚀 WhatsApp Status Webhook Handler")
    print("="*80)
    print("\n📝 Setup Instructions:")
    print("1. Run this server: python webhook_handler.py")
    print("2. Expose with ngrok: ngrok http 8000")
    print("3. Set webhook URL in Meta: https://your-ngrok-url/webhook")
    print("4. Verify token: " + WEBHOOK_VERIFY_TOKEN)
    print("\n🔍 Then send messages with: python track_messages.py")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
