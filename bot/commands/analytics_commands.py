"""
Analytics and Performance Tracking Commands
"""

import discord
from discord.ext import commands
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AnalyticsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='dashboard', brief='View your affiliate dashboard')
    async def dashboard(self, ctx):
        """
        View your complete affiliate marketing dashboard
        Usage: !dashboard
        """
        try:
            dashboard_data = await self.bot.affiliate_service.get_user_dashboard(ctx.author.id)
            
            embed = discord.Embed(
                title=f"📊 {ctx.author.display_name}'s Affiliate Dashboard",
                color=0x0099ff,
                timestamp=discord.utils.utcnow()
            )
            
            # Overview stats
            embed.add_field(
                name="📈 Overview",
                value=f"**Total Links:** {dashboard_data['total_links']}\n"
                      f"**Total Clicks:** {dashboard_data['total_clicks']}\n"
                      f"**Avg Clicks/Link:** {dashboard_data['average_clicks_per_link']:.1f}",
                inline=True
            )
            
            # Top performing links
            if dashboard_data['top_performing']:
                top_links_text = ""
                for i, link in enumerate(dashboard_data['top_performing'][:3], 1):
                    top_links_text += f"{i}. **{link['title']}** ({link['clicks']} clicks)\n"
                
                embed.add_field(
                    name="🏆 Top Performers",
                    value=top_links_text or "No clicks yet",
                    inline=True
                )
            
            # Recent activity
            if dashboard_data['recent_links']:
                recent_text = ""
                for link in dashboard_data['recent_links'][:3]:
                    recent_text += f"• **{link['title']}** ({link['clicks']} clicks)\n"
                
                embed.add_field(
                    name="🕒 Recent Links",
                    value=recent_text,
                    inline=True
                )
            
            # Quick actions
            embed.add_field(
                name="⚡ Quick Actions",
                value="• `!create` - Create new link\n"
                      "• `!analyze <niche>` - AI analysis\n"
                      "• `!links` - View all links",
                inline=False
            )
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} viewed dashboard")
            
        except Exception as e:
            logger.error(f"Error showing dashboard: {e}")
            await ctx.send("❌ Error loading dashboard. Please try again.")
    
    @commands.command(name='analytics', brief='Detailed analytics for a link')
    async def detailed_analytics(self, ctx, short_id: str):
        """
        Get detailed analytics for a specific link
        Usage: !analytics <short_id>
        """
        try:
            analytics = await self.bot.affiliate_service.get_link_analytics(short_id, ctx.author.id)
            
            if not analytics:
                await ctx.send("❌ Link not found or you don't have permission to view it.")
                return
            
            link_info = analytics['link_info']
            stats = analytics['stats']
            
            embed = discord.Embed(
                title=f"📊 Analytics: {link_info['title']}",
                color=0x0099ff,
                timestamp=discord.utils.utcnow()
            )
            
            # Basic info
            embed.add_field(name="Short ID", value=f"`{link_info['short_id']}`", inline=True)
            embed.add_field(name="Category", value=link_info['category'], inline=True)
            embed.add_field(name="Status", value="🟢 Active" if link_info['is_active'] else "🔴 Inactive", inline=True)
            
            # Performance metrics
            embed.add_field(
                name="📈 Performance (30 days)",
                value=f"**Total Clicks:** {stats['total_clicks']}\n"
                      f"**Unique Users:** {stats['unique_users']}\n"
                      f"**Active Days:** {stats['active_days']}/30",
                inline=True
            )
            
            # Calculated metrics
            if stats['total_clicks'] > 0:
                click_rate = (stats['unique_users'] / stats['total_clicks']) * 100
                daily_avg = stats['total_clicks'] / max(1, stats['active_days'])
                
                embed.add_field(
                    name="📊 Calculated Metrics",
                    value=f"**Unique Click Rate:** {click_rate:.1f}%\n"
                          f"**Daily Average:** {daily_avg:.1f} clicks\n"
                          f"**Engagement:** {'High' if click_rate > 50 else 'Medium' if click_rate > 25 else 'Low'}",
                    inline=True
                )
            
            # Tracking URL
            embed.add_field(
                name="🔗 Tracking URL",
                value=f"`{analytics['tracking_url']}`",
                inline=False
            )
            
            # Recommendations
            recommendations = []
            if stats['total_clicks'] == 0:
                recommendations.append("💡 No clicks yet - try promoting on different platforms")
            elif stats['total_clicks'] < 10:
                recommendations.append("💡 Low traffic - consider improving your promotional strategy")
            elif stats['unique_users'] / max(1, stats['total_clicks']) < 0.3:
                recommendations.append("💡 High repeat clicks - good engagement but try reaching new audiences")
            else:
                recommendations.append("🎉 Great performance! Keep up the good work")
            
            if recommendations:
                embed.add_field(
                    name="💡 Recommendations",
                    value="\n".join(recommendations),
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error showing analytics: {e}")
            await ctx.send("❌ Error loading analytics. Please try again.")
    
    @commands.command(name='leaderboard', brief='See top performers')
    async def leaderboard(self, ctx):
        """
        View leaderboard of top performing links (public)
        Usage: !leaderboard
        """
        try:
            # Get top links across all users (you might want to make this configurable)
            cursor = await self.bot.database.connection.execute(
                """
                SELECT 
                    al.title,
                    al.category,
                    u.display_name as creator,
                    COUNT(ct.id) as clicks
                FROM affiliate_links al
                LEFT JOIN click_tracking ct ON al.id = ct.link_id
                LEFT JOIN (
                    SELECT DISTINCT created_by, 'Anonymous' as display_name 
                    FROM affiliate_links
                ) u ON al.created_by = u.created_by
                WHERE al.is_active = 1
                GROUP BY al.id
                HAVING clicks > 0
                ORDER BY clicks DESC
                LIMIT 10
                """
            )
            
            rows = await cursor.fetchall()
            
            if not rows:
                await ctx.send("📊 No data available for leaderboard yet.")
                return
            
            embed = discord.Embed(
                title="🏆 Top Performing Links",
                description="Most clicked affiliate links across all users",
                color=0xffd700,
                timestamp=discord.utils.utcnow()
            )
            
            for i, (title, category, creator, clicks) in enumerate(rows, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                
                embed.add_field(
                    name=f"{medal} {title}",
                    value=f"**Category:** {category}\n**Clicks:** {clicks}",
                    inline=True if i <= 6 else False
                )
            
            embed.set_footer(text="Create your own tracked links with !create")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} viewed leaderboard")
            
        except Exception as e:
            logger.error(f"Error showing leaderboard: {e}")
            await ctx.send("❌ Error loading leaderboard. Please try again.")
    
    @commands.command(name='export', brief='Export your data')
    async def export_data(self, ctx):
        """
        Export your affiliate link data
        Usage: !export
        """
        try:
            user_links = await self.bot.database.get_user_links(ctx.author.id)
            
            if not user_links:
                await ctx.send("📝 No data to export.")
                return
            
            # Create a simple CSV-like format
            export_text = "Title,Category,Short_ID,Clicks,Created_Date\n"
            
            for link in user_links:
                export_text += f"\"{link['title']}\",\"{link['category']}\",{link['short_id']},{link['clicks']},{link['created_at']}\n"
            
            # Send as a file
            file = discord.File(
                filename=f"affiliate_links_{ctx.author.id}_{datetime.now().strftime('%Y%m%d')}.csv",
                fp=discord.utils.StringIO(export_text)
            )
            
            embed = discord.Embed(
                title="📤 Data Export",
                description=f"Your affiliate link data ({len(user_links)} links)",
                color=0x00ff00
            )
            
            await ctx.send(embed=embed, file=file)
            logger.info(f"User {ctx.author.id} exported data")
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            await ctx.send("❌ Error exporting data. Please try again.")
