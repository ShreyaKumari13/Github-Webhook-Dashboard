#!/usr/bin/env python3
"""
Direct database clear using DATABASE_URL
This connects directly to your PostgreSQL database
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def clear_database_direct():
    """Clear database using direct connection"""
    
    # You'll need to set your DATABASE_URL
    # Get it from your Render dashboard: https://dashboard.render.com
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found!")
        print("🔧 Please set DATABASE_URL environment variable")
        print("📍 Get it from: https://dashboard.render.com → Your Service → Environment")
        return False
    
    try:
        print("🔄 Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        # Check current count
        cursor.execute("SELECT COUNT(*) as count FROM webhook_events")
        result = cursor.fetchone()
        current_count = result['count'] if result else 0
        
        print(f"📊 Current events in database: {current_count}")
        
        if current_count == 0:
            print("✅ Database is already empty!")
            return True
        
        # Show sample records
        print("🔍 Sample records to be deleted:")
        cursor.execute("SELECT author, action, to_branch FROM webhook_events ORDER BY timestamp DESC LIMIT 3")
        samples = cursor.fetchall()
        for i, record in enumerate(samples):
            print(f"  {i+1}. {record['action']} by {record['author']} to {record['to_branch']}")
        
        # Clear all records
        print(f"\n🗑️  Deleting {current_count} records...")
        cursor.execute("DELETE FROM webhook_events")
        deleted_count = cursor.rowcount
        
        # Reset sequence
        cursor.execute("ALTER SEQUENCE webhook_events_id_seq RESTART WITH 1")
        
        conn.commit()
        
        # Verify
        cursor.execute("SELECT COUNT(*) as count FROM webhook_events")
        final_result = cursor.fetchone()
        final_count = final_result['count'] if final_result else 0
        
        cursor.close()
        conn.close()
        
        print(f"✅ Successfully deleted {deleted_count} records")
        print(f"📊 Records remaining: {final_count}")
        print("🔄 Auto-increment sequence reset")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🗑️  Direct Database Clear")
    print("=" * 30)
    
    # Check if DATABASE_URL is set
    if not os.getenv('DATABASE_URL'):
        print("⚠️  DATABASE_URL not found in environment variables")
        print("\n🔧 To set it:")
        print("1. Go to https://dashboard.render.com")
        print("2. Click on your webhook service")
        print("3. Go to Environment tab")
        print("4. Copy the DATABASE_URL value")
        print("5. Set it as environment variable:")
        print("   Windows: set DATABASE_URL=your_database_url")
        print("   Mac/Linux: export DATABASE_URL=your_database_url")
        print("\n💡 Or create a .env file with:")
        print("DATABASE_URL=your_database_url")
    else:
        clear_database_direct()
    
    print("=" * 30)
