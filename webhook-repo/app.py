from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pymongo
from datetime import datetime
import hashlib
import hmac
import os
from bson import ObjectId
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = 'github_webhooks'
COLLECTION_NAME = 'events'

# GitHub webhook secret (set this in your environment)
WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', 'your-secret-key')

# MongoDB client with error handling
try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    # Test the connection
    client.admin.command('ping')
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}.{COLLECTION_NAME}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("⚠️  App will continue but data won't be saved")
    client = None
    db = None
    collection = None

def verify_signature(payload_body, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256 signature."""
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

def extract_event_data(payload, event_type):
    """Extract relevant data from GitHub webhook payload according to schema."""
    try:
        if event_type == 'push':
            # For push events, use commit hash as request_id
            request_id = payload['commits'][0]['id'] if payload['commits'] else payload['after']
            return {
                'request_id': request_id,
                'author': payload['pusher']['name'],
                'action': 'PUSH',
                'from_branch': None,
                'to_branch': payload['ref'].replace('refs/heads/', ''),
                'timestamp': datetime.utcnow()
            }

        elif event_type == 'pull_request':
            action = payload['action']
            request_id = str(payload['pull_request']['id'])

            if action in ['opened', 'synchronize']:
                return {
                    'request_id': request_id,
                    'author': payload['pull_request']['user']['login'],
                    'action': 'PULL_REQUEST',
                    'from_branch': payload['pull_request']['head']['ref'],
                    'to_branch': payload['pull_request']['base']['ref'],
                    'timestamp': datetime.utcnow()
                }
            elif action == 'closed' and payload['pull_request']['merged']:
                return {
                    'request_id': request_id,
                    'author': payload['pull_request']['merged_by']['login'] if payload['pull_request']['merged_by'] else payload['pull_request']['user']['login'],
                    'action': 'MERGE',
                    'from_branch': payload['pull_request']['head']['ref'],
                    'to_branch': payload['pull_request']['base']['ref'],
                    'timestamp': datetime.utcnow()
                }

        return None
    except KeyError as e:
        print(f"Error extracting event data: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events."""
    signature = request.headers.get('X-Hub-Signature-256')
    event_type = request.headers.get('X-GitHub-Event')

    print(f"🔔 Received webhook: {event_type}")
    print(f"📝 Headers: X-GitHub-Event={event_type}, X-Hub-Signature-256={'Present' if signature else 'Missing'}")
    print(f"🌐 Request from: {request.remote_addr}")
    print(f"📋 All headers: {dict(request.headers)}")

    # Force flush output
    import sys
    sys.stdout.flush()

    # Handle ping events (GitHub webhook test)
    if event_type == 'ping':
        payload = request.json
        repo_name = payload.get('repository', {}).get('full_name', 'Unknown')
        print(f"🏓 Ping event received from repository: {repo_name}")
        print("✅ Webhook connection successful!")
        return jsonify({
            'status': 'success',
            'message': 'Webhook ping received successfully',
            'repository': repo_name
        }), 200

    # Verify the signature for real GitHub webhooks
    if not verify_signature(request.data, signature):
        print("❌ Signature verification failed!")
        return jsonify({'error': 'Invalid signature'}), 401

    payload = request.json

    # Extract event data
    event_data = extract_event_data(payload, event_type)

    if event_data:
        # Store in MongoDB if connected
        if collection is not None:
            try:
                result = collection.insert_one(event_data)
                print(f"💾 Stored event: {event_data['action']} by {event_data['author']}")
                return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 200
            except Exception as e:
                print(f"❌ Failed to store in MongoDB: {e}")
                return jsonify({'status': 'error', 'message': 'Database error'}), 500
        else:
            print(f"⚠️  MongoDB not connected - event not stored: {event_data['action']} by {event_data['author']}")
            return jsonify({'status': 'success', 'message': 'Event received but not stored (DB offline)'}), 200

    print(f"⚠️  Event type '{event_type}' ignored or not supported")
    return jsonify({'status': 'ignored'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    """Get recent events from MongoDB."""
    if collection is None:
        return jsonify({'error': 'Database not connected'}), 500

    try:
        # Get the latest 50 events, sorted by timestamp descending
        events = list(collection.find().sort('timestamp', -1).limit(50))
        
        # Convert ObjectId to string for JSON serialization
        for event in events:
            event['_id'] = str(event['_id'])
            # Handle both datetime objects and string timestamps
            if hasattr(event['timestamp'], 'isoformat'):
                event['timestamp'] = event['timestamp'].isoformat()
            # If it's already a string, keep it as is
        
        return jsonify(events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve the main UI."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({'status': 'healthy', 'mongodb': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    # Create indexes for better performance
    collection.create_index([('timestamp', -1)])
    collection.create_index('action')

    # Use PORT environment variable for deployment platforms
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'

    app.run(debug=debug, host='0.0.0.0', port=port)
