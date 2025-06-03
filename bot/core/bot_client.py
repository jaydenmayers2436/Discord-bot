"""
Main Discord Bot Client
"""

import discord
from discord.ext import commands
import asyncio
import logging
from typing import Optional

from bot.commands.affiliate_commands import AffiliateCommands
from bot.commands.ai_commands import AICommands
from bot.commands.analytics_commands import AnalyticsCommands
from bot.commands.help_commands import HelpCommands
from bot.core.database import Database
from bot.services.groq_service import GroqService
from bot.services.affiliate_service import AffiliateService

logger = logging.getLogger(__name__)

class AffiliateBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents,
                 database: Database, groq_service: GroqService, 
                 affiliate_service: AffiliateService):
        super().__init__(command_prefix=command_prefix, intents=intents)
        
        self.database = database
        self.groq_service = groq_service
        self.affiliate_service = affiliate_service
        
        # Add command groups
        self.add_cog(AffiliateCommands(self))
        self.add_cog(AICommands(self))
        self.add_cog(AnalyticsCommands(self))
        
        logger.info("✅ Bot client initialized with all command groups")
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'🤖 Bot logged in as {self.user.name} (ID: {self.user.id})')
        logger.info(f'📊 Connected to {len(self.guilds)} guilds')
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="affiliate links 💰 | !help"
        )
        await self.change_presence(activity=activity)
        
        print("\n" + "="*50)
        print("🚀 DISCORD AFFILIATE MARKETING BOT READY!")
        print("="*50)
        print(f"Bot Name: {self.user.name}")
        print(f"Bot ID: {self.user.id}")
        print(f"Guilds: {len(self.guilds)}")
        print(f"Commands: {len(self.commands)}")
        print("\n📋 Available Commands:")
        for command in self.commands:
            print(f"   !{command.name} - {command.brief or 'No description'}")
        print("="*50)
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Unknown command. Use `!help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param.name}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"❌ Invalid argument provided: {error}")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏰ Command on cooldown. Try again in {error.retry_after:.1f} seconds.")
        else:
            logger.error(f"Unexpected error in command {ctx.command}: {error}")
            await ctx.send("❌ An unexpected error occurred. Please try again.")
    
    async def on_message(self, message):
        """Handle messages"""
        # Don't respond to bots
        if message.author.bot:
            return
        
        # Process commands
        await self.process_commands(message)
        
        # Log non-command messages for analytics (optional)
        if not message.content.startswith(self.command_prefix):
            logger.debug(f"Message from {message.author}: {message.content[:50]}...")
    
    async def notify_click(self, link_data: dict, click_data: dict):
        """Send click notification to configured channel"""
        try:
            # You can configure a specific channel for notifications
            notification_channel_id = None  # Set this to your channel ID
            
            if notification_channel_id:
                channel = self.get_channel(notification_channel_id)
                if channel:
                    embed = discord.Embed(
                        title="🎯 Affiliate Link Clicked!",
                        color=0x00ff00,
                        timestamp=discord.utils.utcnow()
                    )
                    embed.add_field(
                        name="Link",
                        value=f"[{link_data['title']}]({link_data['affiliate_url']})",
                        inline=False
                    )
                    embed.add_field(name="Category", value=link_data['category'], inline=True)
                    embed.add_field(name="Short ID", value=link_data['short_id'], inline=True)
                    
                    if click_data.get('user_id'):
                        user = self.get_user(click_data['user_id'])
                        embed.add_field(
                            name="Clicked by",
                            value=user.display_name if user else "Unknown User",
                            inline=True
                        )
                    
                    await channel.send(embed=embed)
                    
        except Exception as e:
            logger.error(f"Error sending click notification: {e}")
    
    async def close(self):
        """Cleanup when bot shuts down"""
        await self.database.close()
        await super().close()
        logger.info("🔴 Bot disconnected and database closed")
