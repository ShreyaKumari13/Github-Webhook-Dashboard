#!/usr/bin/env python3
"""
Test script for the deployed GitHub webhook endpoint
Tests the live deployment at https://github-webhook-dashboard.onrender.com/
"""

import requests
import json
import time
from datetime import datetime

# Configuration for deployed app
BASE_URL = "https://github-webhook-dashboard.onrender.com"
WEBHOOK_URL = f"{BASE_URL}/webhook"
EVENTS_URL = f"{BASE_URL}/events"
DB_STATUS_URL = f"{BASE_URL}/db-status"

def test_deployed_status():
    """Test the deployed application status"""
    print("🧪 Testing deployed application status...")
    
    try:
        # Test main page
        response = requests.get(BASE_URL, timeout=10)
        print(f"Main page: {response.status_code}")
        
        # Test database status
        response = requests.get(DB_STATUS_URL, timeout=10)
        print(f"Database status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Database connected: {data.get('connected', False)}")
            print(f"Event count: {data.get('document_count', 0)}")
        
        # Test events endpoint
        response = requests.get(EVENTS_URL, timeout=10)
        print(f"Events endpoint: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"Current events: {len(events)}")
            
            # Show current event format
            if events:
                print("\n📋 Current event format:")
                for i, event in enumerate(events[:3], 1):
                    print(f"  {i}. {event.get('message', 'No message')}")
                    print(f"     Type: {event.get('type', 'Unknown')} | Actor: {event.get('actor', 'Unknown')}")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error testing deployed app: {e}")
        return False

def test_webhook_format():
    """Test webhook with assessment format"""
    print("🧪 Testing webhook with assessment format...")
    
    # Test PUSH webhook
    push_payload = {
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
    
    try:
        print("Sending PUSH webhook...")
        response = requests.post(WEBHOOK_URL, json=push_payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error response: {response.text}")
        
        # Wait and check events
        time.sleep(2)
        response = requests.get(EVENTS_URL, timeout=10)
        if response.status_code == 200:
            events = response.json()
            if events:
                latest = events[0]
                print(f"Latest event message: {latest.get('message', 'No message')}")
                
                # Check if it matches assessment format
                expected_format = '"Travis" pushed to "staging" on'
                if expected_format in latest.get('message', ''):
                    print("✅ Message format matches assessment requirements!")
                else:
                    print("❌ Message format needs updating")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")
        return False

def show_assessment_requirements():
    """Show the exact assessment requirements"""
    print("📋 Assessment Requirements:")
    print("=" * 50)
    print("PUSH format:")
    print('  "{author}" pushed to "{to_branch}" on {timestamp}')
    print('  Sample: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC')
    print()
    print("PULL_REQUEST format:")
    print('  "{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}')
    print('  Sample: "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC')
    print()
    print("MERGE format:")
    print('  "{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}')
    print('  Sample: "Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC')
    print()

if __name__ == "__main__":
    print("🚀 Testing Deployed GitHub Webhook Dashboard")
    print("=" * 50)
    print(f"Testing: {BASE_URL}")
    print()
    
    # Show requirements first
    show_assessment_requirements()
    
    # Test deployed application
    if test_deployed_status():
        print("✅ Deployed application is accessible")
    else:
        print("❌ Deployed application has issues")
        exit(1)
    
    # Test webhook format
    test_webhook_format()
    
    print("✅ Testing completed!")
    print("\n📝 Next steps:")
    print("1. Update the webhook processing logic to match assessment format")
    print("2. Deploy the updated code to Render")
    print("3. Test with real GitHub webhooks")
