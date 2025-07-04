import requests
import json

# Test health endpoint
print("Testing health endpoint...")
try:
    response = requests.get("http://localhost:5000/health")
    print(f"Health: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Health error: {e}")

# Test events endpoint
print("\nTesting events endpoint...")
try:
    response = requests.get("http://localhost:5000/events")
    events = response.json()
    print(f"Events: {response.status_code} - Found {len(events)} events")
    
    if events:
        print("\nSample events:")
        for i, event in enumerate(events[:3]):
            print(f"{i+1}. Type: {event['event_type']}, Author: {event['author']}, Branch: {event['to_branch']}")
            
except Exception as e:
    print(f"Events error: {e}")

print("\nTest completed!")
