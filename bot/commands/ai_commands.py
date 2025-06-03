"""
AI-Powered Commands using Groq API
"""

import discord
from discord.ext import commands
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='analyze', brief='AI-powered niche analysis')
    @commands.cooldown(1, 30, commands.BucketType.user)  # 1 use per 30 seconds per user
    async def analyze_niche(self, ctx, *, niche: str):
        """
        Get AI-powered analysis of a niche for affiliate marketing
        Usage: !analyze <niche>
        Example: !analyze fitness equipment
        """
        try:
            # Send thinking message
            thinking_msg = await ctx.send("🤖 Analyzing niche with AI... This may take a moment.")
            
            # Check cache first
            cached_analysis = await self.bot.database.get_cached_niche_analysis(niche.lower())
            
            if cached_analysis:
                response = cached_analysis
                await thinking_msg.edit(content="🔄 Retrieved from cache!")
            else:
                # Get fresh analysis from Groq
                response = await self.bot.groq_service.analyze_niche(niche)
                
                # Cache the result
                await self.bot.database.cache_niche_analysis(niche.lower(), response)
                await thinking_msg.delete()
            
            # Create embed for better formatting
            embed = discord.Embed(
                title=f"🎯 Niche Analysis: {niche.title()}",
                description=response,
                color=0x00ff00,
                timestamp=discord.utils.utcnow()
            )
            
            embed.set_footer(text=f"Analysis requested by {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} analyzed niche: {niche}")
            
        except Exception as e:
            logger.error(f"Error in niche analysis: {e}")
            await ctx.send("❌ Error analyzing niche. Please try again later.")
    
    @commands.command(name='products', brief='Get AI product recommendations')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def recommend_products(self, ctx, budget: Optional[str] = None, *, niche: str):
        """
        Get AI-powered product recommendations for affiliate marketing
        Usage: !products [budget] <niche>
        Example: !products $100-500 gaming accessories
        """
        try:
            thinking_msg = await ctx.send("🤖 Finding best products to promote...")
            
            response = await self.bot.groq_service.recommend_products(niche, budget)
            await thinking_msg.delete()
            
            embed = discord.Embed(
                title=f"💰 Product Recommendations: {niche.title()}",
                description=response,
                color=0xffa500,
                timestamp=discord.utils.utcnow()
            )
            
            if budget:
                embed.add_field(name="Budget Range", value=budget, inline=True)
            
            embed.set_footer(text=f"Recommendations for {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} got product recommendations for: {niche}")
            
        except Exception as e:
            logger.error(f"Error in product recommendations: {e}")
            await ctx.send("❌ Error getting product recommendations. Please try again later.")
    
    @commands.command(name='optimize', brief='Get content optimization tips')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def optimize_content(self, ctx, content_type: str, niche: str, *, product: str):
        """
        Get AI-powered content optimization suggestions
        Usage: !optimize <content_type> <niche> <product>
        Example: !optimize blog fitness wireless earbuds
        """
        try:
            thinking_msg = await ctx.send("🤖 Generating optimization strategy...")
            
            response = await self.bot.groq_service.optimize_content(content_type, niche, product)
            await thinking_msg.delete()
            
            embed = discord.Embed(
                title=f"🚀 Content Optimization: {content_type.title()}",
                description=response,
                color=0x9932cc,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Niche", value=niche.title(), inline=True)
            embed.add_field(name="Product", value=product.title(), inline=True)
            embed.add_field(name="Content Type", value=content_type.title(), inline=True)
            
            embed.set_footer(text=f"Optimization for {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} optimized content: {content_type}/{niche}/{product}")
            
        except Exception as e:
            logger.error(f"Error in content optimization: {e}")
            await ctx.send("❌ Error generating optimization tips. Please try again later.")
    
    @commands.command(name='compete', brief='Analyze competition in a niche')
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def analyze_competition(self, ctx, niche: str, competitor_url: Optional[str] = None):
        """
        Get AI-powered competitive analysis
        Usage: !compete <niche> [competitor_url]
        Example: !compete tech reviews https://example.com
        """
        try:
            thinking_msg = await ctx.send("🤖 Analyzing competitive landscape...")
            
            response = await self.bot.groq_service.analyze_competition(niche, competitor_url)
            await thinking_msg.delete()
            
            embed = discord.Embed(
                title=f"🏁 Competitive Analysis: {niche.title()}",
                description=response,
                color=0xff4500,
                timestamp=discord.utils.utcnow()
            )
            
            if competitor_url:
                embed.add_field(name="Competitor Analyzed", value=competitor_url, inline=False)
            
            embed.set_footer(text=f"Analysis for {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} analyzed competition in: {niche}")
            
        except Exception as e:
            logger.error(f"Error in competition analysis: {e}")
            await ctx.send("❌ Error analyzing competition. Please try again later.")
    
    @commands.command(name='trends', brief='Get trending topics in a niche')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def get_trends(self, ctx, *, niche: str):
        """
        Get AI-powered trending topics and opportunities
        Usage: !trends <niche>
        Example: !trends home automation
        """
        try:
            thinking_msg = await ctx.send("🤖 Identifying trending opportunities...")
            
            response = await self.bot.groq_service.get_trending_topics(niche)
            await thinking_msg.delete()
            
            embed = discord.Embed(
                title=f"📈 Trending in {niche.title()}",
                description=response,
                color=0x1da1f2,
                timestamp=discord.utils.utcnow()
            )
            
            embed.set_footer(text=f"Trends for {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} checked trends for: {niche}")
            
        except Exception as e:
            logger.error(f"Error getting trends: {e}")
            await ctx.send("❌ Error getting trending topics. Please try again later.")
    
    @commands.command(name='quick', brief='Quick AI analysis')
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def quick_analysis(self, ctx, *, query: str):
        """
        Quick AI analysis for any affiliate marketing question
        Usage: !quick <your question>
        Example: !quick best niches for beginners
        """
        try:
            thinking_msg = await ctx.send("🤖 Getting quick AI insights...")
            
            # Create a general analysis prompt
            messages = [
                {
                    "role": "system", 
                    "content": "You are an expert affiliate marketing consultant. Provide concise, actionable advice."
                },
                {
                    "role": "user", 
                    "content": f"As an affiliate marketing expert, answer this question: {query}\n\nProvide a helpful, practical response under 1000 characters."
                }
            ]
            
            response = await self.bot.groq_service._make_request(messages, max_tokens=800)
            await thinking_msg.delete()
            
            embed = discord.Embed(
                title="🤖 Quick AI Insight",
                description=response,
                color=0x00ced1,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Your Question", value=query, inline=False)
            embed.set_footer(text=f"Asked by {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            logger.info(f"User {ctx.author.id} asked: {query}")
            
        except Exception as e:
            logger.error(f"Error in quick analysis: {e}")
            await ctx.send("❌ Error getting AI insights. Please try again later.")
