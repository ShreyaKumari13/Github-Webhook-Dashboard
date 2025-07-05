#!/usr/bin/env python3
"""
Test webhook endpoint with a real push payload
"""

import requests
import json

def test_push_webhook():
    """Test the webhook with a realistic push payload"""
    
    webhook_url = "https://github-webhook-dashboard.onrender.com/webhook"
    
    # Create a realistic push payload
    payload = {
        "ref": "refs/heads/main",
        "before": "abc123",
        "after": "def456",
        "pusher": {
            "name": "testuser",
            "email": "test@example.com"
        },
        "sender": {
            "login": "testuser",
            "id": 12345
        },
        "head_commit": {
            "id": "def456",
            "message": "Test commit",
            "timestamp": "2025-07-05T19:30:00Z",
            "author": {
                "name": "Test User",
                "email": "test@example.com",
                "username": "testuser"
            }
        },
        "commits": [
            {
                "id": "def456",
                "message": "Test commit",
                "timestamp": "2025-07-05T19:30:00Z",
                "author": {
                    "name": "Test User",
                    "email": "test@example.com",
                    "username": "testuser"
                }
            }
        ],
        "repository": {
            "name": "test-repo",
            "full_name": "testuser/test-repo"
        }
    }
    
    headers = {
        "X-GitHub-Event": "push",
        "X-Hub-Signature-256": "sha256=test",
        "Content-Type": "application/json"
    }
    
    print("🚀 Testing webhook endpoint...")
    print(f"📍 URL: {webhook_url}")
    
    try:
        response = requests.post(webhook_url, 
                               json=payload, 
                               headers=headers,
                               timeout=15)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            
            # Check if event was stored
            print("\n🔍 Checking if event was stored...")
            events_response = requests.get("https://github-webhook-dashboard.onrender.com/events", timeout=10)
            
            if events_response.status_code == 200:
                events = events_response.json()
                print(f"📊 Total events now: {len(events)}")
                
                if len(events) > 0:
                    latest = events[0]
                    print(f"🎯 Latest event:")
                    print(f"   Author: {latest.get('author')}")
                    print(f"   Action: {latest.get('action')}")
                    print(f"   Branch: {latest.get('to_branch')}")
                    print(f"   Message: {latest.get('message')}")
                else:
                    print("⚠️  No events found in database")
            else:
                print(f"❌ Failed to check events: {events_response.status_code}")
                
        else:
            print("❌ Webhook test failed!")
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

if __name__ == "__main__":
    print("🧪 Webhook Test")
    print("=" * 30)
    test_push_webhook()
    print("=" * 30)
