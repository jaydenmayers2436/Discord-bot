"""
Configuration settings for the Discord bot
"""

import os
from typing import Optional

class Config:
    """Bot configuration settings"""
    
    # Discord settings
    DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')
    
    # Groq API settings
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = 'llama3-70b-8192'  # As requested by user
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///affiliate_bot.db')
    
    # Affiliate settings
    AFFILIATE_DOMAIN = os.getenv('AFFILIATE_DOMAIN', 'your-domain.com')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # For click notifications
    
    # Bot settings
    MAX_EMBED_LENGTH = 2000
    CACHE_TTL = 3600  # 1 hour cache for AI responses
    
    # Click tracking
    CLICK_NOTIFICATION_CHANNEL = os.getenv('CLICK_NOTIFICATION_CHANNEL')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required = [cls.DISCORD_TOKEN, cls.GROQ_API_KEY]
        return all(required)
    
    @classmethod
    def get_missing_vars(cls) -> list:
        """Get list of missing required environment variables"""
        missing = []
        if not cls.DISCORD_TOKEN:
            missing.append('DISCORD_BOT_TOKEN')
        if not cls.GROQ_API_KEY:
            missing.append('GROQ_API_KEY')
        return missing
