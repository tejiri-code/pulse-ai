"""
Mastodon publisher
Free, open-source microblogging platform with excellent API
"""
import os
import httpx
from typing import Dict, Optional
from datetime import datetime


class MastodonPublisher:
    """Publisher for Mastodon platform"""
    
    def __init__(self, access_token: str = None, instance: str = None):
        """
        Initialize Mastodon publisher
        
        Args:
            access_token: Mastodon API access token
            instance: Mastodon instance URL (e.g., https://mastodon.social)
        """
        self.access_token = access_token or os.getenv("MASTODON_ACCESS_TOKEN", "")
        self.instance = instance or os.getenv("MASTODON_INSTANCE", "https://mastodon.social")
        # Remove trailing slash if present
        self.instance = self.instance.rstrip('/')
    
    async def create_status(
        self,
        text: str,
        visibility: str = "public"
    ) -> Optional[Dict]:
        """
        Post a status (toot) to Mastodon
        
        Args:
            text: Status text (max 500 characters)
            visibility: "public", "unlisted", "private", or "direct"
            
        Returns:
            Status data or None
        """
        if not self.access_token:
            print("❌ Mastodon access token not configured")
            return None
        
        try:
            # Mastodon allows 500 characters
            if len(text) > 500:
                text = text[:497] + "..."
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.instance}/api/v1/statuses",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "status": text,
                        "visibility": visibility
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Posted to Mastodon: {data['url']}")
                    return data
                else:
                    print(f"❌ Mastodon error: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Mastodon publish error: {e}")
            return None


async def publish_daily_to_mastodon(summaries: list, access_token: str = None, instance: str = None) -> Dict:
    """
    Publish daily AI news updates to Mastodon
    
    Args:
        summaries: List of news summaries
        access_token: Mastodon API access token (optional)
        instance: Mastodon instance URL (optional)
        
    Returns:
        Publish statistics
    """
    publisher = MastodonPublisher(access_token, instance)
    
    if not publisher.access_token:
        return {
            "success": False,
            "message": "Mastodon access token not configured",
            "posts_created": 0
        }
    
    try:
        posts_created = 0
        
        # Select top summaries (max 5 per day to avoid spam)
        top_summaries = summaries[:5]
        
        for summary in top_summaries:
            # Get summary data
            summary_text = summary.get("three_sentence_summary", "")
            social_hook = summary.get("social_hook", "")
            tags = summary.get("tags", [])
            
            # Format hashtags (max 4)
            hashtags = " ".join([f"#{tag.replace(' ', '')}" for tag in tags[:4]])
            
            # Build toot text (max 500 chars)
            toot_parts = []
            
            if social_hook:
                toot_parts.append(social_hook)
                toot_parts.append("\n")
            
            # Calculate remaining space for summary
            base_length = len("\n".join(toot_parts)) + len("\n" + hashtags)
            remaining_chars = 500 - base_length - 10  # 10 char buffer
            
            # Smart truncation: break at word boundary
            if len(summary_text) > remaining_chars:
                # Find the last space before the limit
                truncated = summary_text[:remaining_chars]
                last_space = truncated.rfind(' ')
                if last_space > 0:
                    summary_text = truncated[:last_space] + "..."
                else:
                    summary_text = truncated + "..."
            
            toot_parts.append(summary_text)
            toot_parts.append("\n")
            toot_parts.append(hashtags)
            
            toot_text = "\n".join(toot_parts)
            
            # Post to Mastodon
            result = await publisher.create_status(toot_text)
            
            if result:
                posts_created += 1
        
        return {
            "success": posts_created > 0,
            "message": f"Posted {posts_created} updates to Mastodon",
            "posts_created": posts_created
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error publishing to Mastodon: {str(e)}",
            "posts_created": 0
        }
