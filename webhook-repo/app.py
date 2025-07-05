#!/usr/bin/env python3
"""
GitHub Webhook Dashboard - Main Entry Point
This is the main entry point for the Flask application.
It imports and runs the PostgreSQL version of the webhook dashboard.
"""

from app_postgres import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
