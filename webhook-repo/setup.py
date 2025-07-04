#!/usr/bin/env python3
"""
Quick setup script for GitHub Webhook Monitor
This script helps you get started quickly by checking prerequisites and guiding setup.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.7+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required. Current version:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True

def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Please start MongoDB or check your connection")
        return False

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    print("❌ Node.js not found. Please install Node.js for localtunnel")
    return False

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_localtunnel():
    """Install localtunnel globally"""
    try:
        print("🌐 Installing localtunnel...")
        subprocess.run(['npm', 'install', '-g', 'localtunnel'], check=True)
        print("✅ Localtunnel installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install localtunnel: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_path = Path('.env')
    if env_path.exists():
        print("✅ .env file found")
        return True
    else:
        print("❌ .env file not found")
        return False

def main():
    """Main setup function"""
    print("🔗 GitHub Webhook Monitor Setup")
    print("=" * 40)
    
    # Check prerequisites
    checks = [
        ("Python 3.7+", check_python_version),
        ("MongoDB", check_mongodb),
        ("Node.js", check_node),
        (".env file", check_env_file)
    ]
    
    all_good = True
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if not check_func():
            all_good = False
    
    if not all_good:
        print("\n❌ Some prerequisites are missing. Please fix them before continuing.")
        print("\n📖 See README.md for detailed setup instructions.")
        return False
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        return False
    
    if check_node():
        install_localtunnel()
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Start MongoDB (if not already running)")
    print("2. Run: python app.py")
    print("3. In another terminal: npx localtunnel --port 5000")
    print("4. Configure GitHub webhook with the tunnel URL")
    print("5. Visit http://localhost:5000 to see the dashboard")
    
    return True

if __name__ == "__main__":
    main()
