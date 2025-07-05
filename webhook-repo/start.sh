#!/bin/bash

# GitHub Webhook Monitor - Quick Start Script

echo "🚀 Starting GitHub Webhook Monitor..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if .env file exists and has DATABASE_URL
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create .env file with DATABASE_URL"
    echo "   Example: DATABASE_URL=postgresql://user:password@localhost:5432/webhook_db"
    exit 1
fi

# Check if DATABASE_URL is set
if ! grep -q "DATABASE_URL" .env; then
    echo "❌ DATABASE_URL not found in .env file"
    echo "   Please add: DATABASE_URL=postgresql://user:password@localhost:5432/webhook_db"
    exit 1
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

# Check if .env file has required variables
echo "⚙️  Checking environment configuration..."
if ! grep -q "GITHUB_WEBHOOK_SECRET" .env; then
    echo "⚠️  GITHUB_WEBHOOK_SECRET not found in .env file"
    echo "   Please add: GITHUB_WEBHOOK_SECRET=your-secret-key"
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

python app_postgres.py
