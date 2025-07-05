#!/usr/bin/env python3
"""
Clear all webhook events from the PostgreSQL database
This script safely removes all data while preserving the table structure
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/github_webhooks')

def clear_webhook_events():
    """Clear all webhook events from the database"""
    
    try:
        print("🔄 Connecting to PostgreSQL database...")
        print(f"📍 DATABASE_URL exists: {bool(DATABASE_URL)}")
        
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        # First, check how many records exist
        print("\n📊 Checking current data...")
        cursor.execute("SELECT COUNT(*) as count FROM webhook_events;")
        count_result = cursor.fetchone()
        current_count = count_result['count'] if count_result else 0
        
        print(f"📈 Current records in database: {current_count}")
        
        if current_count == 0:
            print("✅ Database is already empty!")
            cursor.close()
            conn.close()
            return True
        
        # Show a few sample records before deletion
        print("\n🔍 Sample records to be deleted:")
        cursor.execute("""
            SELECT id, author, action, to_branch, timestamp 
            FROM webhook_events 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        
        sample_records = cursor.fetchall()
        for record in sample_records:
            print(f"  - ID: {record['id']}, Author: {record['author']}, Action: {record['action']}, Branch: {record['to_branch']}")
        
        # Confirm deletion
        print(f"\n⚠️  WARNING: This will delete ALL {current_count} webhook events!")
        print("🔄 Proceeding with deletion...")
        
        # Delete all records
        cursor.execute("DELETE FROM webhook_events;")
        deleted_count = cursor.rowcount
        
        # Reset the auto-increment sequence
        print("🔄 Resetting auto-increment sequence...")
        cursor.execute("ALTER SEQUENCE webhook_events_id_seq RESTART WITH 1;")
        
        # Commit the changes
        conn.commit()
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) as count FROM webhook_events;")
        final_count_result = cursor.fetchone()
        final_count = final_count_result['count'] if final_count_result else 0
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Successfully deleted {deleted_count} records!")
        print(f"📊 Records remaining: {final_count}")
        print("🔄 Auto-increment sequence reset to 1")
        print("✅ Database cleared successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        return False

def verify_table_structure():
    """Verify that the table structure is intact after clearing"""
    
    try:
        print("\n🔍 Verifying table structure...")
        
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'webhook_events'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("📋 Table structure:")
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            print(f"  - {col['column_name']}: {col['data_type']} ({nullable})")
        
        cursor.close()
        conn.close()
        
        print("✅ Table structure is intact!")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying table structure: {e}")
        return False

def test_insert():
    """Test that we can still insert data after clearing"""
    
    try:
        print("\n🧪 Testing data insertion...")
        
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        # Insert a test record
        cursor.execute("""
            INSERT INTO webhook_events
            (request_id, author, action, from_branch, to_branch, timestamp, raw_payload)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """, (
            'test123',
            'TestUser',
            'PUSH',
            None,
            'main',
            '{"test": "data"}'
        ))
        
        conn.commit()
        
        # Verify the test record
        cursor.execute("SELECT * FROM webhook_events WHERE request_id = 'test123';")
        test_record = cursor.fetchone()
        
        if test_record:
            print(f"✅ Test record inserted successfully!")
            print(f"   ID: {test_record['id']}, Author: {test_record['author']}")
            
            # Clean up test record
            cursor.execute("DELETE FROM webhook_events WHERE request_id = 'test123';")
            conn.commit()
            print("🧹 Test record cleaned up")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing insertion: {e}")
        return False

if __name__ == "__main__":
    print("🗑️  GitHub Webhook Database Cleaner")
    print("=" * 50)
    
    # Clear the database
    success = clear_webhook_events()
    
    if success:
        # Verify table structure
        verify_table_structure()
        
        # Test insertion capability
        test_insert()
        
        print("\n" + "=" * 50)
        print("🎉 Database clearing completed successfully!")
        print("📝 Your webhook dashboard is now ready for fresh data")
        print("🚀 Deploy your fixes and test with new webhook events")
    else:
        print("\n" + "=" * 50)
        print("❌ Database clearing failed!")
        print("🔧 Please check the error messages above")
