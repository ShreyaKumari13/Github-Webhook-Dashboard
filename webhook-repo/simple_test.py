import pymongo
import ssl

# Test with NEW MongoDB Atlas cluster
mongo_uri = "mongodb+srv://shreyakumari2713:QjS4kJ9qRXArjuQr@cluster0.8nehy60.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print("Testing MongoDB Atlas connection with SSL fixes...")
print("URI:", mongo_uri[:50] + "...")

try:
    # Test connection with clean configuration (no conflicting SSL options)
    client = pymongo.MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000
    )

    print("🔄 Attempting to ping MongoDB...")
    client.admin.command('ping')
    print("✅ SUCCESS: MongoDB Atlas connection working!")

    # Test database access
    db = client['github_webhooks']
    collection = db['events']
    count = collection.count_documents({})
    print(f"✅ Database accessible. Current document count: {count}")

    # Test insert
    test_doc = {"test": "ssl_fix", "timestamp": "2024-01-01"}
    result = collection.insert_one(test_doc)
    print(f"✅ Test document inserted with ID: {result.inserted_id}")

    # Clean up
    collection.delete_one({"_id": result.inserted_id})
    print("✅ Test document cleaned up")

    client.close()
    print("✅ All tests passed!")

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("❌ Connection failed")
