"""
WhatsApp Configuration
Add these to your existing config.py or use separately
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# WHATSAPP BUSINESS API CONFIGURATION
# ============================================================================

# WhatsApp Business API credentials
# Get from: Meta Business Suite > WhatsApp > API Setup
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")

# Your WhatsApp Business phone number (for display)
WHATSAPP_BUSINESS_PHONE = os.getenv("WHATSAPP_BUSINESS_PHONE", "")

# Webhook verification token (you create this - any random string)
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "my_secret_verify_token_12345")

# ============================================================================
# WHATSAPP API ENDPOINTS
# ============================================================================

# Meta WhatsApp API version (v24.0 is latest stable)
WHATSAPP_API_VERSION = "v24.0"

# Meta WhatsApp API base URL
WHATSAPP_API_URL = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

# Session timeout (in seconds) - how long to keep conversation context
SESSION_TIMEOUT = 1800  # 30 minutes

# Maximum messages to keep in session history
MAX_SESSION_MESSAGES = 10

# ============================================================================
# MESSAGE SETTINGS
# ============================================================================

# Default welcome message
WELCOME_MESSAGE = "Hello! I'm your AI assistant. I can answer questions about your documents. How can I help you today?"

# Message when no documents found
NO_DOCUMENTS_MESSAGE = "I couldn't find any relevant information in my documents. Could you rephrase your question?"

# Error message
ERROR_MESSAGE = "I'm sorry, I encountered an error processing your request. Please try again."

# ============================================================================
# VALIDATION
# ============================================================================

def validate_whatsapp_config():
    """Validate WhatsApp configuration"""
    errors = []
    
    if not WHATSAPP_API_TOKEN:
        errors.append("❌ WHATSAPP_API_TOKEN not set")
    
    if not WHATSAPP_PHONE_NUMBER_ID:
        errors.append("❌ WHATSAPP_PHONE_NUMBER_ID not set")
    
    if not WEBHOOK_VERIFY_TOKEN:
        errors.append("⚠️  WEBHOOK_VERIFY_TOKEN not set (using default)")
    
    if errors:
        print("\n" + "="*60)
        print("⚠️  WHATSAPP CONFIGURATION WARNINGS")
        print("="*60)
        for error in errors:
            print(error)
        print("\n📝 Add to your .env file:")
        print("WHATSAPP_API_TOKEN=your_whatsapp_api_token")
        print("WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id")
        print("WEBHOOK_VERIFY_TOKEN=your_custom_verify_token")
        print("="*60 + "\n")
        return False
    
    print("✅ WhatsApp configuration validated")
    return True


def display_whatsapp_config():
    """Display WhatsApp configuration"""
    print("\n" + "="*60)
    print("📱 WHATSAPP CONFIGURATION")
    print("="*60)
    print(f"Phone Number ID: {WHATSAPP_PHONE_NUMBER_ID or 'Not set'}")
    print(f"API Token: {'Set ✅' if WHATSAPP_API_TOKEN else 'Not set ❌'}")
    print(f"Verify Token: {'Set ✅' if WEBHOOK_VERIFY_TOKEN else 'Not set ❌'}")
    print(f"Session Timeout: {SESSION_TIMEOUT}s ({SESSION_TIMEOUT//60} min)")
    print(f"Max Session Messages: {MAX_SESSION_MESSAGES}")
    print("="*60 + "\n")


if __name__ == "__main__":
    display_whatsapp_config()
    validate_whatsapp_config()
