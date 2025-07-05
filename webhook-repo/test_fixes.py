#!/usr/bin/env python3
"""
Test the webhook fixes with proper GitHub payload structure
"""

import requests
import json
from datetime import datetime

WEBHOOK_URL = "https://github-webhook-dashboard.onrender.com/webhook"
EVENTS_URL = "https://github-webhook-dashboard.onrender.com/events"

def test_realistic_push():
    """Test with a realistic GitHub push payload"""
    
    payload = {
        "ref": "refs/heads/main",
        "before": "0000000000000000000000000000000000000000",
        "after": "abc123def456789",
        "created": False,
        "deleted": False,
        "forced": False,
        "base_ref": None,
        "compare": "https://github.com/user/repo/compare/abc123...def456",
        "commits": [
            {
                "id": "abc123def456789",
                "tree_id": "tree123",
                "distinct": True,
                "message": "Fix webhook author extraction and timestamp formatting",
                "timestamp": "2025-07-05T19:30:00Z",
                "url": "https://github.com/user/repo/commit/abc123def456789",
                "author": {
                    "name": "YourRealName",
                    "email": "your.email@example.com",
                    "username": "yourusername"
                },
                "committer": {
                    "name": "YourRealName", 
                    "email": "your.email@example.com",
                    "username": "yourusername"
                }
            }
        ],
        "head_commit": {
            "id": "abc123def456789",
            "tree_id": "tree123",
            "distinct": True,
            "message": "Fix webhook author extraction and timestamp formatting",
            "timestamp": "2025-07-05T19:30:00Z",
            "url": "https://github.com/user/repo/commit/abc123def456789",
            "author": {
                "name": "YourRealName",
                "email": "your.email@example.com",
                "username": "yourusername"
            },
            "committer": {
                "name": "YourRealName",
                "email": "your.email@example.com", 
                "username": "yourusername"
            }
        },
        "repository": {
            "id": 123456,
            "name": "action-repo",
            "full_name": "yourusername/action-repo",
            "private": False,
            "owner": {
                "name": "yourusername",
                "email": "your.email@example.com",
                "login": "yourusername"
            }
        },
        "pusher": {
            "name": "YourRealName",
            "email": "your.email@example.com"
        },
        "sender": {
            "login": "yourusername",
            "id": 12345,
            "avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
            "type": "User"
        }
    }
    
    headers = {
        "X-GitHub-Event": "push",
        "X-GitHub-Delivery": "12345678-1234-1234-1234-123456789012",
        "X-Hub-Signature-256": "sha256=test_signature",
        "Content-Type": "application/json",
        "User-Agent": "GitHub-Hookshot/abc123"
    }
    
    print("🚀 Testing realistic push webhook...")
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Action: {result.get('action')}")
            print(f"📝 Message: {result.get('message')}")
        else:
            print("❌ Push webhook failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def check_latest_events():
    """Check the latest events to see if they're formatted correctly"""
    
    print("\n📊 Checking latest events...")
    try:
        response = requests.get(EVENTS_URL, timeout=10)
        
        if response.status_code == 200:
            events = response.json()
            print(f"Found {len(events)} total events")
            
            print("\n🔍 Latest 3 events:")
            for i, event in enumerate(events[:3]):
                print(f"\n{i+1}. Event Details:")
                print(f"   Action: {event.get('action', 'Unknown')}")
                print(f"   Author: {event.get('author', 'Unknown')}")
                print(f"   Request ID: {event.get('request_id', 'Unknown')}")
                print(f"   To Branch: {event.get('to_branch', 'Unknown')}")
                print(f"   From Branch: {event.get('from_branch', 'N/A')}")
                print(f"   Timestamp: {event.get('timestamp', 'Unknown')}")
                
                # Check message format
                message = event.get('message', '')
                if 'pushed to' in message and event.get('action') == 'PUSH':
                    print(f"   ✅ Message Format: {message}")
                elif 'submitted a pull request' in message and event.get('action') == 'PULL_REQUEST':
                    print(f"   ✅ Message Format: {message}")
                elif 'merged branch' in message and event.get('action') == 'MERGE':
                    print(f"   ✅ Message Format: {message}")
                else:
                    print(f"   ⚠️ Message Format: {message}")
                    
        else:
            print(f"❌ Failed to get events: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking events: {e}")

def test_health():
    """Test if the application is healthy"""
    
    health_url = "https://github-webhook-dashboard.onrender.com/health"
    
    print("\n🏥 Testing application health...")
    try:
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Application Status: {health.get('status', 'Unknown')}")
            print(f"📊 Database Status: {health.get('database_status', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    print("🔧 Testing Webhook Fixes")
    print("=" * 50)
    
    # Test health first
    test_health()
    
    # Test webhook
    test_realistic_push()
    
    # Wait for processing
    import time
    print("\n⏳ Waiting for processing...")
    time.sleep(3)
    
    # Check results
    check_latest_events()
    
    print("\n" + "=" * 50)
    print("🎯 Test completed! Check the results above.")
