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
import time
from datetime import datetime
from flask import Flask, request, jsonify, render_template
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

        # Create connection pool
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,  # min and max connections
            DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        
        # Test connection and create table
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # Create events table matching the assessment schema requirements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS webhook_events (
                id SERIAL PRIMARY KEY,
                request_id VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                action VARCHAR(100) NOT NULL,
                from_branch VARCHAR(255),
                to_branch VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_payload JSONB,
                event_type VARCHAR(100)
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

def format_timestamp_with_ordinal(dt):
    """Format datetime with ordinal suffix (1st, 2nd, 3rd, 4th, etc.)."""
    day = dt.day
    suffix = 'st' if day in [1, 21, 31] else 'nd' if day in [2, 22] else 'rd' if day in [3, 23] else 'th'
    return dt.strftime(f"{day}{suffix} %B %Y - %I:%M %p UTC")

def format_webhook_message(event_type, payload):
    """Format webhook payload according to assessment requirements."""
    try:
        # Generate request_id using commit hash for push, PR ID for pull requests
        request_id = None
        author = None
        action = None
        from_branch = None
        to_branch = None
        # Default timestamp with proper ordinal formatting
        timestamp = format_timestamp_with_ordinal(datetime.now())

        if event_type == 'push':
            # Extract push information - try multiple fields for author
            author = None

            # Try different ways to get the author
            if payload.get('pusher', {}).get('name'):
                author = payload['pusher']['name']
            elif payload.get('head_commit', {}).get('author', {}).get('name'):
                author = payload['head_commit']['author']['name']
            elif payload.get('sender', {}).get('login'):
                author = payload['sender']['login']
            elif payload.get('commits') and len(payload['commits']) > 0:
                author = payload['commits'][0].get('author', {}).get('name')
            else:
                author = 'Unknown'

            to_branch = payload.get('ref', '').replace('refs/heads/', '')
            commits = payload.get('commits', [])

            # Use commit hash as request_id
            if commits and len(commits) > 0:
                request_id = commits[0].get('id', 'unknown')[:7]  # Short commit hash
            elif payload.get('head_commit', {}).get('id'):
                request_id = payload['head_commit']['id'][:7]
            else:
                request_id = 'push_' + str(hash(str(payload)))[:7]

            action = 'PUSH'
            from_branch = None  # Not applicable for push

            # Use GitHub timestamp if available - try head_commit first, then commits array
            timestamp_str = None
            if payload.get('head_commit', {}).get('timestamp'):
                timestamp_str = payload['head_commit']['timestamp']
            elif commits and len(commits) > 0 and commits[0].get('timestamp'):
                timestamp_str = commits[0]['timestamp']

            if timestamp_str:
                try:
                    # Handle timezone format like "2025-07-06T01:08:07+05:30"
                    if '+' in timestamp_str and not timestamp_str.endswith('Z'):
                        github_time = datetime.fromisoformat(timestamp_str)
                    else:
                        github_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    timestamp = format_timestamp_with_ordinal(github_time)
                except Exception:
                    timestamp = format_timestamp_with_ordinal(datetime.now())
            else:
                timestamp = format_timestamp_with_ordinal(datetime.now())

            # Format: {author} pushed to {to_branch} on {timestamp}
            message = f'"{author}" pushed to "{to_branch}" on {timestamp}'

        elif event_type == 'pull_request':
            # Extract pull request information
            pr = payload.get('pull_request', {})
            pr_action = payload.get('action', 'opened')

            # Check if this is a merge (PR closed and merged)
            if pr_action == 'closed' and pr.get('merged', False):
                # Handle merge action (when PR is closed and merged)
                author = payload.get('sender', {}).get('login', 'Unknown')
                from_branch = pr.get('head', {}).get('ref', 'Unknown')
                to_branch = pr.get('base', {}).get('ref', 'Unknown')
                request_id = str(pr.get('number', 'unknown'))
                action = 'MERGE'

                # Use GitHub timestamp if available
                if pr.get('merged_at'):
                    try:
                        github_time = datetime.fromisoformat(pr['merged_at'].replace('Z', '+00:00'))
                        timestamp = format_timestamp_with_ordinal(github_time)
                    except Exception:
                        timestamp = format_timestamp_with_ordinal(datetime.now())
                else:
                    timestamp = format_timestamp_with_ordinal(datetime.now())

                # Format: {author} merged branch {from_branch} to {to_branch} on {timestamp}
                message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'

            elif pr_action == 'opened':
                # Only process 'opened' action as submission
                author = pr.get('user', {}).get('login', 'Unknown')
                from_branch = pr.get('head', {}).get('ref', 'Unknown')
                to_branch = pr.get('base', {}).get('ref', 'Unknown')
                request_id = str(pr.get('number', 'unknown'))
                action = 'PULL_REQUEST'

                # Use GitHub timestamp if available
                if pr.get('created_at'):
                    try:
                        github_time = datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00'))
                        timestamp = format_timestamp_with_ordinal(github_time)
                    except Exception:
                        timestamp = format_timestamp_with_ordinal(datetime.now())
                else:
                    timestamp = format_timestamp_with_ordinal(datetime.now())

                # Format: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
                message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
            else:
                # Skip other PR actions (synchronized, etc.)
                return None

        else:
            # Skip other event types
            return None

        return {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': datetime.now(),
            'message': message
        }

    except Exception as e:
        print(f"Error formatting message: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events."""
    db_error = None
    db_success = False

    try:
        # Get headers
        signature = request.headers.get('X-Hub-Signature-256')
        event_type = request.headers.get('X-GitHub-Event')

        print(f"🔔 Received webhook: {event_type}")

        # Get payload
        payload_body = request.get_data()

        # Verify signature (optional for testing)
        # if not verify_github_signature(payload_body, signature):
        #     return jsonify({'error': 'Invalid signature'}), 401

        # Parse JSON payload
        try:
            payload = json.loads(payload_body.decode('utf-8'))
            print(f"📦 Payload keys: {list(payload.keys())}")

            # Debug: Print relevant fields for push events
            if event_type == 'push':
                print(f"🔍 Push debug:")
                print(f"  - pusher: {payload.get('pusher')}")
                print(f"  - sender: {payload.get('sender')}")
                print(f"  - head_commit: {payload.get('head_commit', {}).get('author')}")
                print(f"  - ref: {payload.get('ref')}")

        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON payload'}), 400

        # Format the message
        formatted = format_webhook_message(event_type, payload)

        # Skip if event is not relevant (e.g., PR actions other than 'opened')
        if formatted is None:
            return jsonify({
                'status': 'skipped',
                'event_type': event_type,
                'message': 'Event not processed (not relevant for dashboard)'
            }), 200

        # Store in database with better error handling
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()



                cursor.execute("""
                    INSERT INTO webhook_events
                    (request_id, author, action, from_branch, to_branch, timestamp, raw_payload, event_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    formatted['request_id'],
                    formatted['author'],
                    formatted['action'],
                    formatted['from_branch'],
                    formatted['to_branch'],
                    formatted['timestamp'],
                    json.dumps(payload),
                    event_type
                ))
                conn.commit()
                cursor.close()
                print(f"✅ Stored {formatted['action']} event by {formatted['author']}")
                db_success = True
            except Exception as e:
                db_error = str(e)
                print(f"❌ Database insert failed: {e}")
                # Try to rollback
                try:
                    conn.rollback()
                except:
                    pass
            finally:
                return_db_connection(conn)
        else:
            db_error = "No database connection available"
            print("❌ No database connection available")

        # Include database status in response for debugging
        response_data = {
            'status': 'success',
            'event_type': event_type,
            'action': formatted['action'],
            'message': formatted['message'],
            'db_success': db_success
        }

        if db_error:
            response_data['db_error'] = db_error

        return jsonify(response_data), 200

    except Exception as e:
        print(f"❌ Webhook processing error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

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
                SELECT request_id, author, action, from_branch, to_branch, timestamp
                FROM webhook_events
                ORDER BY timestamp DESC
                LIMIT 50
            """)

            events = []
            for row in cursor.fetchall():
                # Reconstruct the message based on action type with proper ordinal formatting
                if row['timestamp']:
                    timestamp_str = format_timestamp_with_ordinal(row['timestamp'])
                else:
                    timestamp_str = 'Unknown time'

                if row['action'] == 'PUSH':
                    message = f'"{row["author"]}" pushed to "{row["to_branch"]}" on {timestamp_str}'
                elif row['action'] == 'PULL_REQUEST':
                    message = f'"{row["author"]}" submitted a pull request from "{row["from_branch"]}" to "{row["to_branch"]}" on {timestamp_str}'
                elif row['action'] == 'MERGE':
                    message = f'"{row["author"]}" merged branch "{row["from_branch"]}" to "{row["to_branch"]}" on {timestamp_str}'
                else:
                    message = f'"{row["author"]}" performed {row["action"]} on {timestamp_str}'

                events.append({
                    'request_id': row['request_id'],
                    'author': row['author'],
                    'action': row['action'],
                    'from_branch': row['from_branch'],
                    'to_branch': row['to_branch'],
                    'message': message,
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



@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('index.html')

# Initialize database on startup
init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
