"""
X (Twitter) publisher module using Twitter API v2
Supports mock mode for testing without API credentials
"""
import os
import json
from typing import Dict, Optional
from datetime import datetime
import httpx

USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "True").lower() == "true"

# Twitter API v2 credentials
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET", "")


async def post_to_twitter(tweet_text: str) -> Dict:
    """
    Post a tweet to Twitter using API v2
    
    Args:
        tweet_text: Text to tweet (max 280 characters)
        
    Returns:
        Dictionary with success status and tweet details
    """
    if USE_MOCK_MODE:
        return post_to_twitter_mock(tweet_text)
    
    if not TWITTER_BEARER_TOKEN:
        return {
            "success": False,
            "error": "Twitter API credentials not configured",
            "mock_mode": False
        }
    
    # Truncate tweet if too long
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
    
    try:
        url = "https://api.twitter.com/2/tweets"
        
        headers = {
            "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": tweet_text
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "success": True,
                    "tweet_id": data.get("data", {}).get("id"),
                    "tweet_text": tweet_text,
                    "posted_at": datetime.utcnow().isoformat(),
                    "mock_mode": False
                }
            else:
                return {
                    "success": False,
                    "error": f"Twitter API error: {response.status_code} - {response.text}",
                    "mock_mode": False
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": f"Error posting to Twitter: {str(e)}",
            "mock_mode": False
        }


def post_to_twitter_mock(tweet_text: str) -> Dict:
    """
    Mock Twitter posting for testing without API credentials
    
    Args:
        tweet_text: Text to tweet
        
    Returns:
        Mock response
    """
    # Truncate tweet if too long
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
    
    # Generate a fake tweet ID
    tweet_id = f"mock_tweet_{hash(tweet_text) % 1000000}"
    
    print(f"\n{'='*60}")
    print("🐦 MOCK TWITTER POST")
    print(f"{'='*60}")
    print(f"Tweet Text: {tweet_text}")
    print(f"Tweet ID: {tweet_id}")
    print(f"Posted At: {datetime.utcnow().isoformat()}")
    print(f"{'='*60}\n")
    
    return {
        "success": True,
        "tweet_id": tweet_id,
        "tweet_text": tweet_text,
        "posted_at": datetime.utcnow().isoformat(),
        "mock_mode": True
    }


async def post_daily_updates(summaries: list) -> Dict:
    """
    Post daily AI news updates to Twitter
    
    Args:
        summaries: List of summary dictionaries with social_hook
        
    Returns:
        Dictionary with posting results
    """
    results = {
        "success": True,
        "posts_created": 0,
        "posts_failed": 0,
        "mock_mode": USE_MOCK_MODE,
        "posts": []
    }
    
    for summary in summaries[:5]:  # Limit to 5 posts per day to avoid spam
        tweet_text = summary.get("social_hook", "")
        
        if not tweet_text:
            continue
        
        result = await post_to_twitter(tweet_text)
        
        if result.get("success"):
            results["posts_created"] += 1
        else:
            results["posts_failed"] += 1
        
        results["posts"].append(result)
    
    if results["posts_failed"] > 0:
        results["success"] = False
    
    return results
