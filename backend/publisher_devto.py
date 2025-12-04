"""
Dev.to publisher
Free alternative to Medium - developer-focused blogging
"""
import os
import httpx
from typing import Dict, Optional
from datetime import datetime


class DevToPublisher:
    """Publisher for Dev.to platform"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Dev.to publisher
        
        Args:
            api_key: Dev.to API key from settings
        """
        self.api_key = api_key or os.getenv("DEVTO_API_KEY", "")
        self.base_url = "https://dev.to/api"
    
    async def upload_image(self, image_path: str) -> Optional[str]:
        """
        Upload an image to Dev.to
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Image URL or None
        """
        if not self.api_key:
            return None
        
        try:
            with open(image_path, 'rb') as image_file:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"{self.base_url}/images",
                        headers={"api-key": self.api_key},
                        files={"image": image_file}
                    )
                    
                    if response.status_code == 201:
                        data = response.json()
                        print(f"✅ Uploaded image to Dev.to: {data['url']}")
                        return data['url']
                    else:
                        print(f"❌ Image upload failed: {response.text}")
                        return None
        except Exception as e:
            print(f"❌ Image upload error: {e}")
            return None
    
    async def create_article(
        self,
        title: str,
        body: str,
        tags: list = None,
        published: bool = False,
        cover_image: str = None
    ) -> Optional[Dict]:
        """
        Create article on Dev.to
        
        Args:
            title: Article title
            body: Markdown content
            tags: Up to 4 tags
            published: True to publish, False for draft
            cover_image: URL of cover image
            
        Returns:
            Article data or None
        """
        if not self.api_key:
            print("❌ Dev.to API key not configured")
            return None
        
        try:
            # Prepare tags (max 4)
            article_tags = tags[:4] if tags else []
            
            article_data = {
                "title": title,
                "body_markdown": body,
                "published": published,
                "tags": article_tags,
                "description": title[:100]
            }
            
            if cover_image:
                article_data["main_image"] = cover_image
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/articles",
                    headers={
                        "api-key": self.api_key,
                        "Content-Type": "application/json"
                    },
                    json={"article": article_data}
                )
                
                if response.status_code == 201:
                    data = response.json()
                    status = "published" if published else "draft"
                    print(f"✅ Created {status} on Dev.to: {data['url']}")
                    return data
                else:
                    print(f"❌ Dev.to error: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Dev.to publish error: {e}")
            return None


async def publish_weekly_to_devto(summaries: list, api_key: str = None) -> Dict:
    """
    Publish weekly AI news roundup to Dev.to with AI-generated cover image
    
    Args:
        summaries: List of news summaries
        api_key: Dev.to API key (optional)
        
    Returns:
        Publish statistics
    """
    publisher = DevToPublisher(api_key)
    
    if not publisher.api_key:
        return {
            "success": False,
            "message": "Dev.to API key not configured",
            "articles_created": 0
        }
    
    try:
        from image_generator import generate_post_image
        import os
        
        # Generate article content
        date_str = datetime.utcnow().strftime('%B %d, %Y')
        title = f"🤖 AI News Roundup - {date_str}"
        
        # Build markdown body
        body_parts = [
            f"# AI/ML News Highlights for {date_str}\n",
            "Here are the top AI and machine learning stories from this week:\n",
        ]
        
        for i, summary in enumerate(summaries[:15], 1):
            title_text = summary.get("title", "Untitled")
            summary_text = summary.get("three_sentence_summary", "")
            tags = ", ".join(summary.get("tags", [])[:5])
            
            body_parts.append(f"\n## {i}. {title_text}\n")
            body_parts.append(f"{summary_text}\n")
            body_parts.append(f"**Tags**: {tags}\n")
        
        body_parts.append("\n---")
        body_parts.append("\n*Generated by Pulse AI Agent - Your autonomous AI news intelligence system*")
        
        body = "\n".join(body_parts)
        
        # Common AI tags
        tags = ["ai", "machinelearning", "tech", "news"]
        
        # Generate cover image
        cover_image_url = None
        huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        
        if huggingface_token and summaries:
            try:
                # Use the first summary to generate a relevant cover image
                first_summary = summaries[0]
                image_path = await generate_post_image(first_summary, huggingface_token)
                
                if image_path:
                    # Upload image to Dev.to
                    cover_image_url = await publisher.upload_image(image_path)
                    if cover_image_url:
                        print(f"✅ Cover image uploaded: {cover_image_url}")
            except Exception as img_err:
                print(f"⚠️  Cover image generation skipped: {img_err}")
        
        # Create as draft (user can publish manually)
        result = await publisher.create_article(
            title=title,
            body=body,
            tags=tags,
            published=False,  # Draft by default
            cover_image=cover_image_url
        )
        
        if result:
            message = f"Created draft article on Dev.to: {result.get('url')}"
            if cover_image_url:
                message += " (with cover image)"
            
            return {
                "success": True,
                "message": message,
                "articles_created": 1,
                "url": result.get("url")
            }
        else:
            return {
                "success": False,
                "message": "Failed to create Dev.to article",
                "articles_created": 0
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error publishing to Dev.to: {str(e)}",
            "articles_created": 0
        }
