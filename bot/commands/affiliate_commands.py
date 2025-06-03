"""
Affiliate Link Management Commands
"""

import discord
from discord.ext import commands
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AffiliateCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='create', brief='Create a new affiliate link')
    async def create_affiliate_link(self, ctx, affiliate_url: str, *, details: str):
        """
        Create a new tracked affiliate link
        Usage: !create <affiliate_url> <title> | <description> | <category>
        Example: !create https://amzn.to/abc123 Amazing Headphones | Best wireless headphones 2024 | Electronics
        """
        try:
            # Parse details
            parts = details.split(' | ')
            if len(parts) != 3:
                await ctx.send("❌ Please use format: `!create <url> <title> | <description> | <category>`")
                return
            
            title, description, category = [part.strip() for part in parts]
            
            # Validate affiliate URL
            is_valid, message = self.bot.affiliate_service.validate_affiliate_url(affiliate_url)
            if not is_valid:
                await ctx.send(f"❌ {message}")
                return
            
            # Create the link
            short_id, link_id = await self.bot.affiliate_service.create_affiliate_link(
                original_url=affiliate_url,  # For now, same as affiliate
                affiliate_url=affiliate_url,
                title=title,
                description=description,
                category=category,
                created_by=ctx.author.id
            )
            
            # Get tracking URL
            tracking_url = self.bot.affiliate_service.get_tracking_url(short_id)
            
            # Get affiliate info
            affiliate_info = self.bot.affiliate_service.extract_affiliate_info(affiliate_url)
            
            # Create response embed
            embed = discord.Embed(
                title="✅ Affiliate Link Created!",
                color=0x00ff00,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Title", value=title, inline=False)
            embed.add_field(name="Category", value=category, inline=True)
            embed.add_field(name="Short ID", value=short_id, inline=True)
            embed.add_field(name="Network", value=affiliate_info.get('network', 'Unknown'), inline=True)
            
            embed.add_field(
                name="🔗 Tracking URL",
                value=f"`{tracking_url}`",
                inline=False
            )
            
            embed.add_field(
                name="📊 Share This",
                value=f"Use this URL to track clicks: {tracking_url}",
                inline=False
            )
            
            embed.set_footer(text=f"Created by {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} created affiliate link {short_id}")
            
        except Exception as e:
            logger.error(f"Error creating affiliate link: {e}")
            await ctx.send("❌ Error creating affiliate link. Please try again.")
    
    @commands.command(name='links', brief='List your affiliate links')
    async def list_links(self, ctx, limit: Optional[int] = 10):
        """
        List your affiliate links
        Usage: !links [limit]
        """
        try:
            user_links = await self.bot.database.get_user_links(ctx.author.id)
            
            if not user_links:
                await ctx.send("📝 You haven't created any affiliate links yet. Use `!create` to get started!")
                return
            
            # Limit results
            user_links = user_links[:limit]
            
            embed = discord.Embed(
                title=f"🔗 Your Affiliate Links ({len(user_links)} shown)",
                color=0x0099ff,
                timestamp=discord.utils.utcnow()
            )
            
            for link in user_links:
                clicks = link.get('clicks', 0)
                click_text = f"👆 {clicks} clicks" if clicks > 0 else "👆 No clicks yet"
                
                embed.add_field(
                    name=f"**{link['title']}**",
                    value=f"Category: {link['category']}\n"
                          f"ID: `{link['short_id']}`\n"
                          f"{click_text}",
                    inline=True
                )
            
            embed.set_footer(text=f"Use !analytics <short_id> for detailed stats")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error listing links: {e}")
            await ctx.send("❌ Error retrieving your links. Please try again.")
    
    @commands.command(name='delete', brief='Delete an affiliate link')
    async def delete_link(self, ctx, short_id: str):
        """
        Delete one of your affiliate links
        Usage: !delete <short_id>
        """
        try:
            # Get link to verify ownership
            link_data = await self.bot.database.get_affiliate_link(short_id)
            
            if not link_data:
                await ctx.send("❌ Link not found.")
                return
            
            if link_data['created_by'] != ctx.author.id:
                await ctx.send("❌ You can only delete your own links.")
                return
            
            # Deactivate the link (soft delete)
            await self.bot.database.connection.execute(
                "UPDATE affiliate_links SET is_active = 0 WHERE short_id = ?",
                (short_id,)
            )
            await self.bot.database.connection.commit()
            
            await ctx.send(f"✅ Affiliate link `{short_id}` has been deleted.")
            logger.info(f"User {ctx.author.id} deleted link {short_id}")
            
        except Exception as e:
            logger.error(f"Error deleting link: {e}")
            await ctx.send("❌ Error deleting link. Please try again.")
    
    @commands.command(name='info', brief='Get detailed info about a link')
    async def link_info(self, ctx, short_id: str):
        """
        Get detailed information about an affiliate link
        Usage: !info <short_id>
        """
        try:
            analytics = await self.bot.affiliate_service.get_link_analytics(short_id, ctx.author.id)
            
            if not analytics:
                await ctx.send("❌ Link not found or you don't have permission to view it.")
                return
            
            link_info = analytics['link_info']
            stats = analytics['stats']
            
            embed = discord.Embed(
                title=f"📊 Link Analytics: {link_info['title']}",
                color=0x0099ff,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Short ID", value=link_info['short_id'], inline=True)
            embed.add_field(name="Category", value=link_info['category'], inline=True)
            embed.add_field(name="Created", value=link_info['created_at'], inline=True)
            
            embed.add_field(name="📈 Total Clicks", value=stats['total_clicks'], inline=True)
            embed.add_field(name="👥 Unique Users", value=stats['unique_users'], inline=True)
            embed.add_field(name="📅 Active Days", value=stats['active_days'], inline=True)
            
            embed.add_field(
                name="🔗 Tracking URL",
                value=f"`{analytics['tracking_url']}`",
                inline=False
            )
            
            embed.add_field(
                name="Description",
                value=link_info['description'],
                inline=False
            )
            
            # Get affiliate network info
            affiliate_info = self.bot.affiliate_service.extract_affiliate_info(link_info['affiliate_url'])
            embed.add_field(
                name="Network Info",
                value=f"**Network:** {affiliate_info.get('network', 'Unknown')}\n"
                      f"**Commission Rate:** {affiliate_info.get('commission_rate', 'Unknown')}",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error getting link info: {e}")
            await ctx.send("❌ Error retrieving link information. Please try again.")
