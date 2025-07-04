#!/bin/bash

# GitHub Webhook Monitor - Quick Start Script

echo "🚀 Starting GitHub Webhook Monitor..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Starting MongoDB..."
    if command -v mongod &> /dev/null; then
        mongod --fork --logpath /tmp/mongodb.log
        sleep 2
    else
        echo "❌ MongoDB is not installed. Please install MongoDB or use Docker:"
        echo "   docker run -d -p 27017:27017 --name mongodb mongo:7.0"
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating environment configuration..."
    cp .env.example .env
    echo "✏️  Please edit .env file with your webhook secret before proceeding."
    echo "   Default secret is 'your-secret-key' for testing."
fi

# Start the Flask application
echo "🌟 Starting Flask application..."
echo "   Dashboard: http://localhost:5000"
echo "   Webhook endpoint: http://localhost:5000/webhook"
echo "   Health check: http://localhost:5000/health"
echo ""
echo "💡 To test webhooks locally, use ngrok:"
echo "   ngrok http 5000"
echo ""
echo "🧪 To run tests:"
echo "   python test_webhook.py"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

python app.py
