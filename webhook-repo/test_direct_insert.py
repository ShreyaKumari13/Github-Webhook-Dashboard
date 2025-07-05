#!/usr/bin/env python3
"""
Test direct database insertion via API endpoint
"""

import requests
import json
import time

BASE_URL = "https://github-webhook-dashboard.onrender.com"

def test_manual_insert():
    """Test manual database insertion via a custom endpoint"""
    print("🧪 Testing manual database insertion...")
    
    # Create a test endpoint payload
    test_data = {
        "request_id": "test123",
        "author": "ManualTest",
        "action": "PUSH",
        "from_branch": None,
        "to_branch": "main",
        "message": "Manual test insertion"
    }
    
    # We'll send this as a webhook but with a special marker
    webhook_payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "ManualTest"
        },
        "sender": {
            "login": "ManualTest"
        },
        "head_commit": {
            "id": "test123456789012345678901234567890abcd",
            "message": "Manual test commit",
            "timestamp": "2025-07-05T20:00:00Z",
            "author": {
                "name": "ManualTest"
            }
        },
        "commits": [
            {
                "id": "test123456789012345678901234567890abcd",
                "message": "Manual test commit",
                "timestamp": "2025-07-05T20:00:00Z",
                "author": {
                    "name": "ManualTest"
                }
            }
        ]
    }
    
    headers = {
        "X-GitHub-Event": "push",
        "Content-Type": "application/json"
    }
    
    try:
        print("Sending manual test webhook...")
        response = requests.post(f"{BASE_URL}/webhook", json=webhook_payload, headers=headers, timeout=15)
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Wait for processing
        time.sleep(5)
        
        # Check database
        db_response = requests.get(f"{BASE_URL}/db-status", timeout=10)
        if db_response.status_code == 200:
            db_data = db_response.json()
            print(f"Database count: {db_data.get('document_count', 0)}")
        
        # Check events
        events_response = requests.get(f"{BASE_URL}/events", timeout=10)
        if events_response.status_code == 200:
            events = events_response.json()
            print(f"Events count: {len(events)}")
            for i, event in enumerate(events):
                print(f"Event {i+1}: {event.get('message', 'No message')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_database_table():
    """Check if the database table exists and is accessible"""
    print("\n🔍 Checking database table structure...")
    
    try:
        # Check database status
        response = requests.get(f"{BASE_URL}/db-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Database connected: {data.get('connected', False)}")
            print(f"Table: {data.get('table', 'Unknown')}")
            print(f"Document count: {data.get('document_count', 0)}")
            
            if data.get('connected'):
                print("✅ Database connection is working")
            else:
                print("❌ Database connection failed")
                print(f"Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Failed to check database status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    print("🔧 Testing Direct Database Insertion")
    print("=" * 50)
    
    # Check database first
    check_database_table()
    
    # Test manual insertion
    test_manual_insert()
    
    print("\n✅ Testing completed!")
