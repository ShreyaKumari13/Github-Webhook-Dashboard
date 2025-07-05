#!/usr/bin/env python3
"""
Test PostgreSQL connection for GitHub Webhook Dashboard
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

print("Testing PostgreSQL connection...")
print(f"DATABASE_URL exists: {bool(DATABASE_URL)}")
print(f"DATABASE_URL: {DATABASE_URL[:50]}...")

try:
    # Test connection
    print("🔄 Connecting to PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    
    print("✅ PostgreSQL connection successful!")
    
    # Test database operations
    print("🔄 Testing database operations...")
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhook_events (
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,
            repository VARCHAR(255),
            actor VARCHAR(255),
            action VARCHAR(100),
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            raw_payload JSONB
        )
    """)
    
    print("✅ Table created successfully!")
    
    # Test insert
    cursor.execute("""
        INSERT INTO webhook_events 
        (event_type, repository, actor, action, message)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, ('test', 'test-repo', 'test-user', 'test action', 'Test message'))
    
    result = cursor.fetchone()
    test_id = result['id']
    print(f"✅ Test record inserted with ID: {test_id}")
    
    # Test query
    cursor.execute("SELECT COUNT(*) as count FROM webhook_events")
    count_result = cursor.fetchone()
    count = count_result['count']
    print(f"✅ Total records in database: {count}")
    
    # Clean up test record
    cursor.execute("DELETE FROM webhook_events WHERE id = %s", (test_id,))
    print("✅ Test record cleaned up")
    
    # Commit changes
    conn.commit()
    cursor.close()
    conn.close()
    
    print("🎉 All PostgreSQL tests passed!")
    
except Exception as e:
    print(f"❌ PostgreSQL test failed: {e}")
    print("❌ Connection failed")
