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
    
    async def upload_media(self, image_path: str) -> Optional[str]:
        """
        Upload an image to Mastodon
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Media ID or None
        """
        if not self.access_token:
            return None
        
        try:
            with open(image_path, 'rb') as image_file:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"{self.instance}/api/v2/media",
                        headers={"Authorization": f"Bearer {self.access_token}"},
                        files={"file": image_file}
                    )
                    
                    if response.status_code in [200, 202]:
                        data = response.json()
                        print(f"✅ Uploaded image to Mastodon: {data['id']}")
                        return data['id']
                    else:
                        print(f"❌ Image upload failed: {response.text}")
                        return None
        except Exception as e:
            print(f"❌ Image upload error: {e}")
            return None
    
    async def create_status(
        self,
        text: str,
        media_ids: list = None,
        visibility: str = "public"
    ) -> Optional[Dict]:
        """
        Post a status (toot) to Mastodon
        
        Args:
            text: Status text (max 500 characters)
            media_ids: List of media IDs to attach
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
            
            payload = {
                "status": text,
                "visibility": visibility
            }
            
            if media_ids:
                payload["media_ids"] = media_ids
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.instance}/api/v1/statuses",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    },
                    json=payload
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
    Publish daily AI news updates to Mastodon with AI-generated images
    
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
        from image_generator import generate_post_image
        import os
        
        posts_created = 0
        huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        
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
            
            # Generate image for this post
            media_ids = []
            if huggingface_token:
                try:
                    image_path = await generate_post_image(summary, huggingface_token)
                    if image_path:
                        # Upload image to Mastodon
                        media_id = await publisher.upload_media(image_path)
                        if media_id:
                            media_ids.append(media_id)
                except Exception as img_err:
                    print(f"⚠️  Image generation skipped: {img_err}")
            
            # Post to Mastodon with or without image
            result = await publisher.create_status(toot_text, media_ids=media_ids if media_ids else None)
            
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
