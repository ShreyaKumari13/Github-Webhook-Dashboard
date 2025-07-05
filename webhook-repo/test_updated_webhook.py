#!/usr/bin/env python3
"""
Test the updated webhook endpoint with better error reporting
"""

import requests
import json
import time

BASE_URL = "https://github-webhook-dashboard.onrender.com"

def test_updated_webhook():
    """Test the updated webhook endpoint"""
    print("🧪 Testing updated webhook endpoint...")
    
    # Test webhook payload
    push_payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "UpdatedTest",
            "email": "test@example.com"
        },
        "sender": {
            "login": "UpdatedTest"
        },
        "head_commit": {
            "id": "updated123456789012345678901234567890abcd",
            "message": "Updated test commit",
            "timestamp": "2025-07-05T20:10:00Z",
            "author": {
                "name": "UpdatedTest",
                "email": "test@example.com"
            }
        },
        "commits": [
            {
                "id": "updated123456789012345678901234567890abcd",
                "message": "Updated test commit",
                "timestamp": "2025-07-05T20:10:00Z",
                "author": {
                    "name": "UpdatedTest",
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
        print("Sending updated webhook...")
        response = requests.post(f"{BASE_URL}/webhook", json=push_payload, headers=headers, timeout=15)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data: {json.dumps(data, indent=2)}")
            
            # Check if database operation was successful
            if data.get('db_success'):
                print("✅ Database insertion was successful!")
            else:
                print("❌ Database insertion failed!")
                if 'db_error' in data:
                    print(f"Database error: {data['db_error']}")
        else:
            print(f"Error response: {response.text}")
        
        # Wait and check events
        time.sleep(3)
        events_response = requests.get(f"{BASE_URL}/events", timeout=10)
        if events_response.status_code == 200:
            events = events_response.json()
            print(f"Events after webhook: {len(events)}")
            if events:
                print(f"Latest event: {events[0].get('message', 'No message')}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")
        return False

def test_direct_insert():
    """Test the direct database insert endpoint"""
    print("\n🧪 Testing direct database insert...")
    
    try:
        response = requests.post(f"{BASE_URL}/admin/test-insert", timeout=15)
        print(f"Direct insert status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Direct insert response: {json.dumps(data, indent=2)}")
            
            # Check events after direct insert
            time.sleep(2)
            events_response = requests.get(f"{BASE_URL}/events", timeout=10)
            if events_response.status_code == 200:
                events = events_response.json()
                print(f"Events after direct insert: {len(events)}")
                if events:
                    print(f"Latest event: {events[0]}")
        else:
            print(f"Error response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error testing direct insert: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Updated Webhook with Better Error Reporting")
    print("=" * 60)
    
    # Check initial state
    print("📊 Initial state:")
    try:
        db_response = requests.get(f"{BASE_URL}/db-status", timeout=10)
        if db_response.status_code == 200:
            db_data = db_response.json()
            print(f"Database connected: {db_data.get('connected', False)}")
            print(f"Event count: {db_data.get('document_count', 0)}")
    except Exception as e:
        print(f"Error checking initial state: {e}")
    
    print("\n" + "=" * 60)
    
    # Test direct database insert first
    if test_direct_insert():
        print("✅ Direct database insert works")
    else:
        print("❌ Direct database insert failed")
    
    # Test webhook
    if test_updated_webhook():
        print("✅ Webhook test completed")
    else:
        print("❌ Webhook test failed")
    
    print("\n✅ All tests completed!")
