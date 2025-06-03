#!/usr/bin/env python3
"""
Setup and Launch Script for Discord Affiliate Marketing Bot
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                             "discord.py>=2.3.2", "python-dotenv>=1.0.0", 
                             "aiosqlite>=0.19.0", "aiohttp>=3.9.0", 
                             "fastapi>=0.104.1", "uvicorn>=0.24.0"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Setup environment file"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from template...")
            env_file.write_text(env_example.read_text())
            print("✅ .env file created")
            print("🔑 Please edit .env file and add your API keys!")
            return False
        else:
            print("❌ .env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
        return True

def check_api_keys():
    """Check if required API keys are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = ["DISCORD_BOT_TOKEN", "GROQ_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print("\n🔑 How to get API keys:")
        print("1. Discord Bot Token:")
        print("   - Go to https://discord.com/developers/applications")
        print("   - Create a new application")
        print("   - Go to 'Bot' section and create a bot")
        print("   - Copy the token")
        print("\n2. Groq API Key:")
        print("   - Go to https://console.groq.com/")
        print("   - Sign up/login")
        print("   - Create an API key")
        print("\n📝 Add these to your .env file and run setup again")
        return False
    
    print("✅ All required API keys are set")
    return True

async def test_bot_functionality():
    """Test core bot functionality"""
    print("🧪 Testing bot functionality...")
    
    try:
        # Import and test core components
        from bot.core.database import Database
        from bot.services.groq_service import GroqService
        from bot.services.affiliate_service import AffiliateService
        
        # Test database
        db = Database(":memory:")
        await db.initialize()
        await db.close()
        print("✅ Database functionality working")
        
        # Test services
        groq_service = GroqService()
        print("✅ Groq service initialized")
        
        print("✅ All core functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Bot functionality test failed: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("🚀 Discord Affiliate Marketing Bot Setup Complete!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Invite your bot to Discord server:")
    print("   - Go to Discord Developer Portal")
    print("   - OAuth2 > URL Generator")
    print("   - Select 'bot' scope and 'Send Messages' permission")
    print("   - Use generated URL to invite bot")
    
    print("\n2. Start the bot:")
    print("   python3 discord_bot.py")
    
    print("\n3. Start click tracking server (optional):")
    print("   python3 click_server.py")
    
    print("\n🔧 Available Commands:")
    commands = [
        "!help - Show all commands",
        "!create <url> <title> | <description> | <category> - Create affiliate link",
        "!analyze <niche> - AI niche analysis",
        "!dashboard - View your performance",
        "!links - List your links"
    ]
    for cmd in commands:
        print(f"   {cmd}")
    
    print("\n💡 Example Usage:")
    print("   !create https://amzn.to/abc123 Gaming Mouse | Best wireless gaming mouse | Gaming")
    print("   !analyze fitness equipment")
    print("   !products $100-500 smart home devices")
    
    print("\n🎯 Features:")
    features = [
        "✅ Real-time click tracking and notifications",
        "✅ AI-powered niche analysis using Groq llama3-70b-8192",
        "✅ Comprehensive analytics and performance tracking",
        "✅ Easy affiliate link management",
        "✅ Product recommendations and trend analysis"
    ]
    for feature in features:
        print(f"   {feature}")

async def main():
    """Main setup function"""
    print("🤖 Discord Affiliate Marketing Bot Setup")
    print("="*50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    env_ready = setup_environment()
    
    if not env_ready:
        print("\n⚠️  Setup incomplete. Please configure .env file and run again.")
        return
    
    # Check API keys
    if not check_api_keys():
        print("\n⚠️  Setup incomplete. Please add API keys to .env file.")
        return
    
    # Test functionality
    test_success = await test_bot_functionality()
    
    if test_success:
        show_usage_instructions()
    else:
        print("\n❌ Setup failed. Please check error messages above.")

if __name__ == "__main__":
    asyncio.run(main())