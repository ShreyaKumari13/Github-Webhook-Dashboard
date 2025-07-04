#!/usr/bin/env python3
"""
Test webhook with exact format requirements from assessment
"""

import requests
import json
import hashlib
import hmac
import time

WEBHOOK_URL = "http://localhost:5000/webhook"
WEBHOOK_SECRET = "your-secret-key"

def create_signature(payload, secret):
    signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"

def send_push_event():
    """Send PUSH event: Travis pushed to staging on timestamp"""
    payload = {
        "ref": "refs/heads/staging",
        "pusher": {
            "name": "Travis"
        },
        "repository": {
            "name": "action-repo"
        },
        "commits": [{"id": "abc123", "message": "Test push"}]
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "push",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"✅ PUSH event sent: {response.status_code}")

def send_pull_request_event():
    """Send PULL_REQUEST event: Travis submitted a pull request from staging to master"""
    payload = {
        "action": "opened",
        "pull_request": {
            "user": {"login": "Travis"},
            "base": {"ref": "master"},
            "head": {"ref": "staging"}
        },
        "repository": {"name": "action-repo"}
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"✅ PULL_REQUEST event sent: {response.status_code}")

def send_merge_event():
    """Send MERGE event: Travis merged branch dev to master"""
    payload = {
        "action": "closed",
        "pull_request": {
            "merged": True,
            "user": {"login": "Travis"},
            "merged_by": {"login": "Travis"},
            "base": {"ref": "master"},
            "head": {"ref": "dev"}
        },
        "repository": {"name": "action-repo"}
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"✅ MERGE event sent: {response.status_code}")

if __name__ == "__main__":
    print("🧪 Testing webhook events with assessment format requirements...")
    print("=" * 60)
    
    # Send test events
    send_push_event()
    time.sleep(1)
    
    send_pull_request_event()
    time.sleep(1)
    
    send_merge_event()
    time.sleep(1)
    
    # Check the latest events
    response = requests.get("http://localhost:5000/events")
    if response.status_code == 200:
        events = response.json()
        print(f"\n📊 Latest events (showing top 3):")
        for i, event in enumerate(events[:3]):
            print(f"{i+1}. {event['event_type']}: {event['author']} -> {event['to_branch']}")
    
    print("\n✨ Test completed! Check the UI at http://localhost:5000 to see the formatted events.")
    print("Expected formats:")
    print('- PUSH: "Travis pushed to staging on [timestamp]"')
    print('- PULL_REQUEST: "Travis submitted a pull request from staging to master on [timestamp]"')
    print('- MERGE: "Travis merged branch dev to master on [timestamp]"')
