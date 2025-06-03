#!/usr/bin/env python3
"""
Test script for Discord Affiliate Marketing Bot
Tests all core functionality without requiring Discord connection
"""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.core.database import Database
from bot.services.groq_service import GroqService
from bot.services.affiliate_service import AffiliateService

async def test_database():
    """Test database functionality"""
    print("🧪 Testing Database...")
    
    db = Database(":memory:")  # Use in-memory database for testing
    await db.initialize()
    
    # Test creating affiliate link
    link_id = await db.create_affiliate_link(
        short_id="test123",
        original_url="https://example.com/product",
        affiliate_url="https://amzn.to/test123",
        title="Test Product",
        description="A test product for testing",
        category="Electronics",
        created_by=12345
    )
    
    print(f"   ✅ Created link with ID: {link_id}")
    
    # Test retrieving link
    link_data = await db.get_affiliate_link("test123")
    assert link_data is not None
    assert link_data['title'] == "Test Product"
    print(f"   ✅ Retrieved link: {link_data['title']}")
    
    # Test click tracking
    click_id = await db.track_click(link_id, user_id=67890, ip_address="192.168.1.1")
    print(f"   ✅ Tracked click with ID: {click_id}")
    
    # Test stats
    stats = await db.get_click_stats(link_id)
    assert stats['total_clicks'] == 1
    print(f"   ✅ Click stats: {stats}")
    
    # Test user links
    user_links = await db.get_user_links(12345)
    assert len(user_links) == 1
    print(f"   ✅ User has {len(user_links)} links")
    
    await db.close()
    print("   ✅ Database tests passed!\n")

async def test_groq_service():
    """Test Groq AI service (without actual API calls)"""
    print("🧪 Testing Groq Service...")
    
    groq_service = GroqService()
    
    # Mock the API call for testing
    async def mock_api_call(messages, max_tokens=2000):
        return "This is a mock AI response for testing purposes."
    
    groq_service._make_request = mock_api_call
    
    # Test niche analysis
    analysis = await groq_service.analyze_niche("fitness equipment")
    assert "mock AI response" in analysis
    print("   ✅ Niche analysis working")
    
    # Test product recommendations
    products = await groq_service.recommend_products("home automation", "$100-500")
    assert "mock AI response" in products
    print("   ✅ Product recommendations working")
    
    # Test content optimization
    optimization = await groq_service.optimize_content("blog", "tech", "wireless headphones")
    assert "mock AI response" in optimization
    print("   ✅ Content optimization working")
    
    print("   ✅ Groq service tests passed!\n")

async def test_affiliate_service():
    """Test affiliate service functionality"""
    print("🧪 Testing Affiliate Service...")
    
    db = Database(":memory:")
    await db.initialize()
    
    affiliate_service = AffiliateService(db)
    
    # Test creating affiliate link
    short_id, link_id = await affiliate_service.create_affiliate_link(
        original_url="https://example.com/product",
        affiliate_url="https://amzn.to/test456",
        title="Gaming Headset",
        description="High-quality gaming headset",
        category="Gaming",
        created_by=11111
    )
    
    print(f"   ✅ Created affiliate link: {short_id}")
    
    # Test tracking URL generation
    tracking_url = affiliate_service.get_tracking_url(short_id)
    assert "track" in tracking_url
    print(f"   ✅ Tracking URL: {tracking_url}")
    
    # Test click tracking
    success, redirect_url = await affiliate_service.track_click(
        short_id=short_id,
        user_id=22222,
        ip_address="10.0.0.1"
    )
    
    assert success is True
    assert redirect_url == "https://amzn.to/test456"
    print("   ✅ Click tracking working")
    
    # Test analytics
    analytics = await affiliate_service.get_link_analytics(short_id, 11111)
    assert analytics is not None
    assert analytics['stats']['total_clicks'] == 1
    print("   ✅ Link analytics working")
    
    # Test dashboard
    dashboard = await affiliate_service.get_user_dashboard(11111)
    assert dashboard['total_links'] == 1
    assert dashboard['total_clicks'] == 1
    print("   ✅ User dashboard working")
    
    # Test URL validation
    is_valid, message = affiliate_service.validate_affiliate_url("https://amzn.to/test")
    assert is_valid is True
    print("   ✅ URL validation working")
    
    # Test affiliate info extraction
    affiliate_info = affiliate_service.extract_affiliate_info("https://amazon.com/dp/B123?tag=mystore-20")
    assert affiliate_info['network'] == 'Amazon Associates'
    print("   ✅ Affiliate info extraction working")
    
    await db.close()
    print("   ✅ Affiliate service tests passed!\n")

async def test_click_server():
    """Test click tracking server components"""
    print("🧪 Testing Click Server Components...")
    
    # Test that we can import the server
    try:
        from click_server import app
        print("   ✅ Click server imports successfully")
    except Exception as e:
        print(f"   ❌ Click server import failed: {e}")
        return
    
    print("   ✅ Click server tests passed!\n")

def test_bot_structure():
    """Test bot structure and imports"""
    print("🧪 Testing Bot Structure...")
    
    try:
        from bot.core.bot_client import AffiliateBot
        from bot.commands.affiliate_commands import AffiliateCommands
        from bot.commands.ai_commands import AICommands
        from bot.commands.analytics_commands import AnalyticsCommands
        from bot.utils.config import Config
        
        print("   ✅ All bot modules import successfully")
        
        # Test configuration
        missing_vars = Config.get_missing_vars()
        print(f"   📋 Missing environment variables: {missing_vars}")
        
        print("   ✅ Bot structure tests passed!\n")
        
    except Exception as e:
        print(f"   ❌ Bot structure test failed: {e}")

async def main():
    """Run all tests"""
    print("🤖 Discord Affiliate Marketing Bot - Test Suite")
    print("=" * 60)
    
    # Test basic structure
    test_bot_structure()
    
    # Test core components
    await test_database()
    await test_groq_service()
    await test_affiliate_service()
    await test_click_server()
    
    print("=" * 60)
    print("🎉 All tests completed!")
    print("\n📋 Next Steps:")
    print("1. Get your Discord Bot Token from https://discord.com/developers/applications")
    print("2. Get your Groq API Key from https://console.groq.com/")
    print("3. Create a .env file with your API keys")
    print("4. Run the bot with: python3 discord_bot.py")
    print("5. Start the click server with: python3 click_server.py")
    print("\n🔗 The bot will create tracking URLs that redirect through your click server")
    print("💰 Every click will be tracked and you'll get notifications!")

if __name__ == "__main__":
    asyncio.run(main())