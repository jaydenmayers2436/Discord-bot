#!/usr/bin/env python3
"""
Click Tracking Web Server
Handles affiliate link redirects and click tracking
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import asyncio
import logging
from contextlib import asynccontextmanager

from bot.core.database import Database
from bot.services.affiliate_service import AffiliateService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for services
database = None
affiliate_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global database, affiliate_service
    
    # Startup
    logger.info("Starting click tracking server...")
    database = Database()
    await database.initialize()
    affiliate_service = AffiliateService(database)
    logger.info("✅ Click tracking server ready")
    
    yield
    
    # Shutdown
    logger.info("Shutting down click tracking server...")
    if database:
        await database.close()
    logger.info("✅ Click tracking server stopped")

app = FastAPI(
    title="Affiliate Click Tracker",
    description="Tracks clicks on affiliate links and redirects users",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Affiliate Click Tracking Server",
        "status": "active",
        "endpoints": {
            "track": "/track/{short_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

@app.get("/track/{short_id}")
async def track_click(short_id: str, request: Request):
    """
    Track click and redirect to affiliate URL
    """
    try:
        # Get client information
        user_agent = request.headers.get("user-agent", "Unknown")
        referrer = request.headers.get("referer", "Direct")
        
        # Get client IP (handling potential proxies)
        client_ip = request.headers.get("x-forwarded-for")
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "Unknown"
        
        # Track the click
        success, redirect_url = await affiliate_service.track_click(
            short_id=short_id,
            user_id=None,  # Web clicks don't have Discord user ID
            ip_address=client_ip,
            user_agent=user_agent,
            referrer=referrer
        )
        
        if not success:
            logger.warning(f"Click tracking failed for {short_id} from {client_ip}")
            raise HTTPException(status_code=404, detail="Link not found")
        
        logger.info(f"Tracked click: {short_id} from {client_ip}")
        
        # Redirect to affiliate URL
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except Exception as e:
        logger.error(f"Error tracking click for {short_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stats/{short_id}")
async def get_link_stats(short_id: str):
    """
    Get public stats for a link (basic info only)
    """
    try:
        link_data = await database.get_affiliate_link(short_id)
        
        if not link_data:
            raise HTTPException(status_code=404, detail="Link not found")
        
        stats = await database.get_click_stats(link_data['id'])
        
        return {
            "short_id": short_id,
            "title": link_data['title'],
            "category": link_data['category'],
            "total_clicks": stats['total_clicks'],
            "active_days": stats['active_days'],
            "created_at": link_data['created_at']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats for {short_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "click_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
