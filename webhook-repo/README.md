# 🔗 GitHub Webhook Monitor

A real-time monitoring system for GitHub repository events using webhooks. Monitor pushes, pull requests, merges, and other repository activities in real-time with a clean web interface.

![Webhook Monitor](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![MongoDB](https://img.shields.io/badge/MongoDB-4.0+-green)

## 🌟 Features

- **Real-time monitoring** of GitHub repository events
- **Clean web interface** with 15-second auto-refresh
- **MongoDB storage** for event persistence
- **Webhook security** with signature verification
- **Multiple event types** support (push, pull_request, merge, etc.)
- **Request tracking** with unique IDs
- **Responsive design** for desktop and mobile

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Setting up GitHub Webhook](#setting-up-github-webhook)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **MongoDB** (local installation or MongoDB Atlas)
- **Node.js** (for localtunnel)
- **Git**

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB
- **Storage**: 100MB free space
- **Network**: Internet connection for webhook delivery

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd webhook-repo
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv webhook_env

# Activate virtual environment
# On Windows:
webhook_env\Scripts\activate
# On macOS/Linux:
source webhook_env/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies (for tunneling)

```bash
npm install -g localtunnel
```

## ⚙️ Configuration

### 1. Environment Variables

The `.env` file is already included in the project with these settings:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/github_webhooks

# GitHub Webhook Secret (set this to match your GitHub webhook configuration)
GITHUB_WEBHOOK_SECRET=gh_webhook_2024_$ecur3_K3y_#789_XyZ

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

**Important**: You can modify the `GITHUB_WEBHOOK_SECRET` if needed, but make sure it matches what you set in GitHub webhook settings.

### 2. MongoDB Setup

#### Option A: Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB

   # macOS
   brew services start mongodb-community

   # Linux
   sudo systemctl start mongod
   ```

#### Option B: MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a cluster
3. Get connection string
4. Update `MONGODB_URI` in `.env` file

### 3. GitHub Repository Setup

1. Go to your GitHub repository
2. Navigate to **Settings** → **Webhooks**
3. Click **Add webhook**
4. You'll configure the URL after starting the tunnel (next section)

## 🚀 Running the Application

### Quick Start (Recommended)

Use the provided start scripts for the easiest setup:

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Python Setup Script:**
```bash
python setup.py
```

### Manual Setup

#### Step 1: Start MongoDB

Ensure MongoDB is running:

```bash
# Check MongoDB status
python -c "from pymongo import MongoClient; print('MongoDB:', 'Connected' if MongoClient().admin.command('ping') else 'Failed')"
```

#### Step 2: Start Flask Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * MongoDB connected successfully
 * Webhook endpoint ready at /webhook
```

#### Step 3: Start Tunnel (for GitHub webhook delivery)

In a **new terminal window**:

```bash
# Option 1: With custom subdomain (recommended)
npx localtunnel --port 5000 --subdomain your-custom-name

# Option 2: Random subdomain
npx localtunnel --port 5000
```

Note the tunnel URL (e.g., `https://your-custom-name.loca.lt`)

#### Step 4: Access the Dashboard

Once Flask is running, access the dashboard at: `http://localhost:5000`

The web interface will show:
- Real-time GitHub webhook events
- Event details (type, author, timestamp, request ID)
- Auto-refresh every 15 seconds

## 🔗 Setting up GitHub Webhook

### 1. Configure Webhook in GitHub

1. Go to your repository → **Settings** → **Webhooks**
2. Click **Add webhook**
3. Fill in the details:
   - **Payload URL**: `https://your-tunnel-url.loca.lt/webhook`
   - **Content type**: `application/json`
   - **Secret**: Use the same secret from your `.env` file
   - **Events**: Select "Send me everything" or choose specific events

### 2. Test Webhook

1. Click **Add webhook**
2. GitHub will send a test ping
3. Check the "Recent Deliveries" section for green checkmarks
4. Visit your dashboard to see the ping event

## 📱 Usage

### Dashboard Features

- **Real-time Events**: See repository events as they happen
- **Event Details**: View event type, timestamp, and request ID
- **Auto-refresh**: Updates every 15 seconds automatically
- **Event History**: Scroll through past events

### Supported Event Types

- `push` - Code pushes to repository
- `pull_request` - Pull request actions
- `merge` - Branch merges
- `issues` - Issue creation/updates
- `release` - Release creation
- `fork` - Repository forks
- And many more GitHub events

## 🔌 API Endpoints

### Main Dashboard
```
GET /
```
Serves the main web interface with real-time event monitoring

### Webhook Endpoint
```
POST /webhook
```
Receives GitHub webhook payloads with signature verification

### Health Check
```
GET /health
```
Returns application and MongoDB connection status

### Events API
```
GET /events
```
Returns the latest 50 webhook events in JSON format

**Example Response:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "event_type": "PUSH",
    "author": "ShreyaKumari13",
    "to_branch": "main",
    "from_branch": null,
    "timestamp": "2025-07-04T10:30:00Z",
    "repository": "ShreyaKumari13/Book-Review",
    "action": "push",
    "request_id": "abc123def456"
  }
]
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Webhook Delivery Failures (Red triangles in GitHub)

