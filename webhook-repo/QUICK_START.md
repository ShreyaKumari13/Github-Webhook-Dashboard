# ⚡ Quick Start Guide

Get your GitHub Webhook Monitor running in **5 minutes**!

## 🎯 Prerequisites

- Python 3.7+
- PostgreSQL running locally
- Node.js (for tunneling)

## 🚀 Super Quick Setup

### 1. Run the Setup Script

```bash
python setup.py
```

### 2. Start the Application

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh && ./start.sh
```

### 3. Start Tunnel

In a **new terminal**:
```bash
npx localtunnel --port 5000 --subdomain your-name-here
```

Copy the tunnel URL (e.g., `https://your-name-here.loca.lt`)

### 4. Configure GitHub Webhook

1. Go to your GitHub repo → **Settings** → **Webhooks**
2. Click **Add webhook**
3. **Payload URL**: `https://your-name-here.loca.lt/webhook`
4. **Content type**: `application/json`
5. **Secret**: `gh_webhook_2024_$ecur3_K3y_#789_XyZ` (from .env file)
6. **Events**: Select "Send me everything"
7. Click **Add webhook**

### 5. Test It!

1. Visit `http://localhost:5000` to see your dashboard
2. Make a commit to your repo
3. Watch events appear in real-time! 🎉

## 🐛 Quick Troubleshooting

**Red triangles in GitHub?**
- Restart tunnel: `npx localtunnel --port 5000`

**No events showing?**
- Check Flask is running: `curl http://localhost:5000/health`
- Check PostgreSQL: `python -c "import psycopg2; import os; from dotenv import load_dotenv; load_dotenv(); conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('PostgreSQL: Connected'); conn.close()"`

**Need help?** See the full [README.md](README.md) for detailed troubleshooting.

---

**That's it! Your webhook monitor is now live! 🚀**
