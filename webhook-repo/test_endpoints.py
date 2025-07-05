#!/usr/bin/env python3
"""
Test what endpoints are available on the deployed app
"""

import requests

def test_endpoints():
    base_url = "https://github-webhook-dashboard.onrender.com"
    
    endpoints = [
        "/",
        "/health", 
        "/events",
        "/admin/clear-database"
    ]
    
    print("🔍 Testing available endpoints...")
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            if endpoint == "/admin/clear-database":
                # Test POST for clear endpoint
                response = requests.post(url, timeout=10)
            else:
                # Test GET for others
                response = requests.get(url, timeout=10)
                
            print(f"✅ {endpoint}: HTTP {response.status_code}")
            
            if endpoint == "/events" and response.status_code == 200:
                events = response.json()
                print(f"   📊 Current events: {len(events)}")
                
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

if __name__ == "__main__":
    test_endpoints()
