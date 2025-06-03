#!/usr/bin/env python3
"""
Create Help Command and Final Bot Setup
"""

import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='help', brief='Show bot commands and features')
    async def custom_help(self, ctx, command_name: str = None):
        """
        Show detailed help for bot commands
        Usage: !help [command_name]
        """
        if command_name:
            # Show help for specific command
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(
                    title=f"📚 Help: !{command.name}",
                    description=command.help or "No description available",
                    color=0x0099ff
                )
                embed.add_field(name="Brief", value=command.brief or "No brief available", inline=False)
                if hasattr(command, 'usage'):
                    embed.add_field(name="Usage", value=command.usage, inline=False)
            else:
                embed = discord.Embed(
                    title="❌ Command Not Found",
                    description=f"Command `{command_name}` not found. Use `!help` to see all commands.",
                    color=0xff0000
                )
        else:
            # Show all commands
            embed = discord.Embed(
                title="🤖 Discord Affiliate Marketing Bot",
                description="AI-powered affiliate marketing with click tracking and niche analysis",
                color=0x00ff00
            )
            
            # Affiliate Commands
            affiliate_commands = [
                "**!create** - Create tracked affiliate link",
                "**!links** - List your affiliate links", 
                "**!info** - Get detailed link information",
                "**!delete** - Delete an affiliate link"
            ]
            embed.add_field(
                name="🔗 Affiliate Commands",
                value="\n".join(affiliate_commands),
                inline=True
            )
            
            # AI Commands
            ai_commands = [
                "**!analyze** - AI niche analysis",
                "**!products** - Product recommendations",
                "**!optimize** - Content optimization tips",
                "**!trends** - Trending topics",
                "**!compete** - Competition analysis",
                "**!quick** - Quick AI insights"
            ]
            embed.add_field(
                name="🤖 AI Commands",
                value="\n".join(ai_commands),
                inline=True
            )
            
            # Analytics Commands
            analytics_commands = [
                "**!dashboard** - Your performance dashboard",
                "**!analytics** - Detailed link analytics",
                "**!leaderboard** - Top performing links",
                "**!export** - Export your data"
            ]
            embed.add_field(
                name="📊 Analytics Commands",
                value="\n".join(analytics_commands),
                inline=True
            )
            
            # Examples
            examples = [
                "`!create https://amzn.to/abc123 Gaming Mouse | Best gaming mouse 2024 | Gaming`",
                "`!analyze fitness equipment`",
                "`!products $100-500 smart home`",
                "`!dashboard`"
            ]
            embed.add_field(
                name="💡 Example Commands",
                value="\n".join(examples),
                inline=False
            )
            
            # Key Features
            features = [
                "🎯 **Click Tracking** - Real-time click notifications",
                "🤖 **AI Analysis** - Powered by Groq llama3-70b-8192",
                "📊 **Performance Analytics** - Detailed statistics", 
                "🔗 **Link Management** - Easy affiliate link creation",
                "💰 **Niche Research** - Find profitable opportunities"
            ]
            embed.add_field(
                name="✨ Key Features",
                value="\n".join(features),
                inline=False
            )
            
            embed.set_footer(text="Use !help <command> for detailed information about a specific command")
        
        await ctx.send(embed=embed)

# Add this to the bot client
def add_help_command_to_bot():
    """Function to add help command to existing bot"""
    return HelpCommands

if __name__ == "__main__":
    print("Help command module ready for import")