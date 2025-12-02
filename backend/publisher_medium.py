"""
Medium publisher module using Medium API
Supports mock mode for testing without API credentials
Posts weekly long-form deep dive reports as DRAFT articles
"""
import os
import json
from typing import Dict, Optional
from datetime import datetime
import httpx

USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "True").lower() == "true"

# Medium API credentials
MEDIUM_INTEGRATION_TOKEN = os.getenv("MEDIUM_INTEGRATION_TOKEN", "")
MEDIUM_USER_ID = os.getenv("MEDIUM_USER_ID", "")


async def get_medium_user_id() -> Optional[str]:
    """
    Get the authenticated user's Medium ID
    
    Returns:
        Medium user ID or None
    """
    if USE_MOCK_MODE or not MEDIUM_INTEGRATION_TOKEN:
        return "mock_user_123"
    
    try:
        url = "https://api.medium.com/v1/me"
        headers = {
            "Authorization": f"Bearer {MEDIUM_INTEGRATION_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("id")
            else:
                print(f"Error getting Medium user ID: {response.status_code}")
                return None
                
    except Exception as e:
        print(f"Error getting Medium user ID: {e}")
        return None


async def post_to_medium(title: str, content: str, tags: list = None) -> Dict:
    """
    Post a long-form article to Medium as a DRAFT
    
    Args:
        title: Article title
        content: Article content (Markdown or HTML)
        tags: List of tags (max 3)
        
    Returns:
        Dictionary with success status and post details
    """
    if USE_MOCK_MODE:
        return post_to_medium_mock(title, content, tags)
    
    if not MEDIUM_INTEGRATION_TOKEN:
        return {
            "success": False,
            "error": "Medium API credentials not configured",
            "mock_mode": False
        }
    
    # Get user ID if not cached
    user_id = MEDIUM_USER_ID or await get_medium_user_id()
    
    if not user_id:
        return {
            "success": False,
            "error": "Could not get Medium user ID",
            "mock_mode": False
        }
    
    try:
        url = f"https://api.medium.com/v1/users/{user_id}/posts"
        
        headers = {
            "Authorization": f"Bearer {MEDIUM_INTEGRATION_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Limit tags to 3 as per Medium API requirements
        if tags:
            tags = tags[:3]
        
        payload = {
            "title": title,
            "contentFormat": "markdown",
            "content": content,
            "tags": tags or [],
            "publishStatus": "draft"  # Always create as draft for review
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                data = response.json()
                post_data = data.get("data", {})
                return {
                    "success": True,
                    "post_id": post_data.get("id"),
                    "post_url": post_data.get("url"),
                    "title": title,
                    "published_at": datetime.utcnow().isoformat(),
                    "status": "draft",
                    "mock_mode": False
                }
            else:
                return {
                    "success": False,
                    "error": f"Medium API error: {response.status_code} - {response.text}",
                    "mock_mode": False
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": f"Error posting to Medium: {str(e)}",
            "mock_mode": False
        }


def post_to_medium_mock(title: str, content: str, tags: list = None) -> Dict:
    """
    Mock Medium posting for testing without API credentials
    
    Args:
        title: Article title
        content: Article content
        tags: List of tags
        
    Returns:
        Mock response
    """
    # Generate a fake post ID and URL
    post_id = f"mock_post_{hash(title) % 1000000}"
    post_url = f"https://medium.com/@mockuser/{post_id}"
    
    print(f"\n{'='*60}")
    print("📝 MOCK MEDIUM POST (DRAFT)")
    print(f"{'='*60}")
    print(f"Title: {title}")
    print(f"Content Length: {len(content)} characters")
    print(f"Tags: {', '.join(tags) if tags else 'None'}")
    print(f"Post ID: {post_id}")
    print(f"Post URL: {post_url}")
    print(f"Status: DRAFT")
    print(f"Created At: {datetime.utcnow().isoformat()}")
    print(f"{'='*60}")
    print(f"\nContent Preview:\n{content[:500]}...")
    print(f"{'='*60}\n")
    
    return {
        "success": True,
        "post_id": post_id,
        "post_url": post_url,
        "title": title,
        "published_at": datetime.utcnow().isoformat(),
        "status": "draft",
        "mock_mode": True
    }


async def post_weekly_report(report: Dict) -> Dict:
    """
    Post a weekly deep dive report to Medium
    
    Args:
        report: Dictionary containing title, content, and tags
        
    Returns:
        Dictionary with posting results
    """
    title = report.get("title", "Weekly AI Deep Dive")
    content = report.get("content", "")
    tags = report.get("tags", ["AI", "Machine Learning", "Technology"])
    
    result = await post_to_medium(title, content, tags)
    
    return {
        "success": result.get("success", False),
        "post_url": result.get("post_url"),
        "post_id": result.get("post_id"),
        "mock_mode": USE_MOCK_MODE,
        "error": result.get("error")
    }
