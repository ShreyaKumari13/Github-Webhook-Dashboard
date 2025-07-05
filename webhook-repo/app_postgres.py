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
        
        # Create events table matching the MongoDB schema from assessment
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS webhook_events (
                id SERIAL PRIMARY KEY,
                request_id VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                action VARCHAR(100) NOT NULL,
                from_branch VARCHAR(255),
                to_branch VARCHAR(255),
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
    """Format webhook payload according to assessment requirements."""
    try:
        # Generate request_id using commit hash for push, PR ID for pull requests
        request_id = None
        author = None
        action = None
        from_branch = None
        to_branch = None
        timestamp = datetime.now().strftime("%d %B %Y - %I:%M %p UTC")

        if event_type == 'push':
            # Extract push information
            pusher = payload.get('pusher', {}).get('name') or payload.get('sender', {}).get('login', 'Unknown')
            to_branch = payload.get('ref', '').replace('refs/heads/', '')
            commits = payload.get('commits', [])

            # Use commit hash as request_id
            if commits:
                request_id = commits[0].get('id', 'unknown')[:7]  # Short commit hash
            else:
                request_id = 'push_' + str(hash(str(payload)))[:7]

            author = pusher
            action = 'PUSH'
            from_branch = None  # Not applicable for push

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

                # Format: {author} merged branch {from_branch} to {to_branch} on {timestamp}
                message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'

            elif pr_action == 'opened':
                # Only process 'opened' action as submission
                author = pr.get('user', {}).get('login', 'Unknown')
                from_branch = pr.get('head', {}).get('ref', 'Unknown')
                to_branch = pr.get('base', {}).get('ref', 'Unknown')
                request_id = str(pr.get('number', 'unknown'))
                action = 'PULL_REQUEST'

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

        # Skip if event is not relevant (e.g., PR actions other than 'opened')
        if formatted is None:
            return jsonify({
                'status': 'skipped',
                'event_type': event_type,
                'message': 'Event not processed (not relevant for dashboard)'
            }), 200

        # Store in database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO webhook_events
                    (request_id, author, action, from_branch, to_branch, timestamp, raw_payload)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    formatted['request_id'],
                    formatted['author'],
                    formatted['action'],
                    formatted['from_branch'],
                    formatted['to_branch'],
                    formatted['timestamp'],
                    json.dumps(payload)
                ))
                conn.commit()
                cursor.close()
                print(f"✅ Stored {formatted['action']} event by {formatted['author']}")
            except Exception as e:
                print(f"❌ Database insert failed: {e}")
            finally:
                return_db_connection(conn)
        
        return jsonify({
            'status': 'success',
            'event_type': event_type,
            'action': formatted['action'],
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
                SELECT request_id, author, action, from_branch, to_branch, timestamp
                FROM webhook_events
                ORDER BY timestamp DESC
                LIMIT 50
            """)

            events = []
            for row in cursor.fetchall():
                # Reconstruct the message based on action type
                timestamp_str = row['timestamp'].strftime("%d %B %Y - %I:%M %p UTC") if row['timestamp'] else 'Unknown time'

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
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GitHub Webhook Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #24292e; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .status { background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #28a745; }
            .events { background: white; border-radius: 8px; padding: 20px; }
            .event { border-bottom: 1px solid #eee; padding: 15px 0; }
            .event:last-child { border-bottom: none; }
            .event-message { font-weight: bold; margin-bottom: 5px; }
            .event-details { color: #666; font-size: 0.9em; }
            .loading { text-align: center; padding: 20px; color: #666; }
            .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 GitHub Webhook Dashboard</h1>
                <p>Assessment Task - Real-time GitHub webhook events (Push, Pull Request, Merge)</p>
            </div>

            <div class="status" id="status">
                <strong>Database Status:</strong> <span id="db-status">Checking...</span>
            </div>

            <div class="events">
                <h2>Latest Repository Changes</h2>
                <p><em>Polling every 15 seconds for new events...</em></p>
                <div id="events-list" class="loading">Loading events...</div>
            </div>
        </div>

        <script>
            function updateStatus() {
                fetch('/db-status')
                    .then(response => response.json())
                    .then(data => {
                        const statusEl = document.getElementById('db-status');
                        if (data.connected) {
                            statusEl.innerHTML = `✅ PostgreSQL Connected (${data.document_count} events stored)`;
                        } else {
                            statusEl.innerHTML = `❌ Disconnected: ${data.error}`;
                        }
                    })
                    .catch(error => {
                        document.getElementById('db-status').innerHTML = '❌ Error checking status';
                    });
            }

            function updateEvents() {
                fetch('/events')
                    .then(response => response.json())
                    .then(events => {
                        const eventsEl = document.getElementById('events-list');
                        if (events.length === 0) {
                            eventsEl.innerHTML = '<p class="loading">No events yet. Send a webhook to see events here!</p>';
                            return;
                        }

                        eventsEl.innerHTML = events.map(event => `
                            <div class="event">
                                <div class="event-message">${event.message}</div>
                                <div class="event-details">
                                    Action: ${event.action} • Request ID: ${event.request_id}
                                </div>
                            </div>
                        `).join('');
                    })
                    .catch(error => {
                        document.getElementById('events-list').innerHTML = '<div class="error">Error loading events</div>';
                    });
            }

            // Update immediately and then every 15 seconds
            updateStatus();
            updateEvents();
            setInterval(() => {
                updateStatus();
                updateEvents();
            }, 15000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

# Initialize database on startup
init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
