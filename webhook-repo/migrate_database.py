#!/usr/bin/env python3
"""
Database migration script to update the webhook_events table
to match the assessment requirements
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/github_webhooks')

def migrate_database():
    """Migrate the database schema to match assessment requirements"""
    try:
        print("🔄 Connecting to PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        print("📋 Checking current table structure...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'webhook_events'
            ORDER BY ordinal_position;
        """)
        
        current_columns = {row['column_name']: row['data_type'] for row in cursor.fetchall()}
        print(f"Current columns: {list(current_columns.keys())}")
        
        # Check if we need to add new columns
        required_columns = {
            'request_id': 'character varying',
            'author': 'character varying', 
            'action': 'character varying',
            'from_branch': 'character varying',
            'to_branch': 'character varying'
        }
        
        # Add missing columns
        for col_name, col_type in required_columns.items():
            if col_name not in current_columns:
                print(f"➕ Adding column: {col_name}")
                if col_name in ['request_id', 'author', 'action']:
                    # These are required fields
                    cursor.execute(f"""
                        ALTER TABLE webhook_events 
                        ADD COLUMN {col_name} VARCHAR(255) DEFAULT 'unknown';
                    """)
                    # Remove default after adding
                    cursor.execute(f"""
                        ALTER TABLE webhook_events 
                        ALTER COLUMN {col_name} DROP DEFAULT;
                    """)
                else:
                    # These can be nullable
                    cursor.execute(f"""
                        ALTER TABLE webhook_events 
                        ADD COLUMN {col_name} VARCHAR(255);
                    """)
        
        # Update existing records to have proper values
        print("🔄 Updating existing records...")
        cursor.execute("""
            UPDATE webhook_events 
            SET 
                request_id = COALESCE(request_id, 'legacy_' || id::text),
                author = COALESCE(author, actor, 'Unknown'),
                action = CASE 
                    WHEN event_type = 'push' THEN 'PUSH'
                    WHEN event_type = 'pull_request' THEN 'PULL_REQUEST'
                    WHEN event_type = 'merge' THEN 'MERGE'
                    ELSE UPPER(COALESCE(event_type, 'UNKNOWN'))
                END
            WHERE request_id IS NULL OR author IS NULL OR action IS NULL;
        """)
        
        # Create index for better performance
        print("📊 Creating indexes...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_webhook_events_timestamp_new 
            ON webhook_events(timestamp DESC);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_webhook_events_action 
            ON webhook_events(action);
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    print("=" * 50)
    
    success = migrate_database()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("The database schema now matches the assessment requirements.")
    else:
        print("\n❌ Migration failed!")
        print("Please check the error messages above.")
