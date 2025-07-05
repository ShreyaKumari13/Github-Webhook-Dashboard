#!/usr/bin/env python3
"""
Debug database connection and insertion
"""

import requests
import json

def test_database_insertion():
    """Test if we can manually insert data via the webhook"""
    
    webhook_url = "https://github-webhook-dashboard.onrender.com/webhook"
    
    # Create a very simple push payload
    payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "debuguser"
        },
        "sender": {
            "login": "debuguser"
        },
        "head_commit": {
            "id": "debug123",
            "message": "Debug test commit",
            "timestamp": "2025-07-05T19:35:00Z",
            "author": {
                "name": "Debug User",
                "username": "debuguser"
            }
        },
        "repository": {
            "name": "debug-repo"
        }
    }
    
    headers = {
        "X-GitHub-Event": "push",
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing database insertion...")
    
    # Step 1: Check current event count
    print("\n📊 Step 1: Check current events...")
    try:
        events_response = requests.get("https://github-webhook-dashboard.onrender.com/events", timeout=10)
        if events_response.status_code == 200:
            events_before = events_response.json()
            print(f"Events before: {len(events_before)}")
        else:
            print(f"Failed to get events: {events_response.status_code}")
            events_before = []
    except Exception as e:
        print(f"Error getting events: {e}")
        events_before = []
    
    # Step 2: Send webhook
    print("\n🚀 Step 2: Send webhook...")
    try:
        response = requests.post(webhook_url, 
                               json=payload, 
                               headers=headers,
                               timeout=15)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error sending webhook: {e}")
        return
    
    # Step 3: Check if event was added
    print("\n📊 Step 3: Check events after webhook...")
    try:
        events_response = requests.get("https://github-webhook-dashboard.onrender.com/events", timeout=10)
        if events_response.status_code == 200:
            events_after = events_response.json()
            print(f"Events after: {len(events_after)}")
            
            if len(events_after) > len(events_before):
                print("✅ New event was added!")
                latest = events_after[0]
                print(f"Latest event: {latest}")
            else:
                print("❌ No new event was added")
                print("This suggests a database insertion issue")
        else:
            print(f"Failed to get events: {events_response.status_code}")
    except Exception as e:
        print(f"Error checking events: {e}")
    
    # Step 4: Check database status
    print("\n🔍 Step 4: Check database status...")
    try:
        db_response = requests.get("https://github-webhook-dashboard.onrender.com/db-status", timeout=10)
        if db_response.status_code == 200:
            db_status = db_response.json()
            print(f"Database status: {db_status}")
        else:
            print(f"Failed to get DB status: {db_response.status_code}")
    except Exception as e:
        print(f"Error checking DB status: {e}")

if __name__ == "__main__":
    print("🔧 Database Debug Test")
    print("=" * 40)
    test_database_insertion()
    print("=" * 40)
