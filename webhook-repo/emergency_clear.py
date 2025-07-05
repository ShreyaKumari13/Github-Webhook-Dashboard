#!/usr/bin/env python3
"""
Emergency database clear - connects directly to PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def clear_database():
    """Clear database with your specific DATABASE_URL"""
    
    # Replace this with your actual DATABASE_URL from Render dashboard
    # Get it from: https://dashboard.render.com → Your Service → Environment
    DATABASE_URL = "postgresql://github_webhooks_user:YOUR_PASSWORD@dpg-YOUR_HOST/github_webhooks"
    
    print("🔧 INSTRUCTIONS:")
    print("1. Go to https://dashboard.render.com")
    print("2. Click on your webhook service")
    print("3. Go to Environment tab")
    print("4. Copy the DATABASE_URL value")
    print("5. Replace the DATABASE_URL in this script")
    print("6. Run this script again")
    print()
    
    # Uncomment and modify this section once you have your DATABASE_URL:
    """
    try:
        print("🔄 Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        # Check current count
        cursor.execute("SELECT COUNT(*) as count FROM webhook_events")
        result = cursor.fetchone()
        current_count = result['count'] if result else 0
        
        print(f"📊 Current events: {current_count}")
        
        if current_count > 0:
            # Delete all records
            print(f"🗑️  Deleting {current_count} records...")
            cursor.execute("DELETE FROM webhook_events")
            deleted_count = cursor.rowcount
            
            # Reset sequence
            cursor.execute("ALTER SEQUENCE webhook_events_id_seq RESTART WITH 1")
            
            conn.commit()
            print(f"✅ Deleted {deleted_count} records")
        else:
            print("✅ Database already empty")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    """

if __name__ == "__main__":
    clear_database()
