#!/usr/bin/env python3
"""
Test script for GitHub webhook functionality
"""

import requests
import json
import hashlib
import hmac
import time
from datetime import datetime

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
            "name": "test_user"
        },
        "repository": {
            "name": "test-repo"
        },
        "commits": [
            {
                "id": "abc123",
                "message": "Test commit"
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
    print(f"Push event test: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_pull_request_event():
    """Test a pull request event webhook"""
    payload = {
        "action": "opened",
        "pull_request": {
            "user": {
                "login": "test_user"
            },
            "base": {
                "ref": "main"
            },
            "head": {
                "ref": "feature/test"
            }
        },
        "repository": {
            "name": "test-repo"
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
    print(f"Pull request event test: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_merge_event():
    """Test a merge event webhook"""
    payload = {
        "action": "closed",
        "pull_request": {
            "merged": True,
            "user": {
                "login": "test_user"
            },
            "merged_by": {
                "login": "reviewer_user"
            },
            "base": {
                "ref": "main"
            },
            "head": {
                "ref": "feature/test"
            }
        },
        "repository": {
            "name": "test-repo"
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
    print(f"Merge event test: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_api_endpoint():
    """Test the events API endpoint"""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            events = response.json()
            print(f"API test: Retrieved {len(events)} events")
            return True
        else:
            print(f"API test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"API test error: {e}")
        return False

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"Health check: {health_data['status']}")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting webhook tests...")
    print("=" * 50)
    
    # Test health endpoint first
    if not test_health_endpoint():
        print("Health check failed. Make sure the server is running.")
        return
    
    # Wait a moment
    time.sleep(1)
    
    # Test webhook events
    tests = [
        ("Push Event", test_push_event),
        ("Pull Request Event", test_pull_request_event),
        ("Merge Event", test_merge_event),
        ("API Endpoint", test_api_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            time.sleep(1)  # Wait between tests
        except Exception as e:
            print(f"Error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()
