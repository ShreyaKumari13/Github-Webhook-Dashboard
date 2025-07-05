#!/usr/bin/env python3
"""
Simple test to check webhook endpoint
"""

import requests
import json

def test_webhook():
    url = "https://github-webhook-dashboard.onrender.com/webhook"
    
    # Simple push payload
    payload = {
        "ref": "refs/heads/main",
        "pusher": {"name": "TestUser"},
        "sender": {"login": "TestUser"},
        "head_commit": {
            "id": "abc123",
            "author": {"name": "TestUser"},
            "timestamp": "2025-07-05T19:00:00Z"
        },
        "commits": [{"id": "abc123", "author": {"name": "TestUser"}}]
    }
    
    headers = {
        "X-GitHub-Event": "push",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def check_events():
    url = "https://github-webhook-dashboard.onrender.com/events"
    try:
        response = requests.get(url, timeout=10)
        print(f"Events status: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"Found {len(events)} events")
            for event in events[:3]:
                print(f"- {event}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing webhook...")
    test_webhook()
    print("\nChecking events...")
    check_events()
