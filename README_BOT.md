# 🤖 Discord Affiliate Marketing Bot

An AI-powered Discord bot for affiliate marketing with advanced click tracking, niche analysis, and performance analytics. Built with Groq AI (llama3-70b-8192) for intelligent insights and recommendations.

## ✨ Features

### 🔗 Affiliate Link Management
- **Smart Link Creation**: Generate tracked affiliate links with custom short IDs
- **Click Tracking**: Real-time click notifications and detailed analytics
- **Link Analytics**: Performance metrics, unique users, and engagement rates
- **Bulk Management**: List, edit, and delete your affiliate links

### 🤖 AI-Powered Insights (Groq llama3-70b-8192)
- **Niche Analysis**: Deep market research and opportunity identification
- **Product Recommendations**: AI-suggested products based on trends and profitability
- **Content Optimization**: SEO and conversion tips for your content
- **Competition Analysis**: Market landscape and competitive intelligence
- **Trend Detection**: Emerging opportunities and seasonal patterns

### 📊 Advanced Analytics
- **Real-time Dashboard**: Complete performance overview
- **Click Statistics**: Detailed tracking with IP, user agent, and referrer data
- **Performance Metrics**: Conversion rates, engagement analysis
- **Data Export**: CSV export for external analysis
- **Leaderboards**: Compare performance across users

### 🎯 Discord Integration
- **Slash Commands**: Easy-to-use command interface
- **Rich Embeds**: Beautiful, informative responses
- **DM Support**: Works in direct messages and channels
- **Permission System**: Secure access control

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Discord Bot Token
- Groq API Key

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd discord-affiliate-bot

# Run setup script
python3 setup_bot.py
```

### 3. Configuration

Create `.env` file with your API keys:

```env
# Discord Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token
COMMAND_PREFIX=!

# Groq AI Configuration  
GROQ_API_KEY=your_groq_api_key

# Optional: Click Tracking
AFFILIATE_DOMAIN=your-domain.com
CLICK_NOTIFICATION_CHANNEL=your_channel_id
```

### 4. Get API Keys

#### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application → Bot section
3. Copy the token

#### Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/login
3. Create an API key

### 5. Run the Bot

```bash
# Start the Discord bot
python3 discord_bot.py

# Start click tracking server (optional)
python3 click_server.py
```

## 📚 Commands

### 🔗 Affiliate Commands
```bash
!create <url> <title> | <description> | <category>
# Example: !create https://amzn.to/abc123 Gaming Mouse | Best wireless gaming mouse | Gaming

!links [limit]           # List your affiliate links
!info <short_id>         # Detailed link information  
!delete <short_id>       # Delete a link
```

### 🤖 AI Commands
```bash
!analyze <niche>                    # AI niche analysis
!products [budget] <niche>          # Product recommendations
!optimize <content_type> <niche> <product>  # Content optimization
!trends <niche>                     # Trending topics
!compete <niche> [competitor_url]   # Competition analysis
!quick <question>                   # Quick AI insights
```

### 📊 Analytics Commands
```bash
!dashboard              # Your performance dashboard
!analytics <short_id>   # Detailed link analytics
!leaderboard           # Top performing links
!export               # Export your data
```

### 💡 Example Usage

```bash
# Create a tracked affiliate link
!create https://amzn.to/gaming123 Razer Gaming Mouse | Top-rated wireless gaming mouse 2024 | Gaming

# Analyze a niche for opportunities
!analyze fitness equipment

# Get product recommendations with budget
!products $100-500 smart home devices

# Optimize content for better conversions
!optimize blog tech wireless headphones

# Check trending topics
!trends home automation

# View your performance
!dashboard
```

## 🏗️ Architecture

### Core Components

```
📁 bot/
├── 🎮 core/
│   ├── bot_client.py      # Main Discord bot client
│   └── database.py        # SQLite database management
├── 🔧 services/
│   ├── groq_service.py    # Groq AI integration
│   └── affiliate_service.py  # Link management & tracking
├── ⚡ commands/
│   ├── affiliate_commands.py  # Link management commands
│   ├── ai_commands.py         # AI-powered commands
│   ├── analytics_commands.py  # Performance tracking
│   └── help_commands.py       # Help system
└── 🛠️ utils/
    └── config.py          # Configuration management
```

### Database Schema

```sql
-- Affiliate links with tracking
affiliate_links (id, short_id, original_url, affiliate_url, title, description, category, created_by, created_at, is_active)

-- Click tracking with analytics
click_tracking (id, link_id, user_id, ip_address, user_agent, referrer, clicked_at)

