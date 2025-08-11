#!/usr/bin/env python3
"""
Discord User Remover Bot - Runner Script
Simple script to start the Streamlit application
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import discord
        import pandas
        import openpyxl
        from dotenv import load_dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("Please create a .env file with your Discord bot token and server ID")
        print("See config_template.txt for the format")
        return False

def main():
    """Main function to run the application"""
    print("🤖 Discord User Remover Bot")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check env file
    check_env_file()
    
    # Start Streamlit
    print("\n🚀 Starting Streamlit application...")
    print("The application will open in your browser automatically")
    print("If it doesn't open, navigate to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the application")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main() 