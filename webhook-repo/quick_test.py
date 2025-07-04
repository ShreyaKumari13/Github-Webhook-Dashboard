#!/usr/bin/env python3
"""
Quick test script for webhook functionality
"""

import requests
import json
import hashlib
import hmac

# Configuration
WEBHOOK_URL = "http://localhost:5000/webhook"
WEBHOOK_SECRET = "your-secret-key"
API_URL = "http://localhost:5000/events"

def create_signature(payload, secret):
    """Create GitHub-style webhook signature"""
    signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"

def test_push_event():
    """Test a push event webhook"""
    payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "Travis"
        },
        "repository": {
            "name": "action-repo"
        },
        "commits": [
            {
                "id": "abc123",
                "message": "Test commit for webhook"
            }
        ]
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "push",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"✅ Push event test: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_pull_request_event():
    """Test a pull request event webhook"""
    payload = {
        "action": "opened",
        "pull_request": {
            "user": {
                "login": "Travis"
            },
            "base": {
                "ref": "master"
            },
            "head": {
                "ref": "staging"
            }
        },
        "repository": {
            "name": "action-repo"
        }
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"✅ Pull request event test: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_merge_event():
    """Test a merge event webhook"""
    payload = {
        "action": "closed",
        "pull_request": {
            "merged": True,
            "user": {
                "login": "Travis"
            },
            "merged_by": {
                "login": "Travis"
            },
            "base": {
                "ref": "master"
            },
            "head": {
                "ref": "dev"
            }
        },
        "repository": {
            "name": "action-repo"
        }
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"✅ Merge event test: {response.status_code} - {response.json()}")
    return response.status_code == 200

def check_events():
    """Check stored events"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        events = response.json()
        print(f"\n📊 Total events in database: {len(events)}")
        print("\nRecent events:")
        for i, event in enumerate(events[:5]):
            print(f"{i+1}. {event['event_type']}: {event['author']} -> {event['to_branch']} ({event['timestamp']})")
        return True
    return False

if __name__ == "__main__":
    print("🚀 Testing GitHub Webhook System")
    print("=" * 50)
    
    # Test health first
    health_response = requests.get("http://localhost:5000/health")
    if health_response.status_code == 200:
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
        exit(1)
    
    # Test webhook events
    print("\n🔗 Testing webhook events...")
    test_push_event()
    test_pull_request_event()
    test_merge_event()
    
    # Check stored events
    print("\n📋 Checking stored events...")
    check_events()
    
    print("\n✨ Test completed!")