**Symptoms**: Red triangles in GitHub webhook deliveries
**Solutions**:
- Check if tunnel is still running: `curl https://your-tunnel.loca.lt/health`
- Restart tunnel: `npx localtunnel --port 5000`
- Verify Flask app is running on port 5000

#### 2. MongoDB Connection Issues

**Symptoms**: "MongoDB connection failed" error
**Solutions**:
- Check MongoDB service: `sudo systemctl status mongod`
- Verify connection string in `.env`
- For Atlas: Check network access and credentials

#### 3. Signature Verification Errors

**Symptoms**: "Invalid signature" in logs
**Solutions**:
- Ensure webhook secret matches in GitHub and `.env`
- Check that secret is properly set in both places
- Verify payload is being received correctly

#### 4. Frontend Not Loading

**Symptoms**: Dashboard shows blank page
**Solutions**:
- Check if frontend server is running on port 3000
- Verify Flask API is accessible at `http://localhost:5000/api/events`
- Check browser console for JavaScript errors

### Debug Commands

```bash
# Test Flask health
curl http://localhost:5000/health

# Test tunnel connectivity
curl https://your-tunnel.loca.lt/health

# Check recent events
curl http://localhost:5000/events

# Test MongoDB connection
python -c "from pymongo import MongoClient; print(MongoClient().list_database_names())"
```

### Logs and Monitoring

- **Flask logs**: Check terminal running `app.py`
- **Tunnel logs**: Check terminal running localtunnel
- **MongoDB logs**: Check MongoDB service logs
- **Browser console**: F12 → Console for frontend issues

## 🔒 Security Considerations

1. **Webhook Secret**: The project uses a strong webhook secret for signature verification
2. **Signature Verification**: All webhook payloads are verified using HMAC-SHA256
3. **Environment Variables**: Sensitive data is stored in `.env` file
4. **Input Validation**: Webhook payloads are validated before processing
5. **CORS**: Cross-Origin Resource Sharing is properly configured

## 🚀 Production Deployment

For production deployment:

1. **Use a proper domain** instead of localtunnel
2. **Set up SSL certificates** for HTTPS
3. **Use environment variables** for all configuration
4. **Set up monitoring** and logging
5. **Use a production WSGI server** like Gunicorn
6. **Set up database backups**

Example production command:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 Database Schema

Events are stored in MongoDB with the following structure:

```json
{
  "_id": "ObjectId",
  "event_type": "PUSH|PULL_REQUEST|MERGE",
  "author": "string",
  "to_branch": "string",
  "from_branch": "string|null",
  "timestamp": "ISODate",
  "repository": "string",
  "action": "string",
  "request_id": "string"
}
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework for the web application
- MongoDB for data storage
- Localtunnel for webhook testing
- GitHub for webhook functionality

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing issues in the repository
3. Create a new issue with detailed information
4. Include logs and error messages

---

**Happy monitoring! 🎉**