-- Performance metrics
link_performance (id, link_id, date, clicks, conversions, revenue)

-- AI analysis cache
niche_analysis_cache (id, niche_query, analysis_data, created_at, expires_at)

-- User preferences
user_preferences (user_id, preferred_categories, notification_settings)
```

## 🔄 Click Tracking Flow

1. **Link Creation**: User creates affiliate link via `!create`
2. **Short URL Generation**: Bot generates unique tracking URL
3. **Click Detection**: User shares tracking URL, clicks are detected
4. **Data Collection**: IP, user agent, referrer tracked
5. **Notification**: Real-time click notifications sent
6. **Analytics**: Performance metrics calculated and stored

## 🤖 AI Features (Groq Integration)

### Niche Analysis
- Market size and growth potential
- Target audience demographics  
- Monetization opportunities
- Competition analysis
- Action plans

### Product Recommendations
- High-converting product categories
- Commission rate analysis
- Trending products
- Seasonal opportunities

### Content Optimization  
- SEO keyword strategies
- Conversion tactics
- Platform-specific tips
- Performance tracking

## 📊 Analytics Dashboard

### Key Metrics
- **Total Links**: Number of affiliate links created
- **Total Clicks**: Aggregate click count across all links
- **Unique Users**: Number of distinct users who clicked
- **Conversion Rate**: Clicks to conversions ratio
- **Top Performers**: Best performing links by category

### Advanced Analytics
- **Geographic Distribution**: Click origins by location
- **Device Analytics**: Desktop vs mobile clicks
- **Time-based Trends**: Performance over time
- **Referrer Analysis**: Traffic sources

## 🛡️ Security Features

- **Input Validation**: All user inputs sanitized
- **Rate Limiting**: API cooldowns prevent abuse
- **Permission System**: User-specific data access
- **Secure Token Storage**: Environment variable configuration
- **SQL Injection Protection**: Parameterized queries

## 🔧 Configuration Options

### Environment Variables
```env
# Core Configuration
DISCORD_BOT_TOKEN=          # Required: Discord bot token
GROQ_API_KEY=              # Required: Groq API key
COMMAND_PREFIX=!           # Optional: Command prefix (default: !)
DATABASE_URL=              # Optional: Database URL (default: SQLite)

# Click Tracking
AFFILIATE_DOMAIN=          # Optional: Your tracking domain
CLICK_NOTIFICATION_CHANNEL= # Optional: Discord channel for notifications
WEBHOOK_URL=               # Optional: External webhook for notifications

# Performance
CACHE_TTL=3600            # Optional: AI response cache time (seconds)
MAX_EMBED_LENGTH=2000     # Optional: Maximum embed length
```

## 🧪 Testing

```bash
# Run comprehensive tests
python3 test_bot.py

# Test individual components
python3 -m pytest tests/

# Test database functionality
python3 -c "from bot.core.database import Database; import asyncio; asyncio.run(Database(':memory:').initialize())"
```

## 📈 Performance Optimization

### Database Optimization
- **Indexed Queries**: Fast lookups on frequently accessed columns
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Optimized SQL for analytics

### API Optimization
- **Response Caching**: Cache AI responses to reduce API calls
- **Rate Limiting**: Prevent API quota exhaustion
- **Async Operations**: Non-blocking database and API calls

### Memory Management
- **Connection Cleanup**: Proper resource cleanup
- **Cache Management**: Automatic cache expiration
- **Memory Monitoring**: Track memory usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**Bot doesn't respond**
- Check Discord bot token
- Verify bot permissions in server
- Check console for error messages

**AI commands timeout**
- Verify Groq API key
- Check API rate limits
- Monitor API status

**Click tracking not working**
- Ensure click server is running
- Check domain configuration
- Verify database connectivity

### Getting Help

- 📧 Create an issue on GitHub
- 💬 Join our Discord support server
- 📖 Check the documentation wiki

## 🎯 Roadmap

### Upcoming Features
- **Advanced AI Models**: Integration with multiple AI providers
- **Web Dashboard**: Browser-based analytics interface  
- **Webhook Integrations**: Zapier, IFTTT compatibility
- **Multi-language Support**: Internationalization
- **Advanced Reporting**: PDF report generation
- **Team Management**: Multi-user organizations

### Version History
- **v1.0.0**: Initial release with core features
- **v1.1.0**: Enhanced AI analysis (Planned)
- **v1.2.0**: Web dashboard (Planned)

---

Built with ❤️ for affiliate marketers who want to leverage AI and automation for better results.