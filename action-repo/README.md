# Action Repository

This repository is designed to trigger GitHub webhooks for testing the webhook monitoring system.

## Purpose

This repository serves as the source for GitHub webhook events that will be captured by the webhook-repo Flask application. It demonstrates:

- Push events when code is committed
- Pull request events when PRs are created
- Merge events when PRs are merged

## Setup Instructions

### 1. Create GitHub Repository

1. Create a new repository on GitHub named `action-repo`
2. Clone this repository to your local machine
3. Push the initial code to GitHub

### 2. Configure Webhooks

1. Go to your repository Settings → Webhooks
2. Click "Add webhook"
3. Configure the webhook:
   - **Payload URL**: `https://your-webhook-endpoint.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: Your webhook secret (same as in webhook-repo)
   - **Events**: Select "Let me select individual events"
     - ✅ Pushes
     - ✅ Pull requests
   - **Active**: ✅ Checked

### 3. Test the Webhook

After setting up the webhook, you can test it by:

1. **Push Events**: Make changes to files and push to any branch
2. **Pull Request Events**: Create a new branch, make changes, and open a PR
3. **Merge Events**: Merge the pull request

## Sample Workflow

```bash
# Create a new feature branch
git checkout -b feature/new-feature

# Make some changes
echo "console.log('Hello, World!');" > app.js
git add app.js
git commit -m "Add hello world script"

# Push the branch
git push origin feature/new-feature

# Create a pull request on GitHub
# Then merge the pull request
```

## Files in this Repository

- `README.md` - This documentation
- `app.js` - Sample JavaScript application
- `package.json` - Node.js package configuration
- `src/` - Source code directory
- `.gitignore` - Git ignore rules

## Webhook Events Generated

This repository will generate the following webhook events:

### Push Event
Triggered when commits are pushed to any branch.

### Pull Request Event  
Triggered when:
- A new pull request is opened
- Commits are added to an existing pull request

### Merge Event
Triggered when a pull request is merged into the target branch.

## Monitoring

All webhook events from this repository will be captured and displayed in the webhook-repo dashboard at:
`https://your-webhook-endpoint.com/`

The dashboard updates every 15 seconds and shows events in the format:
- **Push**: "{author} pushed to {branch} on {timestamp}"
- **Pull Request**: "{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
- **Merge**: "{author} merged branch {from_branch} to {to_branch} on {timestamp}"
