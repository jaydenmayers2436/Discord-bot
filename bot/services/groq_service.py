"""
Groq AI Service for niche analysis and product recommendations
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional
from bot.utils.config import Config

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            logger.error("Groq API key not found!")
            
        logger.info(f"✅ Groq service initialized with model: {self.model}")
    
    async def _make_request(self, messages: List[Dict], max_tokens: int = 2000) -> Optional[str]:
        """Make a request to Groq API"""
        if not self.api_key:
            return "❌ Groq API key not configured"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content'].strip()
                    else:
                        error_text = await response.text()
                        logger.error(f"Groq API error {response.status}: {error_text}")
                        return f"❌ API Error: {response.status}"
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return f"❌ Network Error: {str(e)}"
    
    async def analyze_niche(self, niche: str) -> str:
        """Analyze a niche for affiliate marketing opportunities"""
        prompt = f"""
        As an expert affiliate marketer, analyze the "{niche}" niche for affiliate marketing opportunities.
        
        Provide a comprehensive analysis including:
        
        📊 **Market Analysis:**
        - Market size and growth potential
        - Target audience demographics
        - Seasonal trends and patterns
        
        💰 **Monetization Opportunities:**
        - High-converting product categories
        - Average commission rates
        - Top affiliate programs/networks
        
        🎯 **Content Strategy:**
        - Best content types for this niche
        - Trending keywords and topics
        - Platform recommendations (Blog, YouTube, Social Media)
        
        ⚠️ **Challenges & Competition:**
        - Market saturation level
        - Main competitors
        - Potential obstacles
        
        🚀 **Action Plan:**
        - 3 specific product types to promote
        - Content ideas for immediate implementation
        - Growth strategies
        
        Keep the response detailed but concise, under 1500 characters for Discord.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert affiliate marketing analyst with years of experience in niche research and optimization."},
            {"role": "user", "content": prompt}
        ]
        
        return await self._make_request(messages, max_tokens=1500)
    
    async def recommend_products(self, niche: str, budget: Optional[str] = None) -> str:
        """Recommend specific products for affiliate promotion"""
        budget_text = f" with a budget of {budget}" if budget else ""
        
        prompt = f"""
        Recommend specific product types and categories for affiliate marketing in the "{niche}" niche{budget_text}.
        
        Provide:
        
        🎯 **Top 5 Product Recommendations:**
        1. Product type + why it converts well
        2. Expected commission range
        3. Target customer profile
        
        📈 **Trending Products:**
        - What's hot right now in this niche
        - Seasonal opportunities
        - Emerging product categories
        
        💡 **Pro Tips:**
        - Best promotional strategies for each product
        - Platforms where these products perform best
        - Content angles that drive sales
        
        🔍 **Research Keywords:**
        - High-intent buyer keywords
        - Product comparison terms
        - Problem-solving searches
        
        Format for Discord readability, under 1500 characters.
        """
        
        messages = [
            {"role": "system", "content": "You are a seasoned affiliate marketer specializing in product research and conversion optimization."},
            {"role": "user", "content": prompt}
        ]
        
        return await self._make_request(messages, max_tokens=1500)
    
    async def optimize_content(self, content_type: str, niche: str, product: str) -> str:
        """Generate optimized content ideas for affiliate marketing"""
        prompt = f"""
        Create optimized {content_type} content strategy for promoting "{product}" in the "{niche}" niche.
        
        Provide:
        
        📝 **Content Ideas:**
        - 3 high-converting content angles
        - Attention-grabbing headlines/titles
        - Hook strategies for engagement
        
        🔍 **SEO Strategy:**
        - Primary keywords to target
        - Long-tail keyword opportunities
        - Content structure recommendations
        
        🎯 **Conversion Tactics:**
        - Where to place affiliate links naturally
        - Call-to-action examples
        - Trust-building elements
        
        📊 **Performance Tracking:**
        - Metrics to monitor
        - A/B testing suggestions
        - Optimization opportunities
        
        Keep practical and actionable, under 1500 characters.
        """
        
        messages = [
            {"role": "system", "content": "You are a content marketing expert focused on affiliate marketing conversions and SEO optimization."},
            {"role": "user", "content": prompt}
        ]
        
        return await self._make_request(messages, max_tokens=1500)
    
    async def analyze_competition(self, niche: str, competitor_url: Optional[str] = None) -> str:
        """Analyze competition in a niche"""
        competitor_text = f" Also analyze this competitor: {competitor_url}" if competitor_url else ""
        
        prompt = f"""
        Analyze the competition landscape for the "{niche}" affiliate marketing niche.{competitor_text}
        
        Provide:
        
        🏁 **Competitive Landscape:**
        - Market saturation level (Low/Medium/High)
        - Main types of competitors
        - Barrier to entry assessment
        
        💪 **Competitive Advantages:**
        - Gaps in the market you can exploit
        - Underserved customer segments
        - Content opportunities competitors miss
        
        📊 **Benchmark Analysis:**
        - Average content quality standards
        - Common promotional strategies
        - Pricing and commission comparisons
        
        🚀 **Differentiation Strategy:**
        - How to stand out from competitors
        - Unique value propositions to consider
        - Blue ocean opportunities
        
        ⚡ **Quick Wins:**
        - Immediate opportunities to capture
        - Low-hanging fruit in this niche
        
        Format for Discord, under 1500 characters.
        """
        
        messages = [
            {"role": "system", "content": "You are a competitive intelligence analyst specializing in affiliate marketing and digital business strategy."},
            {"role": "user", "content": prompt}
        ]
        
        return await self._make_request(messages, max_tokens=1500)
    
    async def get_trending_topics(self, niche: str) -> str:
        """Get trending topics and opportunities in a niche"""
        prompt = f"""
        Identify current trending topics and emerging opportunities in the "{niche}" niche for affiliate marketing.
        
        📈 **Current Trends:**
        - What's trending now in this niche
        - Social media buzz topics
        - Search volume spikes
        
        🔮 **Emerging Opportunities:**
        - New product categories gaining traction
        - Underexplored sub-niches
        - Technology disruptions creating opportunities
        
        📅 **Seasonal Patterns:**
        - Best times of year for this niche
        - Holiday/event-driven opportunities
        - Cyclical buying patterns
        
        💎 **Hidden Gems:**
        - Lesser-known but profitable angles
        - Micro-niches with high potential
        - Cross-over opportunities from related niches
        
        🎯 **Action Items:**
        - Top 3 trends to capitalize on immediately
        - Content ideas for each trend
        
        Keep concise for Discord, under 1500 characters.
        """
        
        messages = [
            {"role": "system", "content": "You are a trend analyst and affiliate marketing strategist with expertise in identifying profitable opportunities."},
            {"role": "user", "content": prompt}
        ]
        
        return await self._make_request(messages, max_tokens=1500)
