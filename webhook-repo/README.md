# 🔗 GitHub Webhook Assessment - webhook-repo

A Flask application that receives GitHub webhooks and displays them in a web dashboard. This is the **webhook-repo** component of the GitHub webhook assessment task.

![Assessment](https://img.shields.io/badge/Assessment-Task-orange)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue)
![Deployment](https://img.shields.io/badge/Status-Live%20on%20Render-brightgreen)
[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-github--webhook--dashboard.onrender.com-blue)](https://github-webhook-dashboard.onrender.com/)

## 🛠️ **Technologies Used**

For this GitHub webhook assessment, I used **Python Flask** as the main web framework to handle webhook endpoints and serve the dashboard. **PostgreSQL** was chosen as the database instead of MongoDB because it offers seamless integration with Render deployment platform, making production deployment much easier. The frontend uses **HTML5, CSS3, and vanilla JavaScript** for a clean, minimal UI with 15-second polling intervals. The project follows a **two-repository architecture** with action-repo (Node.js Express) for triggering webhooks and webhook-repo (Flask) containing the main application and UI. **Git/GitHub** handles version control, while **Render** provides reliable cloud hosting with PostgreSQL support.

## 🎯 Assessment Requirements

This project implements the GitHub webhook assessment with the following specifications:

- **Event Types**: PUSH, PULL_REQUEST, MERGE actions
- **Message Formats**: Exact formats as specified in assessment
- **Database**: PostgreSQL with assessment-specified schema
- **UI Polling**: 15-second intervals for real-time updates
- **Repository Structure**: Two-repo setup (action-repo + webhook-repo)

## ✅ Assessment Compliance Checklist

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| **Two Repository Structure** | ✅ Complete | `action-repo/` (Node.js) + `webhook-repo/` (Flask) |
| **GitHub Webhooks Integration** | ✅ Complete | `/webhook` endpoint with signature verification |
| **PUSH Event Handling** | ✅ Complete | `app_postgres.py` lines 150-170 |
| **PULL_REQUEST Event Handling** | ✅ Complete | `app_postgres.py` lines 171-190 |
| **MERGE Event Handling** | ✅ Complete | `app_postgres.py` lines 191-210 |
| **Exact Message Formats** | ✅ Complete | `templates/index.html` lines 214-224 |
| **PostgreSQL Storage** | ✅ Complete | Schema in `app_postgres.py` lines 53-64 |
| **15-Second UI Polling** | ✅ Complete | `templates/index.html` line 282 |
| **Flask Implementation** | ✅ Complete | `app_postgres.py` main application |
| **Live Deployment** | ✅ **BONUS** | [Live Demo](https://github-webhook-dashboard.onrender.com/) |
| **Clean Professional Code** | ✅ **BONUS** | Production-ready implementation |
| **Professional Documentation** | ✅ **BONUS** | Detailed READMEs with setup guides |

## 🎯 Assessment Submission

This project is **ready for submission** with the following deliverables:

### Repository Links
- **action-repo**: [GitHub Repository URL] - Node.js Express application for triggering webhooks
- **webhook-repo**: [GitHub Repository URL] - Flask application for receiving and displaying webhooks

### Live Demo
- **Deployed Application**: https://github-webhook-dashboard.onrender.com/
- **Status**: ✅ Live and functional
- **Database**: PostgreSQL (production-ready)

### Assessment Compliance
✅ **All requirements met** - See compliance checklist above
✅ **Bonus features implemented** - Live deployment, professional UI, comprehensive documentation
✅ **Production-ready code** - Error handling, logging, monitoring endpoints

## 📋 Message Formats (Assessment Specification)

### PUSH Action
**Format**: `"{author}" pushed to "{to_branch}" on {timestamp}`
**Sample**: `"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC`

### PULL_REQUEST Action
**Format**: `"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}`
**Sample**: `"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC`

### MERGE Action (Brownie Points)
**Format**: `"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}`
**Sample**: `"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC`

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
- **PostgreSQL 12+** (local installation or cloud service)
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

Create a `.env` file in the project root with these settings:

```env
# PostgreSQL Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/webhook_db

# GitHub Webhook Secret (set this to match your GitHub webhook configuration)
GITHUB_WEBHOOK_SECRET=gh_webhook_2024_$ecur3_K3y_#789_XyZ

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

**Important**:
- Replace `username`, `password`, and `webhook_db` with your actual PostgreSQL credentials and database name
- You can modify the `GITHUB_WEBHOOK_SECRET` if needed, but make sure it matches what you set in GitHub webhook settings

### 2. PostgreSQL Setup

#### Option A: Local PostgreSQL
1. Install PostgreSQL 12+ from [postgresql.org](https://www.postgresql.org/download/)
2. Start PostgreSQL service:
   ```bash
   # Windows
   net start postgresql-x64-12

   # macOS
   brew services start postgresql

   # Linux
   sudo systemctl start postgresql
   ```
3. Create database and user:
   ```sql
   CREATE DATABASE webhook_db;
   CREATE USER webhook_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE webhook_db TO webhook_user;
   ```

#### Option B: Cloud PostgreSQL
1. Use services like **Heroku Postgres**, **AWS RDS**, **Google Cloud SQL**, or **DigitalOcean**
2. Get the connection string
3. Update `DATABASE_URL` in `.env` file

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

#### Step 1: Start PostgreSQL

Ensure PostgreSQL is running and test connection:

```bash
# Check PostgreSQL connection
python -c "import psycopg2; import os; from dotenv import load_dotenv; load_dotenv(); conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('PostgreSQL: Connected'); conn.close()"
```

#### Step 2: Start Flask Application

```bash
python app_postgres.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * PostgreSQL connected successfully
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
Returns application and PostgreSQL connection status

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

#### 2. PostgreSQL Connection Issues

**Symptoms**: "PostgreSQL connection failed" error
**Solutions**:
- Check PostgreSQL service: `sudo systemctl status postgresql`
- Verify DATABASE_URL in `.env` file
- For cloud services: Check network access and credentials
- Ensure database exists and user has proper permissions

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

# Test PostgreSQL connection
python -c "import psycopg2; import os; from dotenv import load_dotenv; load_dotenv(); conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('PostgreSQL: Connected'); conn.close()"
```

### Logs and Monitoring

- **Flask logs**: Check terminal running `app_postgres.py`
- **Tunnel logs**: Check terminal running localtunnel
- **PostgreSQL logs**: Check PostgreSQL service logs
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

## 📊 Database Schema (Assessment Specification)

Events are stored in PostgreSQL with the following table structure matching the assessment requirements:

```sql
CREATE TABLE webhook_events (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    from_branch VARCHAR(255),
    to_branch VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_payload JSONB
);
```

**Column Descriptions (Assessment Schema):**
- `id`: Auto-incrementing primary key
- `request_id`: Git commit hash (for PUSH) or PR ID (for PULL_REQUEST/MERGE)
- `author`: Name of the GitHub user making the action
- `action`: GitHub action enum ("PUSH", "PULL_REQUEST", "MERGE")
- `from_branch`: Git branch in LHS (source branch for PRs)
- `to_branch`: Git branch in RHS (target branch for pushes/PRs)
- `timestamp`: Datetime formatted string (UTC) for the time of action
- `raw_payload`: Complete GitHub webhook payload as JSON

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 🧪 Testing the Webhook Integration

### Method 1: Using the Live Demo
1. **Fork the action-repo** to your GitHub account
2. **Configure webhook** in your forked repository:
   - Go to Settings → Webhooks → Add webhook
   - Payload URL: `https://github-webhook-dashboard.onrender.com/webhook`
   - Content type: `application/json`
   - Events: Select "Pushes" and "Pull requests"
3. **Test events**:
   - Make a commit and push to trigger PUSH events
   - Create a pull request to trigger PULL_REQUEST events
   - Merge the pull request to trigger MERGE events
4. **Monitor results** at: https://github-webhook-dashboard.onrender.com/

### Method 2: Local Testing
1. **Run the Flask app locally** (see Local Development section)
2. **Use ngrok or localtunnel** to expose your local server:
   ```bash
   # Using ngrok
   ngrok http 5000

   # Using localtunnel
   npx localtunnel --port 5000
   ```
3. **Configure webhook** with your tunnel URL + `/webhook`
4. **Test with real GitHub events**

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Flask framework for the web application
- PostgreSQL for reliable data storage
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
