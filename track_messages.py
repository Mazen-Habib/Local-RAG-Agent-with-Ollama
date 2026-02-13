"""
WhatsApp Message Delivery Tracker
Track delivery status using wamid returned from API
"""

import requests
import json
import time
from typing import Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")


def get_message_status(wamid: str) -> Dict[str, Any]:
    """
    Get the delivery status of a message using its wamid
    
    Args:
        wamid: WhatsApp Message ID returned from send_message
        
    Returns:
        Status information
    """
    try:
        # Get message details from Meta API
        url = f"https://graph.facebook.com/v24.0/{wamid}"
        headers = {
            "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            
            print("\n" + "="*60)
            print(f"📦 MESSAGE STATUS (wamid: {wamid})")
            print("="*60)
            print(f"Status: {status}")
            
            # Status meanings:
            # - accepted: Sent to WhatsApp
            # - sent: Delivered to device
            # - delivered: Delivered to phone
            # - read: User read message
            # - failed: Message failed
            
            status_emoji = {
                "accepted": "📤",
                "sent": "✅",
                "delivered": "📱",
                "read": "👁️",
                "failed": "❌",
            }.get(status, "❓")
            
            print(f"\n{status_emoji} Meaning:")
            meanings = {
                "accepted": "Message sent to WhatsApp servers (in queue)",
                "sent": "Message sent to recipient's device",
                "delivered": "Message delivered to phone",
                "read": "User has read the message",
                "failed": "Message failed to send"
            }
            print(f"  {meanings.get(status, 'Unknown status')}")
            
            print("="*60 + "\n")
            
            return {"status": status, "data": data}
        else:
            print(f"❌ Error getting status: {response.text}")
            return {"error": response.text}
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}


def send_and_track(to: str, message: str) -> Dict[str, Any]:
    """
    Send a WhatsApp message and track its delivery
    
    Args:
        to: Recipient phone number (format: 923335231335)
        message: Message text
        
    Returns:
        Message info with wamid
    """
    
    # Clean phone number
    to_clean = to.replace("+", "").replace(" ", "").replace("-", "")
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_clean,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }
    
    url = f"https://graph.facebook.com/v24.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    
    print("\n📤 Sending message...")
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if response.status_code == 200:
        wamid = result.get("messages", [{}])[0].get("id")
        print(f"✅ Message sent!")
        print(f"📍 wamid: {wamid}")
        
        return {
            "success": True,
            "wamid": wamid,
            "to": to_clean,
            "data": result
        }
    else:
        error = result.get("error", {})
        print(f"❌ Error: {error.get('message', 'Unknown error')}")
        print(f"   Code: {error.get('code', 'N/A')}")
        
        # Common errors
        if error.get("code") == "131052":
            print("   → Number not in test recipient list")
            print("   → Add it at: https://business.facebook.com/wa/manage/home")
        elif error.get("code") == "131056":
            print("   → Invalid phone number format")
        
        return {"success": False, "error": error}


def main():
    """Main function"""
    print("\n" + "="*60)
    print("📱 WhatsApp Message Tracker")
    print("="*60)
    
    # Option 1: Send new message
    choice = input("\n1. Send new message\n2. Check existing wamid\nChoose (1 or 2): ").strip()
    
    if choice == "1":
        to = input("\nPhone number (e.g., 923335231335): ").strip()
        message = input("Message text: ").strip()
        
        result = send_and_track(to, message)
        
        if result.get("success"):
            wamid = result["wamid"]
            
            # Poll for delivery status
            print("\n⏳ Checking delivery status...")
            for i in range(5):
                time.sleep(2)
                status_result = get_message_status(wamid)
                
                if status_result.get("status") == "delivered":
                    print("✅ Message delivered successfully!")
                    break
                elif status_result.get("status") == "failed":
                    print("❌ Message delivery failed")
                    break
                else:
                    print(f"  Attempt {i+1}: {status_result.get('status', 'checking...')}")
    
    elif choice == "2":
        wamid = input("\nEnter wamid: ").strip()
        get_message_status(wamid)
    
    print("\n" + "="*60)
    print("📝 NOTE: Message status is updated via webhook")
    print("    Status updates come from Meta when:")
    print("    • Message is delivered to phone")
    print("    • User reads the message")
    print("    • Message fails to send")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
