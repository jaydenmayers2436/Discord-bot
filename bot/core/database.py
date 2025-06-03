"""
Database management for affiliate tracking and analytics
"""

import aiosqlite
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "affiliate_bot.db"):
        self.db_path = db_path
        self.connection = None
    
    async def initialize(self):
        """Initialize database connection and create tables"""
        self.connection = await aiosqlite.connect(self.db_path)
        await self._create_tables()
        logger.info("✅ Database initialized")
    
    async def _create_tables(self):
        """Create necessary database tables"""
        tables = [
            # Affiliate links table
            """
            CREATE TABLE IF NOT EXISTS affiliate_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                affiliate_url TEXT NOT NULL,
                title TEXT,
                description TEXT,
                category TEXT,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
            """,
            
            # Click tracking table
            """
            CREATE TABLE IF NOT EXISTS click_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link_id INTEGER NOT NULL,
                user_id INTEGER,
                ip_address TEXT,
                user_agent TEXT,
                referrer TEXT,
                clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (link_id) REFERENCES affiliate_links (id)
            )
            """,
            
            # User preferences table
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                preferred_categories TEXT,
                notification_settings TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            # Niche analysis cache
            """
            CREATE TABLE IF NOT EXISTS niche_analysis_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                niche_query TEXT NOT NULL,
                analysis_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL
            )
            """,
            
            # Performance analytics
            """
            CREATE TABLE IF NOT EXISTS link_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link_id INTEGER NOT NULL,
                date DATE NOT NULL,
                clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                revenue DECIMAL(10,2) DEFAULT 0.00,
                FOREIGN KEY (link_id) REFERENCES affiliate_links (id),
                UNIQUE(link_id, date)
            )
            """
        ]
        
        for table_sql in tables:
            await self.connection.execute(table_sql)
        
        await self.connection.commit()
        logger.info("✅ Database tables created/verified")
    
    async def create_affiliate_link(self, short_id: str, original_url: str, 
                                  affiliate_url: str, title: str, description: str,
                                  category: str, created_by: int) -> int:
        """Create a new affiliate link"""
        cursor = await self.connection.execute(
            """
            INSERT INTO affiliate_links 
            (short_id, original_url, affiliate_url, title, description, category, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (short_id, original_url, affiliate_url, title, description, category, created_by)
        )
        await self.connection.commit()
        return cursor.lastrowid
    
    async def get_affiliate_link(self, short_id: str) -> Optional[Dict]:
        """Get affiliate link by short ID"""
        cursor = await self.connection.execute(
            "SELECT * FROM affiliate_links WHERE short_id = ? AND is_active = 1",
            (short_id,)
        )
        row = await cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    async def track_click(self, link_id: int, user_id: Optional[int] = None,
                         ip_address: Optional[str] = None, user_agent: Optional[str] = None,
                         referrer: Optional[str] = None) -> int:
        """Track a click on an affiliate link"""
        cursor = await self.connection.execute(
            """
            INSERT INTO click_tracking 
            (link_id, user_id, ip_address, user_agent, referrer)
            VALUES (?, ?, ?, ?, ?)
            """,
            (link_id, user_id, ip_address, user_agent, referrer)
        )
        await self.connection.commit()
        
        # Update daily performance
        await self._update_daily_performance(link_id)
        
        return cursor.lastrowid
    
    async def _update_daily_performance(self, link_id: int):
        """Update daily performance statistics"""
        today = datetime.now().date()
        await self.connection.execute(
            """
            INSERT INTO link_performance (link_id, date, clicks)
            VALUES (?, ?, 1)
            ON CONFLICT(link_id, date) 
            DO UPDATE SET clicks = clicks + 1
            """,
            (link_id, today)
        )
        await self.connection.commit()
    
    async def get_click_stats(self, link_id: int, days: int = 30) -> Dict:
        """Get click statistics for a link"""
        start_date = datetime.now() - timedelta(days=days)
        
        cursor = await self.connection.execute(
            """
            SELECT 
                COUNT(*) as total_clicks,
                COUNT(DISTINCT DATE(clicked_at)) as active_days,
                COUNT(DISTINCT user_id) as unique_users
            FROM click_tracking 
            WHERE link_id = ? AND clicked_at >= ?
            """,
            (link_id, start_date)
        )
        row = await cursor.fetchone()
        
        if row:
            return {
                'total_clicks': row[0],
                'active_days': row[1], 
                'unique_users': row[2]
            }
        return {'total_clicks': 0, 'active_days': 0, 'unique_users': 0}
    
    async def get_top_performing_links(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get top performing links for a user"""
        cursor = await self.connection.execute(
            """
            SELECT 
                al.short_id,
                al.title,
                al.category,
                COUNT(ct.id) as clicks,
                COUNT(DISTINCT ct.user_id) as unique_users
            FROM affiliate_links al
            LEFT JOIN click_tracking ct ON al.id = ct.link_id
            WHERE al.created_by = ? AND al.is_active = 1
            GROUP BY al.id
            ORDER BY clicks DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        
        rows = await cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    async def cache_niche_analysis(self, query: str, analysis_data: str, ttl_hours: int = 24):
        """Cache niche analysis results"""
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        await self.connection.execute(
            """
            INSERT OR REPLACE INTO niche_analysis_cache 
            (niche_query, analysis_data, expires_at)
            VALUES (?, ?, ?)
            """,
            (query, analysis_data, expires_at)
        )
        await self.connection.commit()
    
    async def get_cached_niche_analysis(self, query: str) -> Optional[str]:
        """Get cached niche analysis if still valid"""
        cursor = await self.connection.execute(
            """
            SELECT analysis_data FROM niche_analysis_cache 
            WHERE niche_query = ? AND expires_at > CURRENT_TIMESTAMP
            """,
            (query,)
        )
        row = await cursor.fetchone()
        return row[0] if row else None
    
    async def get_user_links(self, user_id: int) -> List[Dict]:
        """Get all links created by a user"""
        cursor = await self.connection.execute(
            """
            SELECT 
                short_id, title, category, created_at,
                (SELECT COUNT(*) FROM click_tracking WHERE link_id = affiliate_links.id) as clicks
            FROM affiliate_links 
            WHERE created_by = ? AND is_active = 1
            ORDER BY created_at DESC
            """,
            (user_id,)
        )
        
        rows = await cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    async def close(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            logger.info("Database connection closed")
