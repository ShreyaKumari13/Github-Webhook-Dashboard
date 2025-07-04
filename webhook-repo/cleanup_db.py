#!/usr/bin/env python3
"""
Script to clean up the database and remove old records with incorrect timestamp format.
"""

import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/github_webhooks')
DATABASE_NAME = 'github_webhooks'
COLLECTION_NAME = 'events'

# MongoDB client
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def cleanup_database():
    """Remove all existing records to start fresh."""
    try:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} old records from the database.")
        print("Database cleaned up successfully!")
        return True
    except Exception as e:
        print(f"Error cleaning up database: {e}")
        return False

if __name__ == '__main__':
    cleanup_database()
