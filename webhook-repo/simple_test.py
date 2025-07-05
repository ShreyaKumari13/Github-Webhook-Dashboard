import pymongo
import ssl

# Direct connection string test - using exact format from MongoDB Atlas
mongo_uri = "mongodb+srv://shreyakumari2713:bC9fiHqESCWqAuhF@cluster0.mkyihia.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print("Testing MongoDB Atlas connection...")
print("URI:", mongo_uri[:50] + "...")

try:
    # Test connection with updated PyMongo
    client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ SUCCESS: MongoDB Atlas connection working!")
    
    # Test database access
    db = client['github_webhooks']
    collection = db['events']
    count = collection.count_documents({})
    print(f"✅ Database accessible. Current document count: {count}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("❌ Connection failed")
