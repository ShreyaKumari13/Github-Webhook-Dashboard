import pymongo
import urllib.parse

# Test different connection string formats
username = "shreyakumari2713"
password = "bC9fiHqESCWqAuhF"
cluster = "cluster0.mkyihia.mongodb.net"

print("🔍 Testing different connection string formats...")
print("=" * 60)

# Test 1: URL encode the password
encoded_password = urllib.parse.quote_plus(password)
print(f"Original password: {password}")
print(f"URL encoded password: {encoded_password}")

# Test 2: Try different connection string formats
test_uris = [
    f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0",
    f"mongodb+srv://{username}:{encoded_password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0",
    f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority",
    f"mongodb+srv://{username}:{password}@{cluster}/",
]

for i, uri in enumerate(test_uris, 1):
    print(f"\n🧪 Test {i}: {uri[:50]}...")
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print(f"✅ SUCCESS with format {i}!")
        
        # Test database access
        db = client['github_webhooks']
        collection = db['events']
        count = collection.count_documents({})
        print(f"✅ Database accessible. Document count: {count}")
        client.close()
        break
        
    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}...")
        
print("\n" + "=" * 60)
