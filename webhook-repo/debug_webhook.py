#!/usr/bin/env python3
"""
Debug script to test webhook processing with sample GitHub payloads
"""

import json
import requests
from datetime import datetime

# Your deployed webhook URL
WEBHOOK_URL = "https://github-webhook-dashboard.onrender.com/webhook"

def test_push_webhook():
    """Test push webhook with realistic GitHub payload"""
    
    # Sample GitHub push payload
    payload = {
        "ref": "refs/heads/main",
        "before": "abc123def456",
        "after": "def456ghi789",
        "pusher": {
            "name": "YourUsername",
            "email": "your.email@example.com"
        },
        "sender": {
            "login": "YourUsername",
            "id": 12345
        },
        "head_commit": {
            "id": "def456ghi789abc123",
            "message": "Fix webhook author extraction",
            "timestamp": datetime.now().isoformat() + "Z",
            "author": {
                "name": "YourUsername",
                "email": "your.email@example.com"
            }
        },
        "commits": [
            {
                "id": "def456ghi789abc123",
                "message": "Fix webhook author extraction",
                "author": {
                    "name": "YourUsername",
                    "email": "your.email@example.com"
                }
            }
        ],
        "repository": {
            "name": "action-repo",
            "full_name": "YourUsername/action-repo"
        }
    }
    
    headers = {
        "X-GitHub-Event": "push",
        "X-Hub-Signature-256": "sha256=test",
        "Content-Type": "application/json"
    }
    
    print("🚀 Testing push webhook...")
    try:
        response = requests.post(WEBHOOK_URL, 
                               json=payload, 
                               headers=headers,
                               timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Push webhook test successful!")
        else:
            print("❌ Push webhook test failed!")
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

def test_pull_request_webhook():
    """Test pull request webhook"""
    
    payload = {
        "action": "opened",
        "number": 123,
        "pull_request": {
            "id": 123,
            "number": 123,
            "user": {
                "login": "YourUsername"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            },
            "created_at": datetime.now().isoformat() + "Z"
        },
        "sender": {
            "login": "YourUsername"
        }
    }
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": "sha256=test",
        "Content-Type": "application/json"
    }
    
    print("🔄 Testing pull request webhook...")
    try:
        response = requests.post(WEBHOOK_URL, 
                               json=payload, 
                               headers=headers,
                               timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Pull request webhook test successful!")
        else:
            print("❌ Pull request webhook test failed!")
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

def check_events():
    """Check if events are being stored correctly"""
    
    events_url = "https://github-webhook-dashboard.onrender.com/events"
    
    print("📊 Checking stored events...")
    try:
        response = requests.get(events_url, timeout=10)
        
        if response.status_code == 200:
            events = response.json()
            print(f"Found {len(events)} events:")
            
            for event in events[:5]:  # Show first 5
                print(f"  - {event.get('action', 'Unknown')} by {event.get('author', 'Unknown')}")
                print(f"    Request ID: {event.get('request_id', 'Unknown')}")
                print(f"    Timestamp: {event.get('timestamp', 'Unknown')}")
                print()
        else:
            print(f"❌ Failed to get events: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking events: {e}")

if __name__ == "__main__":
    print("🔧 GitHub Webhook Debug Tool")
    print("=" * 40)
    
    # Test webhooks
    test_push_webhook()
    print()
    test_pull_request_webhook()
    print()
    
    # Wait a moment for processing
    import time
    print("⏳ Waiting for processing...")
    time.sleep(3)
    
    # Check results
    check_events()
