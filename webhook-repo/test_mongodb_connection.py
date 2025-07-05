#!/usr/bin/env python3
"""
Test script to verify MongoDB Atlas connection
"""

import pymongo
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB Atlas connection and basic operations"""
    
    print("🔍 Testing MongoDB Atlas Connection...")
    print("=" * 50)
    
    # Get connection string from environment
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("❌ ERROR: MONGO_URI not found in environment variables")
        return False
    
    print(f"📡 Connection URI: {mongo_uri[:50]}...")
    
    try:
        # Create MongoDB client
        print("\n1️⃣ Creating MongoDB client...")
        client = pymongo.MongoClient(mongo_uri)
        
        # Test connection with ping
        print("2️⃣ Testing connection with ping...")
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Get database and collection
        print("3️⃣ Accessing database and collection...")
        db = client['github_webhooks']
        collection = db['events']
        print(f"✅ Database: {db.name}")
        print(f"✅ Collection: {collection.name}")
        
        # Test write operation
        print("4️⃣ Testing write operation...")
        test_document = {
            'request_id': 'test_connection_' + str(int(datetime.now().timestamp())),
            'author': 'test_user',
            'action': 'TEST',
            'from_branch': 'test_branch',
            'to_branch': 'main',
            'timestamp': datetime.utcnow()
        }
        
        result = collection.insert_one(test_document)
        print(f"✅ Document inserted with ID: {result.inserted_id}")
        
        # Test read operation
        print("5️⃣ Testing read operation...")
        found_document = collection.find_one({'_id': result.inserted_id})
        if found_document:
            print(f"✅ Document found: {found_document['action']} by {found_document['author']}")
        else:
            print("❌ Document not found")
            return False
        
        # Test update operation
        print("6️⃣ Testing update operation...")
        update_result = collection.update_one(
            {'_id': result.inserted_id},
            {'$set': {'action': 'TEST_UPDATED'}}
        )
        print(f"✅ Document updated: {update_result.modified_count} document(s)")
        
        # Test delete operation (cleanup)
        print("7️⃣ Cleaning up test document...")
        delete_result = collection.delete_one({'_id': result.inserted_id})
        print(f"✅ Test document deleted: {delete_result.deleted_count} document(s)")
        
        # Show collection stats
        print("8️⃣ Collection statistics...")
        doc_count = collection.count_documents({})
        print(f"✅ Total documents in collection: {doc_count}")
        
        # Test indexes
        print("9️⃣ Testing indexes...")
        indexes = list(collection.list_indexes())
        print(f"✅ Available indexes: {len(indexes)}")
        for idx in indexes:
            print(f"   - {idx['name']}: {idx.get('key', {})}")
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! MongoDB Atlas is working correctly!")
        print("=" * 50)
        
        return True
        
    except pymongo.errors.ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        return False
    except pymongo.errors.AuthenticationFailed as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Check your username and password in the connection string")
        return False
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {e}")
        print("💡 Check your network connection and MongoDB Atlas network access settings")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        try:
            client.close()
            print("🔌 MongoDB connection closed")
        except:
            pass

if __name__ == "__main__":
    success = test_mongodb_connection()
    if success:
        print("\n✅ Your MongoDB Atlas database is ready for deployment!")
    else:
        print("\n❌ Please fix the database connection issues before deploying.")
