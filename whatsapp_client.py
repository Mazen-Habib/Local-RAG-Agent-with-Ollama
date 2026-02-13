"""
WhatsApp Client
Handles sending and receiving WhatsApp messages via Meta Business API
"""

import requests
import json
from typing import Dict, Any, Optional
import time

from whatsapp_config import (
    WHATSAPP_API_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
    WHATSAPP_API_URL,
)


class WhatsAppClient:
    """Client for interacting with WhatsApp Business API"""
    
    def __init__(self):
        """Initialize WhatsApp client"""
        self.api_token = WHATSAPP_API_TOKEN
        self.phone_number_id = WHATSAPP_PHONE_NUMBER_ID
        self.api_url = WHATSAPP_API_URL
        
        # Set up headers
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        
        print("✅ WhatsApp client initialized")
    
    def send_message(
        self,
        to: str,
        message: str,
        preview_url: bool = False
    ) -> Dict[str, Any]:
        """
        Send a text message to a WhatsApp number
        
        Args:
            to: Recipient phone number (with country code, no + sign)
            message: Message text to send
            preview_url: Whether to show URL previews
            
        Returns:
            API response dictionary
        """
        # Clean phone number (remove + and spaces)
        to_clean = to.replace("+", "").replace(" ", "").replace("-", "")
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_clean,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": message
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            result = response.json()
            
            # Check if API returned an error
            if response.status_code != 200:
                error_msg = result.get("error", {}).get("message", str(result))
                print(f"❌ API Error ({response.status_code}): {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "status_code": response.status_code,
                    "data": result
                }
            
            response.raise_for_status()
            
            print(f"✅ Message sent to {to_clean}")
            print(f"   Response: {json.dumps(result, indent=2)}")
            return {
                "success": True,
                "data": result,
                "message_id": result.get("messages", [{}])[0].get("id")
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send message: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Status Code: {e.response.status_code}")
                print(f"   Response: {e.response.text}")
            
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send WhatsApp message"
            }
    
    def send_reaction(
        self,
        to: str,
        message_id: str,
        emoji: str = "👍"
    ) -> Dict[str, Any]:
        """
        React to a message with an emoji
        
        Args:
            to: Recipient phone number
            message_id: ID of message to react to
            emoji: Emoji to react with
            
        Returns:
            API response dictionary
        """
        to_clean = to.replace("+", "").replace(" ", "").replace("-", "")
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_clean,
            "type": "reaction",
            "reaction": {
                "message_id": message_id,
                "emoji": emoji
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            return {"success": True, "data": response.json()}
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send reaction: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def mark_as_read(
        self,
        message_id: str
    ) -> Dict[str, Any]:
        """
        Mark a message as read
        
        Args:
            message_id: ID of message to mark as read
            
        Returns:
            API response dictionary
        """
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            return {"success": True, "data": response.json()}
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Failed to mark as read: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def send_typing_indicator(
        self,
        to: str,
        duration: int = 3
    ):
        """
        Simulate typing indicator (by sending multiple reactions quickly)
        This is a workaround as WhatsApp API doesn't have official typing indicator
        
        Args:
            to: Recipient phone number
            duration: How long to "type" (seconds)
        """
        # Note: WhatsApp Business API doesn't support typing indicators
        # This is just a placeholder for future implementation
        print(f"💬 Simulating typing for {duration}s...")
        time.sleep(min(duration, 3))  # Max 3 seconds
    
    def parse_webhook_message(
        self,
        webhook_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Parse incoming webhook message from WhatsApp
        
        Args:
            webhook_data: Raw webhook data from WhatsApp
            
        Returns:
            Parsed message dictionary or None
        """
        try:
            # Extract message data
            entry = webhook_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            
            # Get message
            messages = value.get("messages", [])
            if not messages:
                return None
            
            message = messages[0]
            
            # Get contact info
            contacts = value.get("contacts", [{}])
            contact = contacts[0] if contacts else {}
            
            # Parse based on message type
            message_type = message.get("type")
            
            parsed = {
                "message_id": message.get("id"),
                "from": message.get("from"),
                "timestamp": message.get("timestamp"),
                "type": message_type,
                "name": contact.get("profile", {}).get("name", "Unknown"),
            }
            
            # Extract text content
            if message_type == "text":
                parsed["text"] = message.get("text", {}).get("body", "")
            elif message_type == "button":
                parsed["text"] = message.get("button", {}).get("text", "")
            elif message_type == "interactive":
                # Handle button/list replies
                interactive = message.get("interactive", {})
                if interactive.get("type") == "button_reply":
                    parsed["text"] = interactive.get("button_reply", {}).get("title", "")
                elif interactive.get("type") == "list_reply":
                    parsed["text"] = interactive.get("list_reply", {}).get("title", "")
            else:
                # Unsupported message type
                parsed["text"] = f"[{message_type} message - not supported]"
                parsed["unsupported"] = True
            
            print(f"📨 Received message from {parsed['from']}: {parsed.get('text', '')[:50]}...")
            
            return parsed
            
        except Exception as e:
            print(f"❌ Error parsing webhook message: {str(e)}")
            return None
    
    def verify_webhook(
        self,
        mode: str,
        token: str,
        challenge: str,
        verify_token: str
    ) -> Optional[str]:
        """
        Verify webhook subscription
        
        Args:
            mode: Verification mode from webhook
            token: Token from webhook
            challenge: Challenge string to return
            verify_token: Your verify token
            
        Returns:
            Challenge string if verification successful, None otherwise
        """
        if mode == "subscribe" and token == verify_token:
            print("✅ Webhook verified successfully")
            return challenge
        else:
            print("❌ Webhook verification failed")
            return None


def test_whatsapp_client():
    """Test WhatsApp client functionality"""
    print("\n" + "="*60)
    print("🧪 Testing WhatsApp Client")
    print("="*60)
    
    client = WhatsAppClient()
    
    # Test sending a message (to your number)
    test_number = input("\nEnter your WhatsApp number (with country code, e.g., 923335231335): ")
    
    if test_number:
        result = client.send_message(
            to=test_number,
            message="🤖 Test message from RAG Agent! If you received this, WhatsApp integration is working! ✅"
        )
        
        if result["success"]:
            print("\n✅ Test message sent successfully!")
            print(f"   Message ID: {result.get('message_id')}")
        else:
            print("\n❌ Failed to send test message")
            print(f"   Error: {result.get('error')}")
    
    print("="*60)


if __name__ == "__main__":
    from whatsapp_config import validate_whatsapp_config
    
    if validate_whatsapp_config():
        test_whatsapp_client()
    else:
        print("\n⚠️  Please configure WhatsApp credentials first")
