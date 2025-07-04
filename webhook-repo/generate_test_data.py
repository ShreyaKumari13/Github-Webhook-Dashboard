#!/usr/bin/env python3
"""
Generate fake webhook events for testing without using real GitHub webhooks.
"""

import requests
import json
import random
import time
from datetime import datetime

# Your local webhook endpoint
WEBHOOK_URL = "http://127.0.0.1:5000/webhook"

# Sample data for generating fake events
USERS = ["alice_dev", "bob_coder", "charlie_ops", "diana_designer", "eve_tester"]
BRANCHES = ["main", "develop", "feature-auth", "feature-ui", "bugfix-login", "hotfix-security"]
COMMIT_MESSAGES = [
    "Fix authentication bug",
    "Add new dashboard feature", 
    "Update user interface",
    "Improve performance",
    "Fix security vulnerability",
    "Add unit tests",
    "Update documentation"
]

def generate_push_event():
    """Generate a fake push event."""
    user = random.choice(USERS)
    branch = random.choice(BRANCHES)
    commit_id = f"{''.join(random.choices('abcdef0123456789', k=40))}"
    
    return {
        "pusher": {"name": user},
        "ref": f"refs/heads/{branch}",
        "commits": [{"id": commit_id, "message": random.choice(COMMIT_MESSAGES)}],
        "after": commit_id,
        "repository": {"name": "test-repo"}
    }

def generate_pull_request_event():
    """Generate a fake pull request event."""
    user = random.choice(USERS)
    from_branch = random.choice([b for b in BRANCHES if b != "main"])
    to_branch = "main"
    pr_id = random.randint(1, 999)
    
    return {
        "action": "opened",
        "pull_request": {
            "id": pr_id,
            "user": {"login": user},
            "head": {"ref": from_branch},
            "base": {"ref": to_branch}
        },
        "repository": {"name": "test-repo"}
    }

def send_webhook_event(event_type, payload):
    """Send a webhook event to the local server."""
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": event_type
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Sent {event_type} event: {payload.get('pusher', {}).get('name') or payload.get('pull_request', {}).get('user', {}).get('login')}")
        else:
            print(f"❌ Failed to send {event_type} event: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending {event_type} event: {e}")

def generate_test_events(count=5):
    """Generate multiple test events."""
    print(f"🚀 Generating {count} test webhook events...")
    
    for i in range(count):
        # Randomly choose between push and pull request events
        if random.choice([True, False]):
            event_type = "push"
            payload = generate_push_event()
        else:
            event_type = "pull_request" 
            payload = generate_pull_request_event()
        
        send_webhook_event(event_type, payload)
        
        # Wait a bit between events
        time.sleep(1)
    
    print("✅ Done generating test events!")

if __name__ == "__main__":
    print("🧪 GitHub Webhook Test Data Generator")
    print("Make sure your Flask app is running on http://127.0.0.1:5000")
    print()
    
    # Generate some test events
    generate_test_events(8)
