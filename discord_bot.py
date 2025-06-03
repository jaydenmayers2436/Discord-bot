#!/usr/bin/env python3
"""
Discord Affiliate Marketing Bot with Groq AI Integration
Features: Click tracking, niche optimization, affiliate link management
"""

import discord
from discord.ext import commands
import asyncio
import logging
import os
from dotenv import load_dotenv

# Import bot modules
from bot.core.bot_client import AffiliateBot
from bot.core.database import Database
from bot.services.groq_service import GroqService
from bot.services.affiliate_service import AffiliateService
from bot.utils.config import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point for the Discord bot"""
    
    # Check for required environment variables
    required_vars = ['DISCORD_BOT_TOKEN', 'GROQ_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("\n🔑 Required Environment Variables:")
        print("   DISCORD_BOT_TOKEN - Your Discord bot token")
        print("   GROQ_API_KEY - Your Groq API key")
        print("\n📁 Create a .env file with these variables")
        return
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        db = Database()
        await db.initialize()
        
        # Initialize services
        groq_service = GroqService()
        affiliate_service = AffiliateService(db)
        
        # Create bot instance
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        bot = AffiliateBot(
            command_prefix='!',
            intents=intents,
            database=db,
            groq_service=groq_service,
            affiliate_service=affiliate_service
        )
        
        # Start the bot
        logger.info("🤖 Starting Discord Affiliate Marketing Bot...")
        await bot.start(os.getenv('DISCORD_BOT_TOKEN'))
        
    except discord.LoginFailure:
        logger.error("Invalid Discord bot token")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        if 'db' in locals():
            await db.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
