# 🚀 Action Repository

A sample Node.js Express application designed to trigger GitHub webhooks for testing the **GitHub Webhook Monitor** system.

![Node.js](https://img.shields.io/badge/Node.js-16+-green)
![Express](https://img.shields.io/badge/Express-4.18+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Purpose

This repository serves as the **source repository** for GitHub webhook events that will be captured and displayed by the [webhook-repo](../webhook-repo) Flask application. It demonstrates:

- **Push events** when code is committed to any branch
- **Pull request events** when PRs are created, updated, or closed
- **Merge events** when PRs are merged into target branches
- **Real-time monitoring** of repository activities

## 🏗️ Architecture

```
┌─────────────────┐    GitHub Webhooks    ┌──────────────────┐
│   action-repo   │ ──────────────────────▶│   webhook-repo   │
│  (This Repo)    │                        │  (Flask Monitor) │
│                 │                        │                  │
│ • Express API   │                        │ • Webhook Handler│
│ • Sample Data   │                        │ • PostgreSQL DB  │
│ • Trigger Events│                        │ • Web Dashboard  │
└─────────────────┘                        └──────────────────┘
```

## 📋 Quick Start

### 1. Local Development Setup

```bash
# Clone the repository
git clone <your-repository-url>
cd action-repo

# Install dependencies
npm install

# Start the development server
npm start
```

The API will be available at `http://localhost:3000`

### 2. GitHub Repository Setup

1. **Create GitHub Repository**
   ```bash
   # Create a new repository on GitHub named 'action-repo'
   # Push this code to your GitHub repository
   git remote add origin https://github.com/YOUR_USERNAME/action-repo.git
   git branch -M main
   git push -u origin main
   ```

2. **Configure Webhooks**
   - Go to your repository **Settings** → **Webhooks**
   - Click **"Add webhook"**
   - Configure the webhook:
     - **Payload URL**: `https://your-tunnel-url.loca.lt/webhook`
     - **Content type**: `application/json`
     - **Secret**: `gh_webhook_2024_$ecur3_K3y_#789_XyZ` (or your custom secret)
     - **Events**: Select **"Send me everything"** or choose:
       - ✅ Pushes
       - ✅ Pull requests
       - ✅ Issues
       - ✅ Releases
     - **Active**: ✅ Checked

### 3. Test Webhook Integration

After setting up the webhook, test the integration:

1. **Push Events**: Make changes and push to any branch
2. **Pull Request Events**: Create a branch, make changes, and open a PR
3. **Merge Events**: Merge the pull request
4. **Monitor**: Check the webhook-repo dashboard for real-time events

## 🔄 Sample Workflow for Testing

### Basic Testing Workflow

```bash
# 1. Create a new feature branch
git checkout -b feature/add-new-endpoint

# 2. Make meaningful changes (don't overwrite the entire app.js!)
# Add a new endpoint to app.js
echo "
// New test endpoint
app.get('/api/test', (req, res) => {
    res.json({
        success: true,
        message: 'Test endpoint working!',
        timestamp: new Date().toISOString()
    });
});" >> app.js

# 3. Commit your changes
git add .
git commit -m "Add test endpoint for webhook testing"

# 4. Push the branch (triggers push webhook)
git push origin feature/add-new-endpoint

# 5. Create a pull request on GitHub (triggers PR webhook)
# 6. Merge the pull request (triggers merge webhook)
```

### Advanced Testing Scenarios

```bash
# Test multiple commits
git checkout -b feature/multiple-commits
echo "// Comment 1" >> src/utils.js
git add . && git commit -m "Add comment 1"
echo "// Comment 2" >> src/utils.js
git add . && git commit -m "Add comment 2"
git push origin feature/multiple-commits

# Test issue creation (if webhook configured for issues)
# Create issues through GitHub UI

# Test releases (if webhook configured for releases)
git tag v1.1.0
git push origin v1.1.0
```

## 📁 Repository Structure

```
action-repo/
├── 📄 README.md              # This documentation
├── 📄 CONTRIBUTING.md        # Contribution guidelines
├── 📄 LICENSE                # MIT License
├── 📄 package.json           # Node.js dependencies and scripts
├── 📄 .gitignore             # Git ignore rules
├── 🚀 app.js                 # Main Express.js application
└── 📁 src/
    └── 🔧 utils.js           # Utility functions
```

### File Descriptions

- **`app.js`** - Express.js REST API with user management endpoints and request logging
- **`package.json`** - Node.js project configuration, dependencies, and useful scripts
- **`src/utils.js`** - Utility functions for date formatting, validation, and more
- **`README.md`** - Comprehensive project documentation
- **`CONTRIBUTING.md`** - Guidelines for contributing to the project
- **`LICENSE`** - MIT License for the project
- **`.gitignore`** - Git ignore rules for Node.js projects

## 🎯 API Endpoints

The Express application provides the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message and API information |
| `GET` | `/version` | Application version and system info |
| `GET` | `/api/users` | List all users |
| `GET` | `/api/users/:id` | Get specific user by ID |
| `POST` | `/api/users` | Create new user |
| `GET` | `/health` | Health check endpoint |

### Example API Usage

```bash
# Test the API locally
curl http://localhost:3000/health
curl http://localhost:3000/version
curl http://localhost:3000/api/users
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'
```

## 📡 Webhook Events Generated

This repository will generate the following webhook events when connected to GitHub:

### 🔄 Push Events
- **Triggered**: When commits are pushed to any branch
- **Use Case**: Monitor code changes and deployments
- **Dashboard Format**: `"{author} pushed to {branch} on {timestamp}"`

### 🔀 Pull Request Events
- **Triggered**: When PRs are opened, updated, or closed
- **Use Case**: Track code review process
- **Dashboard Format**: `"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"`

### 🎯 Merge Events
- **Triggered**: When PRs are merged into target branches
- **Use Case**: Monitor successful code integrations
- **Dashboard Format**: `"{author} merged branch {from_branch} to {to_branch} on {timestamp}"`

### 🐛 Issue Events (Optional)
- **Triggered**: When issues are created, updated, or closed
- **Use Case**: Track bug reports and feature requests

### 🏷️ Release Events (Optional)
- **Triggered**: When releases/tags are created
- **Use Case**: Monitor version releases

## 📊 Real-time Monitoring

All webhook events from this repository are captured and displayed in the **webhook-repo dashboard**:

- **URL**: `https://your-tunnel-url.loca.lt/` (or your deployed URL)
- **Auto-refresh**: Updates every 15 seconds (as per assessment requirements)
- **Event History**: Shows recent webhook events with details
- **Request Tracking**: Each event includes a unique request ID
- **Database**: PostgreSQL for reliable data storage

### Dashboard Features
- ✅ Real-time event display
- ✅ Event type identification (PUSH, PULL_REQUEST, MERGE)
- ✅ Author and timestamp information
- ✅ Branch information for relevant events
- ✅ Request ID for debugging

## 🛠️ Development

### Prerequisites

- **Node.js 16+** and npm
- **Git** for version control
- **GitHub account** for webhook testing

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm start

# The API will be available at http://localhost:3000
```

### Available Scripts

```bash
npm start       # Start the production server
npm run dev     # Start development server (same as start)
npm test        # Run tests (currently placeholder)
```

### Making Changes

1. **Always create a feature branch** for your changes
2. **Test your changes locally** before pushing
3. **Follow the existing code style** and patterns
4. **Update documentation** if needed
5. **Test webhook integration** after pushing

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# If port 3000 is busy, use a different port
PORT=3001 npm start
```

#### Dependencies Issues
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### Webhook Not Triggering
1. Check if webhook URL is correct in GitHub settings
2. Verify webhook-repo Flask app is running
3. Ensure tunnel (localtunnel) is active
4. Check webhook secret matches between repos

### Debug Commands

```bash
# Test API health
curl http://localhost:3000/health

# Test webhook endpoint (if webhook-repo is running)
curl https://your-tunnel.loca.lt/health

# Check webhook deliveries in GitHub
# Go to Settings → Webhooks → Recent Deliveries
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test them
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[webhook-repo](../webhook-repo)** - Flask application that receives and displays webhook events
- **GitHub Webhooks Documentation** - [Official GitHub Docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks)

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [webhook-repo documentation](../webhook-repo/README.md)
3. Search existing issues in the repository
4. Create a new issue with detailed information

## 🎉 Acknowledgments

- **Express.js** for the web framework
- **GitHub** for webhook functionality
- **Node.js** community for excellent tooling

---

**Happy webhook testing! 🚀**
