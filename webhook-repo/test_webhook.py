#!/usr/bin/env python3
"""
Comprehensive test script for GitHub webhook endpoint
Tests all three event types: PUSH, PULL_REQUEST, and MERGE
"""

import requests
import json
import time
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:5000/webhook"
EVENTS_URL = "http://localhost:5000/events"
DB_STATUS_URL = "http://localhost:5000/db-status"

def test_push_webhook():
    """Test push webhook payload according to assessment requirements"""
    payload = {
        "ref": "refs/heads/staging",
        "pusher": {
            "name": "Travis",
            "email": "travis@example.com"
        },
        "sender": {
            "login": "Travis"
        },
        "commits": [
            {
                "id": "abc123def456789",
                "message": "Add new feature",
                "author": {
                    "name": "Travis",
                    "email": "travis@example.com"
                }
            }
        ],
        "repository": {
            "name": "action-repo",
            "full_name": "testuser/action-repo"
        }
    }

    headers = {
        "X-GitHub-Event": "push",
        "Content-Type": "application/json",
        "X-Hub-Signature-256": "sha256=test"
    }

    print("🧪 Testing PUSH webhook...")
    print("Expected format: \"Travis\" pushed to \"staging\" on [timestamp]")
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_pull_request_webhook():
    """Test pull request webhook payload (opened action)"""
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 42,
            "title": "Feature: Add user authentication",
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "staging"
            },
            "base": {
                "ref": "master"
            }
        },
        "repository": {
            "name": "action-repo",
            "full_name": "testuser/action-repo"
        },
        "sender": {
            "login": "Travis"
        }
    }


    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json",
        "X-Hub-Signature-256": "sha256=test"
    }

    print("🧪 Testing PULL_REQUEST webhook...")
    print("Expected format: \"Travis\" submitted a pull request from \"staging\" to \"master\" on [timestamp]")
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_merge_webhook():
    """Test merge webhook payload (PR closed and merged)"""
    payload = {
        "action": "closed",
        "pull_request": {
            "number": 42,
            "title": "Feature: Add user authentication",
            "merged": True,
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "dev"
            },
            "base": {
                "ref": "master"
            }
        },
        "repository": {
            "name": "action-repo",
            "full_name": "testuser/action-repo"
        },
        "sender": {
            "login": "Travis"
        }
    }

    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json",
        "X-Hub-Signature-256": "sha256=test"
    }

    print("🧪 Testing MERGE webhook...")
    print("Expected format: \"Travis\" merged branch \"dev\" to \"master\" on [timestamp]")
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_ignored_events():
    """Test that non-relevant events are properly ignored"""
    # Test PR synchronize action (should be ignored)
    payload = {
        "action": "synchronize",
        "pull_request": {
            "number": 42,
            "title": "Test PR",
            "user": {"login": "Travis"},
            "head": {"ref": "feature"},
            "base": {"ref": "main"}
        },
        "repository": {"name": "test-repo", "full_name": "testuser/test-repo"},
        "sender": {"login": "Travis"}
    }

    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json"
    }

    print("🧪 Testing ignored event (PR synchronize)...")
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_database_status():
    """Test database connection status"""
    print("🧪 Testing database status...")
    response = requests.get(DB_STATUS_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_events_endpoint():
    """Test events retrieval endpoint"""
    print("🧪 Testing events endpoint...")
    response = requests.get(EVENTS_URL)
    print(f"Status: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events:")

    for i, event in enumerate(events[:5], 1):  # Show first 5 events
        print(f"  {i}. {event.get('message', 'No message')}")
        print(f"     Action: {event.get('action', 'Unknown')} | Request ID: {event.get('request_id', 'Unknown')}")
    print()

def verify_message_formats(events):
    """Verify that messages match the exact assessment requirements"""
    print("🔍 Verifying message formats...")

    for event in events:
        action = event.get('action')
        message = event.get('message', '')

        if action == 'PUSH':
            # Should match: "author" pushed to "branch" on timestamp
            if 'pushed to' in message and 'on' in message:
                print(f"✅ PUSH format correct: {message}")
            else:
                print(f"❌ PUSH format incorrect: {message}")

        elif action == 'PULL_REQUEST':
            # Should match: "author" submitted a pull request from "branch" to "branch" on timestamp
            if 'submitted a pull request from' in message and 'to' in message and 'on' in message:
                print(f"✅ PULL_REQUEST format correct: {message}")
            else:
                print(f"❌ PULL_REQUEST format incorrect: {message}")

        elif action == 'MERGE':
            # Should match: "author" merged branch "branch" to "branch" on timestamp
            if 'merged branch' in message and 'to' in message and 'on' in message:
                print(f"✅ MERGE format correct: {message}")
            else:
                print(f"❌ MERGE format incorrect: {message}")
    print()

if __name__ == "__main__":
    print("🚀 GitHub Webhook Assessment Test Suite")
    print("=" * 50)
    print("Testing all three required event types: PUSH, PULL_REQUEST, MERGE")
    print()

    # Test database connection first
    test_database_status()

    # Test all webhook types
    test_push_webhook()
    test_pull_request_webhook()
    test_merge_webhook()
    test_ignored_events()

    # Wait for database writes
    print("⏳ Waiting for database writes...")
    time.sleep(2)

    # Test events retrieval
    test_events_endpoint()

    # Get events for format verification
    response = requests.get(EVENTS_URL)
    if response.status_code == 200:
        events = response.json()
        verify_message_formats(events)

    print("✅ Assessment test suite completed!")
    print("\n📋 Summary:")
    print("- PUSH events should show: author pushed to branch")
    print("- PULL_REQUEST events should show: author submitted PR from branch to branch")
    print("- MERGE events should show: author merged branch to branch")
    print("- UI should poll every 15 seconds")
    print("- All timestamps should be in format: DD Month YYYY - HH:MM AM/PM UTC")
