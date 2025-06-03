"""
Affiliate Service for link management, tracking, and analytics
"""

import asyncio
import hashlib
import secrets
import string
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs
import logging

from bot.core.database import Database

logger = logging.getLogger(__name__)

class AffiliateService:
    def __init__(self, database: Database):
        self.db = database
        self.base_domain = "your-domain.com"  # This should be configurable
        
        logger.info("✅ Affiliate service initialized")
    
    def generate_short_id(self, length: int = 8) -> str:
        """Generate a unique short ID for affiliate links"""
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    async def create_affiliate_link(self, original_url: str, affiliate_url: str, 
                                  title: str, description: str, category: str, 
                                  created_by: int) -> Tuple[str, int]:
        """Create a new tracked affiliate link"""
        # Generate unique short ID
        short_id = self.generate_short_id()
        
        # Ensure uniqueness
        while await self.db.get_affiliate_link(short_id):
            short_id = self.generate_short_id()
        
        # Create the link in database
        link_id = await self.db.create_affiliate_link(
            short_id=short_id,
            original_url=original_url,
            affiliate_url=affiliate_url,
            title=title,
            description=description,
            category=category,
            created_by=created_by
        )
        
        logger.info(f"Created affiliate link: {short_id} for user {created_by}")
        return short_id, link_id
    
    def get_tracking_url(self, short_id: str) -> str:
        """Get the full tracking URL for a short ID"""
        return f"https://{self.base_domain}/track/{short_id}"
    
    async def track_click(self, short_id: str, user_id: Optional[int] = None,
                         ip_address: Optional[str] = None, user_agent: Optional[str] = None,
                         referrer: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Track a click and return success status and redirect URL"""
        # Get the affiliate link
        link_data = await self.db.get_affiliate_link(short_id)
        
        if not link_data:
            return False, None
        
        # Track the click
        await self.db.track_click(
            link_id=link_data['id'],
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer
        )
        
        logger.info(f"Tracked click for link {short_id} from user {user_id}")
        return True, link_data['affiliate_url']
    
    async def get_link_analytics(self, short_id: str, user_id: int) -> Optional[Dict]:
        """Get analytics for a specific link"""
        link_data = await self.db.get_affiliate_link(short_id)
        
        if not link_data or link_data['created_by'] != user_id:
            return None
        
        # Get click statistics
        stats = await self.db.get_click_stats(link_data['id'])
        
        return {
            'link_info': link_data,
            'stats': stats,
            'tracking_url': self.get_tracking_url(short_id)
        }
    
    async def get_user_dashboard(self, user_id: int) -> Dict:
        """Get comprehensive dashboard data for a user"""
        # Get user's links
        user_links = await self.db.get_user_links(user_id)
        
        # Get top performing links
        top_links = await self.db.get_top_performing_links(user_id, limit=5)
        
        # Calculate totals
        total_links = len(user_links)
        total_clicks = sum(link.get('clicks', 0) for link in user_links)
        
        return {
            'total_links': total_links,
            'total_clicks': total_clicks,
            'recent_links': user_links[:10],  # Most recent 10
            'top_performing': top_links,
            'average_clicks_per_link': total_clicks / total_links if total_links > 0 else 0
        }
    
    def extract_affiliate_info(self, url: str) -> Dict:
        """Extract affiliate information from URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Common affiliate patterns
        affiliate_patterns = {
            'amazon.com': self._extract_amazon_info,
            'amazon.': self._extract_amazon_info,  # For international domains
            'clickbank.net': self._extract_clickbank_info,
            'shareasale.com': self._extract_shareasale_info,
            'cj.com': self._extract_cj_info,
            'commission-junction.com': self._extract_cj_info,
        }
        
        # Check for known affiliate networks
        for pattern, extractor in affiliate_patterns.items():
            if pattern in domain:
                return extractor(url, parsed)
        
        # Generic affiliate detection
        return self._extract_generic_info(url, parsed)
    
    def _extract_amazon_info(self, url: str, parsed) -> Dict:
        """Extract Amazon affiliate information"""
        params = parse_qs(parsed.query)
        
        return {
            'network': 'Amazon Associates',
            'affiliate_id': params.get('tag', ['Unknown'])[0],
            'product_id': self._extract_amazon_asin(url),
            'commission_rate': '1-10%',
            'network_type': 'merchant'
        }
    
    def _extract_amazon_asin(self, url: str) -> str:
        """Extract ASIN from Amazon URL"""
        import re
        asin_patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'asin=([A-Z0-9]{10})',
        ]
        
        for pattern in asin_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return 'Unknown'
    
    def _extract_clickbank_info(self, url: str, parsed) -> Dict:
        """Extract ClickBank affiliate information"""
        # ClickBank URLs often have affiliate ID in the path
        path_parts = parsed.path.split('/')
        affiliate_id = path_parts[1] if len(path_parts) > 1 else 'Unknown'
        
        return {
            'network': 'ClickBank',
            'affiliate_id': affiliate_id,
            'commission_rate': '10-75%',
            'network_type': 'digital_products'
        }
    
    def _extract_shareasale_info(self, url: str, parsed) -> Dict:
        """Extract ShareASale affiliate information"""
        params = parse_qs(parsed.query)
        
        return {
            'network': 'ShareASale',
            'affiliate_id': params.get('afftrack', ['Unknown'])[0],
            'merchant_id': params.get('merchantid', ['Unknown'])[0],
            'commission_rate': '5-30%',
            'network_type': 'network'
        }
    
    def _extract_cj_info(self, url: str, parsed) -> Dict:
        """Extract Commission Junction (CJ) affiliate information"""
        params = parse_qs(parsed.query)
        
        return {
            'network': 'Commission Junction',
            'affiliate_id': params.get('PID', ['Unknown'])[0],
            'commission_rate': '2-20%',
            'network_type': 'network'
        }
    
    def _extract_generic_info(self, url: str, parsed) -> Dict:
        """Extract generic affiliate information"""
        params = parse_qs(parsed.query)
        
        # Look for common affiliate parameters
        affiliate_params = ['ref', 'affiliate', 'aff', 'partner', 'source', 'utm_source']
        affiliate_id = 'Unknown'
        
        for param in affiliate_params:
            if param in params:
                affiliate_id = params[param][0]
                break
        
        return {
            'network': 'Unknown/Custom',
            'affiliate_id': affiliate_id,
            'domain': parsed.netloc,
            'commission_rate': 'Unknown',
            'network_type': 'unknown'
        }
    
    def validate_affiliate_url(self, url: str) -> Tuple[bool, str]:
        """Validate if URL appears to be an affiliate link"""
        try:
            parsed = urlparse(url)
            
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL format"
            
            # Check for common affiliate indicators
            affiliate_indicators = [
                'tag=', 'ref=', 'affiliate=', 'aff=', 'partner=',
                'clickbank.net', 'shareasale.com', 'cj.com',
                'amazon.', 'amzn.to'
            ]
            
            for indicator in affiliate_indicators:
                if indicator in url.lower():
                    return True, "Valid affiliate URL detected"
            
            return True, "URL accepted (affiliate status unclear)"
            
        except Exception as e:
            return False, f"URL validation error: {str(e)}"
