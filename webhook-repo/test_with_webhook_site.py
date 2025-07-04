#!/usr/bin/env python3
"""
Test webhook using webhook.site as intermediary
"""

import requests
import json

# Your webhook.site URL (replace with your actual URL)
WEBHOOK_SITE_URL = "https://webhook.site/3b946566-0e54-4747-8715-1dc426342017"

# Your local webhook endpoint
LOCAL_WEBHOOK_URL = "http://127.0.0.1:5000/webhook"

def test_local_webhook_directly():
    """Test your local webhook endpoint directly."""
    print("🧪 Testing local webhook endpoint directly...")
    
    # Sample push event payload
    payload = {
        "pusher": {"name": "test_user"},
        "ref": "refs/heads/main",
        "commits": [{"id": "abc123def456"}],
        "after": "abc123def456",
        "repository": {"name": "test-repo"}
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "push"
    }
    
    try:
        response = requests.post(LOCAL_WEBHOOK_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ Local webhook test successful!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Local webhook test failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing local webhook: {e}")

def send_to_webhook_site():
    """Send a test payload to webhook.site to see the format."""
    print("📡 Sending test payload to webhook.site...")
    
    # Sample GitHub webhook payload
    payload = {
        "pusher": {"name": "webhook_site_test"},
        "ref": "refs/heads/main",
        "commits": [{"id": "test123456"}],
        "after": "test123456",
        "repository": {"name": "webhook-site-test"}
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "push",
        "User-Agent": "GitHub-Hookshot/test"
    }
    
    try:
        response = requests.post(WEBHOOK_SITE_URL, json=payload, headers=headers)
        print(f"✅ Sent to webhook.site: {response.status_code}")
        print("📋 Check your webhook.site page to see the received data!")
    except Exception as e:
        print(f"❌ Error sending to webhook.site: {e}")

if __name__ == "__main__":
    print("🚀 Webhook Testing with webhook.site")
    print("=" * 50)
    
    # Test 1: Direct local webhook test
    test_local_webhook_directly()
    print()
    
    # Test 2: Send to webhook.site to see format
    send_to_webhook_site()
    print()
    print("🔍 Next steps:")
    print("1. Check your webhook.site page to see the received payload")
    print("2. Check your Flask app at http://127.0.0.1:5000 to see if events appear")
    print("3. Check http://127.0.0.1:5000/events to see stored events")
