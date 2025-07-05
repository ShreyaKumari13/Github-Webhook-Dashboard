#!/usr/bin/env python3
"""
GitHub Webhook Dashboard - PostgreSQL Version
A Flask application that receives GitHub webhooks and displays them in a web dashboard.
This version uses PostgreSQL instead of MongoDB for better Render compatibility.
"""

import os
import json
import hashlib
import hmac
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg2.pool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', 'default_secret')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/github_webhooks')

# PostgreSQL connection pool
connection_pool = None

def init_database():
    """Initialize PostgreSQL database and create tables."""
    global connection_pool
    
    try:
        print(f"🔄 Connecting to PostgreSQL...")
        print(f"📍 DATABASE_URL exists: {bool(DATABASE_URL)}")
        
        # Create connection pool
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,  # min and max connections
            DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        
        # Test connection and create table
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # Create events table
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
        
        # Create index for better performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_webhook_events_timestamp 
            ON webhook_events(timestamp DESC)
        """)
        
        conn.commit()
        cursor.close()
        connection_pool.putconn(conn)
        
        print("✅ PostgreSQL connected and tables created")
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def get_db_connection():
    """Get a database connection from the pool."""
    if connection_pool:
        return connection_pool.getconn()
    return None

def return_db_connection(conn):
    """Return a database connection to the pool."""
    if connection_pool and conn:
        connection_pool.putconn(conn)

def verify_github_signature(payload_body, signature_header):
    """Verify GitHub webhook signature."""
    if not signature_header:
        return False
    
    try:
        hash_object = hmac.new(
            GITHUB_WEBHOOK_SECRET.encode('utf-8'),
            msg=payload_body,
            digestmod=hashlib.sha256
        )
        expected_signature = "sha256=" + hash_object.hexdigest()
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception:
        return False

def format_webhook_message(event_type, payload):
    """Format webhook payload into a readable message."""
    try:
        repo_name = payload.get('repository', {}).get('full_name', 'Unknown Repository')
        
        if event_type == 'push':
            pusher = payload.get('pusher', {}).get('name', 'Unknown')
            commits = payload.get('commits', [])
            commit_count = len(commits)
            branch = payload.get('ref', '').replace('refs/heads/', '')
            
            return {
                'type': 'push',
                'repository': repo_name,
                'actor': pusher,
                'action': f'pushed {commit_count} commit(s)',
                'message': f"🚀 {pusher} pushed {commit_count} commit(s) to {branch} in {repo_name}"
            }
            
        elif event_type == 'pull_request':
            action = payload.get('action', 'unknown')
            pr = payload.get('pull_request', {})
            pr_number = pr.get('number', 'Unknown')
            pr_title = pr.get('title', 'Unknown')
            actor = payload.get('sender', {}).get('login', 'Unknown')
            
            return {
                'type': 'pull_request',
                'repository': repo_name,
                'actor': actor,
                'action': f'{action} PR #{pr_number}',
                'message': f"🔄 {actor} {action} pull request #{pr_number}: {pr_title} in {repo_name}"
            }
            
        elif event_type == 'merge':
            actor = payload.get('sender', {}).get('login', 'Unknown')
            return {
                'type': 'merge',
                'repository': repo_name,
                'actor': actor,
                'action': 'merged changes',
                'message': f"🔀 {actor} merged changes in {repo_name}"
            }
            
        else:
            actor = payload.get('sender', {}).get('login', 'Unknown')
            return {
                'type': event_type,
                'repository': repo_name,
                'actor': actor,
                'action': f'{event_type} event',
                'message': f"📝 {actor} triggered {event_type} event in {repo_name}"
            }
            
    except Exception as e:
        print(f"Error formatting message: {e}")
        return {
            'type': event_type,
            'repository': 'Unknown',
            'actor': 'Unknown',
            'action': 'unknown action',
            'message': f"📝 {event_type} event received"
        }

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events."""
    try:
        # Get headers
        signature = request.headers.get('X-Hub-Signature-256')
        event_type = request.headers.get('X-GitHub-Event')
        
        # Get payload
        payload_body = request.get_data()
        
        # Verify signature (optional for testing)
        # if not verify_github_signature(payload_body, signature):
        #     return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse JSON payload
        try:
            payload = json.loads(payload_body.decode('utf-8'))
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON payload'}), 400
        
        # Format the message
        formatted = format_webhook_message(event_type, payload)
        
        # Store in database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO webhook_events 
                    (event_type, repository, actor, action, message, raw_payload)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    formatted['type'],
                    formatted['repository'],
                    formatted['actor'],
                    formatted['action'],
                    formatted['message'],
                    json.dumps(payload)
                ))
                conn.commit()
                cursor.close()
                print(f"✅ Stored {event_type} event from {formatted['repository']}")
            except Exception as e:
                print(f"❌ Database insert failed: {e}")
            finally:
                return_db_connection(conn)
        
        return jsonify({
            'status': 'success',
            'event_type': event_type,
            'message': formatted['message']
        }), 200
        
    except Exception as e:
        print(f"❌ Webhook processing error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/events')
def get_events():
    """Get recent webhook events."""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify([]), 200
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT event_type, repository, actor, action, message, timestamp
                FROM webhook_events 
                ORDER BY timestamp DESC 
                LIMIT 50
            """)
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    'type': row['event_type'],
                    'repository': row['repository'],
                    'actor': row['actor'],
                    'action': row['action'],
                    'message': row['message'],
                    'timestamp': row['timestamp'].isoformat() if row['timestamp'] else None
                })
            
            cursor.close()
            return jsonify(events), 200
            
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            return jsonify([]), 200
        finally:
            return_db_connection(conn)
            
    except Exception as e:
        print(f"❌ Events endpoint error: {e}")
        return jsonify([]), 200

@app.route('/db-status')
def db_status():
    """Database connection status."""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'connected': False, 'error': 'No connection pool'}), 200
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM webhook_events")
            result = cursor.fetchone()
            count = result['count'] if result else 0
            cursor.close()
            
            return jsonify({
                'connected': True,
                'database': 'PostgreSQL',
                'table': 'webhook_events',
                'document_count': count
            }), 200
            
        except Exception as e:
            return jsonify({'connected': False, 'error': str(e)}), 200
        finally:
            return_db_connection(conn)
            
    except Exception as e:
        return jsonify({'connected': False, 'error': str(e)}), 200

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'GitHub Webhook Dashboard',
        'database': 'PostgreSQL',
        'timestamp': datetime.now().isoformat()
    }), 200

# Initialize database on startup
init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
