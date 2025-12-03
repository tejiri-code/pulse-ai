"""
Bluesky (AT Protocol) publisher
Free alternative to Twitter - no API fees!
"""
import os
import httpx
from typing import Dict, Optional
from datetime import datetime


class BlueskyPublisher:
    """Publisher for Bluesky social network"""
    
    def __init__(self, handle: str = None, app_password: str = None):
        """
        Initialize Bluesky publisher
        
        Args:
            handle: Bluesky handle (e.g., 'username.bsky.social')
            app_password: App password from Bluesky settings
        """
        self.handle = handle or os.getenv("BLUESKY_HANDLE", "")
        self.app_password = app_password or os.getenv("BLUESKY_APP_PASSWORD", "")
        self.base_url = "https://bsky.social/xrpc"
        self.session = None
        self.did = None
    
    async def authenticate(self) -> bool:
        """Authenticate with Bluesky and get session token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/com.atproto.server.createSession",
                    json={
                        "identifier": self.handle,
                        "password": self.app_password
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.session = data["accessJwt"]
                    self.did = data["did"]
                    print(f"✅ Authenticated as {self.handle}")
                    return True
                else:
                    print(f"❌ Auth failed: {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Bluesky auth error: {e}")
            return False
    
    async def post(self, text: str, tags: list = None) -> Optional[Dict]:
        """
        Post to Bluesky
        
        Args:
            text: Post text (300 char limit)
            tags: Optional hashtags
            
        Returns:
            Post data or None
        """
        if not self.session:
            if not await self.authenticate():
                return None
        
        try:
            # Format text with tags
            if tags:
                tag_str = " ".join([f"#{tag}" for tag in tags[:3]])
                text = f"{text}\n\n{tag_str}"
            
            # Truncate if needed
            if len(text) > 300:
                text = text[:297] + "..."
            
            # Create post
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/com.atproto.repo.createRecord",
                    headers={
                        "Authorization": f"Bearer {self.session}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "repo": self.did,
                        "collection": "app.bsky.feed.post",
                        "record": {
                            "text": text,
                            "createdAt": datetime.utcnow().isoformat() + "Z",
                            "$type": "app.bsky.feed.post"
                        }
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Posted to Bluesky!")
                    return data
                else:
                    print(f"❌ Post failed: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Bluesky post error: {e}")
            return None


async def publish_daily_to_bluesky(summaries: list, handle: str = None, app_password: str = None) -> Dict:
    """
    Publish daily AI news to Bluesky
    
    Args:
        summaries: List of news summaries
        handle: Bluesky handle (optional, uses env if not provided)
        app_password: App password (optional)
        
    Returns:
        Publish statistics
    """
    publisher = BlueskyPublisher(handle, app_password)
    
    if not publisher.handle or not publisher.app_password:
        return {
            "success": False,
            "message": "Bluesky credentials not configured",
            "posts_created": 0
        }
    
    posts_created = 0
    
    try:
        # Post top 5 summaries
        for summary in summaries[:5]:
            social_hook = summary.get("social_hook", "")
            tags = summary.get("tags", [])
            
            result = await publisher.post(social_hook, tags[:3])
            if result:
                posts_created += 1
        
        return {
            "success": True,
            "message": f"Posted {posts_created} updates to Bluesky",
            "posts_created": posts_created
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error publishing to Bluesky: {str(e)}",
            "posts_created": posts_created
        }
