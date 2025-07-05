#!/usr/bin/env python3
"""
Quick database clear script
"""

import requests
import json

def clear_database():
    """Clear the database via the admin endpoint"""
    
    print("🗑️  Clearing webhook database...")
    
    # First check current events
    try:
        events_response = requests.get("https://github-webhook-dashboard.onrender.com/events", timeout=15)
        if events_response.status_code == 200:
            current_events = events_response.json()
            print(f"📊 Current events in database: {len(current_events)}")
            
            if len(current_events) == 0:
                print("✅ Database is already empty!")
                return
                
            # Show sample events
            print("🔍 Sample events to be deleted:")
            for i, event in enumerate(current_events[:3]):
                print(f"  {i+1}. {event.get('action', 'Unknown')} by {event.get('author', 'Unknown')}")
        else:
            print(f"⚠️  Could not check current events: HTTP {events_response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not check current events: {e}")
    
    # Clear the database
    try:
        clear_url = "https://github-webhook-dashboard.onrender.com/admin/clear-database"
        
        print(f"\n🔄 Sending clear request to: {clear_url}")
        
        response = requests.post(clear_url, timeout=30)
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📝 Response text: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ Success: {result.get('message', 'Database cleared')}")
                print(f"📊 Records deleted: {result.get('deleted_count', 'Unknown')}")
            except:
                print("✅ Database cleared successfully!")
        else:
            print(f"❌ Clear failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
    
    # Verify clearing worked
    try:
        print("\n🔍 Verifying database is empty...")
        verify_response = requests.get("https://github-webhook-dashboard.onrender.com/events", timeout=15)
        
        if verify_response.status_code == 200:
            remaining_events = verify_response.json()
            print(f"📊 Events remaining: {len(remaining_events)}")
            
            if len(remaining_events) == 0:
                print("✅ Database successfully cleared!")
            else:
                print(f"⚠️  {len(remaining_events)} events still remain")
        else:
            print(f"⚠️  Could not verify: HTTP {verify_response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Could not verify clearing: {e}")

if __name__ == "__main__":
    print("🗑️  Quick Database Clear")
    print("=" * 30)
    clear_database()
    print("=" * 30)
    print("🎯 Clear operation completed!")
