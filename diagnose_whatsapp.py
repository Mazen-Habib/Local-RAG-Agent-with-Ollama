"""
Diagnose WhatsApp message delivery issues
"""

import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")

print("\n" + "="*80)
print("🔍 WHATSAPP DIAGNOSIS")
print("="*80)

# 1. Check credentials
print("\n1️⃣ CHECKING CREDENTIALS")
print("-" * 80)
print(f"Phone Number ID: {WHATSAPP_PHONE_NUMBER_ID or '❌ NOT SET'}")
print(f"API Token: {'✅ SET (length: ' + str(len(WHATSAPP_API_TOKEN)) + ')' if WHATSAPP_API_TOKEN else '❌ NOT SET'}")

if not WHATSAPP_API_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
    print("\n❌ Missing credentials. Add to .env file!")
    exit(1)

# 2. Check API access with a test call
print("\n2️⃣ CHECKING API ACCESS")
print("-" * 80)

api_url = f"https://graph.facebook.com/v24.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
    "Content-Type": "application/json",
}

# Try to get phone details
try:
    response = requests.get(
        f"https://graph.facebook.com/v24.0/{WHATSAPP_PHONE_NUMBER_ID}",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API Token is valid")
        print(f"   Phone Number: {data.get('display_phone_number', 'N/A')}")
        print(f"   Status: {data.get('quality_rating', 'N/A')}")
    else:
        error = response.json().get("error", {})
        print(f"❌ API Error ({response.status_code}): {error.get('message', 'Unknown error')}")
        
        if response.status_code == 401:
            print("   → Token might be expired or invalid")
        elif response.status_code == 400:
            print("   → Phone Number ID might be wrong")
        
except Exception as e:
    print(f"❌ Connection error: {e}")

# 3. List common issues
print("\n3️⃣ COMMON ISSUES & SOLUTIONS")
print("-" * 80)

issues = [
    ("Phone number format", "Use format like: 923335231335 (no +, no spaces)"),
    ("Sandbox mode", "In testing, you need to add numbers as test numbers first"),
    ("Token expired", "Generate a new token from Meta Business Suite"),
    ("Permissions", "Token needs: whatsapp_business_messaging permission"),
    ("Phone not verified", "Verify phone number in WhatsApp API Setup page"),
    ("Test number not added", "Add recipient numbers in Meta Business → Test Messages"),
]

for issue, solution in issues:
    print(f"• {issue}")
    print(f"  └─ {solution}")

print("\n" + "="*80)
print("📝 NEXT STEPS:")
print("="*80)
print("1. Check test recipient numbers at: https://business.facebook.com/wa/manage/home")
print("2. Verify token hasn't expired")
print("3. Run: python whatsapp_client.py")
print("4. Enter phone number in format: 923335231335")
print("5. Check the API error response above")
print("="*80 + "\n")
