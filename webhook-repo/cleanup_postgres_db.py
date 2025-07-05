#!/usr/bin/env python3
"""
Script to clean up the PostgreSQL database and remove old webhook event records.
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL configuration
DATABASE_URL = os.getenv('DATABASE_URL')

def cleanup_database():
    """Remove all existing webhook event records to start fresh."""
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment variables")
        print("   Please set DATABASE_URL in your .env file")
        return False
        
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get count before deletion
        cursor.execute("SELECT COUNT(*) FROM webhook_events")
        count_before = cursor.fetchone()[0]
        
        # Delete all records
        cursor.execute("DELETE FROM webhook_events")
        
        # Reset the sequence for the ID column
        cursor.execute("ALTER SEQUENCE webhook_events_id_seq RESTART WITH 1")
        
        # Commit the changes
        conn.commit()
        
        print(f"✅ Deleted {count_before} old records from the database.")
        print("✅ Database cleaned up successfully!")
        print("✅ ID sequence reset to start from 1")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up database: {e}")
        return False

def show_database_stats():
    """Show current database statistics."""
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment variables")
        return False
        
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("""
            SELECT COUNT(*) as total_events,
                   COUNT(DISTINCT event_type) as unique_event_types,
                   COUNT(DISTINCT repository) as unique_repositories,
                   MIN(timestamp) as oldest_event,
                   MAX(timestamp) as newest_event
            FROM webhook_events
        """)
        
        stats = cursor.fetchone()
        
        print("📊 Database Statistics:")
        print(f"   Total events: {stats[0]}")
        print(f"   Unique event types: {stats[1]}")
        print(f"   Unique repositories: {stats[2]}")
        print(f"   Oldest event: {stats[3]}")
        print(f"   Newest event: {stats[4]}")
        
        # Get event type breakdown
        cursor.execute("""
            SELECT event_type, COUNT(*) as count
            FROM webhook_events
            GROUP BY event_type
            ORDER BY count DESC
        """)
        
        event_types = cursor.fetchall()
        if event_types:
            print("\n📈 Event Types:")
            for event_type, count in event_types:
                print(f"   {event_type}: {count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error getting database stats: {e}")
        return False

if __name__ == '__main__':
    print("🗄️  PostgreSQL Database Cleanup Tool")
    print("=" * 40)
    
    # Show current stats
    print("\n📊 Current Database Status:")
    show_database_stats()
    
    # Ask for confirmation
    print("\n⚠️  This will delete ALL webhook events from the database!")
    response = input("Are you sure you want to continue? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print("\n🧹 Cleaning up database...")
        success = cleanup_database()
        
        if success:
            print("\n📊 Database Status After Cleanup:")
            show_database_stats()
    else:
        print("❌ Cleanup cancelled.")
