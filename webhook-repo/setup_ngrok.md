# Setting Up ngrok for Real GitHub Webhooks

## Step 1: Download and Install ngrok
1. Go to https://ngrok.com/download
2. Download ngrok for Windows
3. Extract the executable to a folder (e.g., C:\ngrok\)

## Step 2: Get ngrok Auth Token
1. Sign up at https://ngrok.com
2. Go to https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy your auth token

## Step 3: Configure ngrok
Open PowerShell and run:
```bash
# Navigate to ngrok folder
cd C:\ngrok\

# Add your auth token (replace YOUR_TOKEN with actual token)
.\ngrok.exe authtoken YOUR_TOKEN
```

## Step 4: Start ngrok Tunnel
```bash
# Start tunnel to your Flask app (port 5000)
.\ngrok.exe http 5000
```

## Step 5: Copy the Public URL
You'll see output like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:5000
```

Use `https://abc123.ngrok.io/webhook` as your GitHub webhook URL.

## Step 6: Enable Signature Verification
Update your Flask app to verify real GitHub signatures.
