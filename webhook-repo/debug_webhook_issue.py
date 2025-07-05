#!/usr/bin/env python3
"""
Debug script to identify why webhooks are not being stored
"""

import requests
import json
import time

BASE_URL = "https://github-webhook-dashboard.onrender.com"

def send_test_webhook():
    """Send a test webhook and check the response"""
    print("🧪 Sending test webhook...")
    
    # Test PUSH webhook with all required fields
    push_payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "TestUser",
            "email": "test@example.com"
        },
        "sender": {
            "login": "TestUser"
        },
        "head_commit": {
            "id": "abc123def456789012345678901234567890abcd",
            "message": "Test commit",
            "timestamp": "2025-07-05T19:50:00Z",
            "author": {
                "name": "TestUser",
                "email": "test@example.com"
            }
        },
        "commits": [
            {
                "id": "abc123def456789012345678901234567890abcd",
                "message": "Test commit",
                "timestamp": "2025-07-05T19:50:00Z",
                "author": {
                    "name": "TestUser",
                    "email": "test@example.com"
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
        "Content-Type": "application/json",
        "X-Hub-Signature-256": "sha256=test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=push_payload, headers=headers, timeout=15)
        print(f"Webhook response status: {response.status_code}")
        print(f"Webhook response: {response.text}")
        
        # Wait a moment for processing
        time.sleep(3)
        
        # Check database status
        db_response = requests.get(f"{BASE_URL}/db-status", timeout=10)
        if db_response.status_code == 200:
            db_data = db_response.json()
            print(f"Database count after webhook: {db_data.get('document_count', 0)}")
        
        # Check events
        events_response = requests.get(f"{BASE_URL}/events", timeout=10)
        if events_response.status_code == 200:
            events = events_response.json()
            print(f"Events retrieved: {len(events)}")
            if events:
                print(f"Latest event: {events[0]}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error sending webhook: {e}")
        return False

def test_pull_request_webhook():
    """Send a test pull request webhook"""
    print("\n🧪 Sending test pull request webhook...")
    
    pr_payload = {
        "action": "opened",
        "pull_request": {
            "number": 123,
            "user": {
                "login": "TestUser"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            },
            "created_at": "2025-07-05T19:50:00Z"
        },
        "sender": {
            "login": "TestUser"
        },
        "repository": {
            "name": "test-repo",
            "full_name": "testuser/test-repo"
        }
    }
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json",
        "X-Hub-Signature-256": "sha256=test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=pr_payload, headers=headers, timeout=15)
        print(f"PR webhook response status: {response.status_code}")
        print(f"PR webhook response: {response.text}")
        
        # Wait a moment for processing
        time.sleep(3)
        
        # Check events
        events_response = requests.get(f"{BASE_URL}/events", timeout=10)
        if events_response.status_code == 200:
            events = events_response.json()
            print(f"Events after PR webhook: {len(events)}")
            if events:
                print(f"Latest event: {events[0]}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error sending PR webhook: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Debugging webhook storage issue")
    print("=" * 50)
    
    # Check initial state
    print("📊 Initial database state:")
    try:
        db_response = requests.get(f"{BASE_URL}/db-status", timeout=10)
        if db_response.status_code == 200:
            db_data = db_response.json()
            print(f"Connected: {db_data.get('connected', False)}")
            print(f"Event count: {db_data.get('document_count', 0)}")
    except Exception as e:
        print(f"Error checking initial state: {e}")
    
    print("\n" + "=" * 50)
    
    # Test push webhook
    send_test_webhook()
    
    # Test pull request webhook
    test_pull_request_webhook()
    
    print("\n✅ Debug testing completed!")
