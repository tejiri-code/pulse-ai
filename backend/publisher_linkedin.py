"""
LinkedIn publisher
Free API for professional sharing
"""
import os
import httpx
from typing import Dict, Optional


class LinkedInPublisher:
    """Publisher for LinkedIn"""
    
    def __init__(self, access_token: str = None):
        """
        Initialize LinkedIn publisher
        
        Args:
            access_token: LinkedIn access token
        """
        self.access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN", "")
        self.base_url = "https://api.linkedin.com/v2"
    
    async def share_update(self, text: str, url: str = None) -> Optional[Dict]:
        """
        Share an update on LinkedIn
        
        Args:
            text: Post text (up to 3000 characters)
            url: Optional link to share
            
        Returns:
            Share data or None
        """
        if not self.access_token:
            print("❌ LinkedIn access token not configured")
            return None
        
        try:
            # Get user's profile URN first
            async with httpx.AsyncClient() as client:
                # Get user info
                me_response = await client.get(
                    f"{self.base_url}/me",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "X-Restli-Protocol-Version": "2.0.0"
                    }
                )
                
                if me_response.status_code != 200:
                    print(f"❌ LinkedIn auth failed: {me_response.text}")
                    return None
                
                user_id = me_response.json()["id"]
                author_urn = f"urn:li:person:{user_id}"
                
                # Create share payload
                share_payload = {
                    "author": author_urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": text[:300]  # LinkedIn limit
                            },
                            "shareMediaCategory": "ARTICLE" if url else "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                    }
                }
                
                # Add URL if provided
                if url:
                    share_payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [{
                        "status": "READY",
                        "originalUrl": url
                    }]
                
                # Post update
                share_response = await client.post(
                    f"{self.base_url}/ugcPosts",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json",
                        "X-Restli-Protocol-Version": "2.0.0"
                    },
                    json=share_payload
                )
                
                if share_response.status_code in [200, 201]:
                    print(f"✅ Posted to LinkedIn!")
                    return share_response.json()
                else:
                    print(f"❌ LinkedIn post failed: {share_response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ LinkedIn publish error: {e}")
            return None


async def publish_to_linkedin(summaries: list, access_token: str = None) -> Dict:
    """
    Publish AI news to LinkedIn
    
    Args:
        summaries: List of news summaries
        access_token: LinkedIn access token (optional)
        
    Returns:
        Publish statistics
    """
    publisher = LinkedInPublisher(access_token)
    
    if not publisher.access_token:
        return {
            "success": False,
            "message": "LinkedIn access token not configured",
            "posts_created": 0
        }
    
    posts_created = 0
    
    try:
        # Post top 3 summaries to LinkedIn
        for summary in summaries[:3]:
            social_hook = summary.get("social_hook", "")
            
            result = await publisher.share_update(social_hook)
            if result:
                posts_created += 1
        
        return {
            "success": True,
            "message": f"Posted {posts_created} updates to LinkedIn",
            "posts_created": posts_created
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error publishing to LinkedIn: {str(e)}",
            "posts_created": posts_created
        }
