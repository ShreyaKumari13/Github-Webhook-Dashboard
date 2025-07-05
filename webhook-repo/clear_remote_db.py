#!/usr/bin/env python3
"""
Clear database via HTTP endpoint - works with deployed Render app
"""

import requests
import json

def clear_via_endpoint():
    """Clear database by calling a special endpoint"""
    
    # We'll add this endpoint to the Flask app
    clear_url = "https://github-webhook-dashboard.onrender.com/admin/clear-database"
    
    print("🗑️  Clearing database via HTTP endpoint...")
    
    try:
        response = requests.post(clear_url, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message', 'Database cleared')}")
            print(f"📊 Records deleted: {result.get('deleted_count', 'Unknown')}")
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def check_events_count():
    """Check how many events are currently in the database"""
    
    events_url = "https://github-webhook-dashboard.onrender.com/events"
    
    print("📊 Checking current events count...")
    
    try:
        response = requests.get(events_url, timeout=10)
        
        if response.status_code == 200:
            events = response.json()
            print(f"📈 Current events in database: {len(events)}")
            
            if len(events) > 0:
                print("🔍 Sample events:")
                for i, event in enumerate(events[:3]):
                    print(f"  {i+1}. {event.get('action', 'Unknown')} by {event.get('author', 'Unknown')}")
            else:
                print("✅ Database is empty!")
                
        else:
            print(f"❌ Failed to check events: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking events: {e}")

if __name__ == "__main__":
    print("🗑️  Remote Database Cleaner")
    print("=" * 40)

    # Check current state
    check_events_count()

    print("\n" + "=" * 40)

    # Ask for confirmation
    current_events_response = requests.get("https://github-webhook-dashboard.onrender.com/events", timeout=10)
    if current_events_response.status_code == 200:
        current_count = len(current_events_response.json())
        if current_count > 0:
            print(f"⚠️  WARNING: This will delete ALL {current_count} webhook events!")
            confirm = input("Type 'YES' to confirm deletion: ")
            if confirm == 'YES':
                clear_via_endpoint()
                print("\n📊 Checking results...")
                check_events_count()
            else:
                print("❌ Operation cancelled")
        else:
            print("✅ Database is already empty!")
    else:
        print("❌ Could not check current database state")
        print("🔧 Proceeding with clear operation...")
        clear_via_endpoint()
