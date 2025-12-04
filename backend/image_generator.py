"""
AI Image Generation using Hugging Face Inference API (Free)
Generates relevant images for social media posts
"""
import os
import httpx
import base64
from typing import Optional
from pathlib import Path


class ImageGenerator:
    """
    Generate AI images using Hugging Face Inference API
    Uses Stable Diffusion (free tier)
    """
    
    def __init__(self, api_token: str = None):
        """
        Initialize image generator
        
        Args:
            api_token: Hugging Face API token (free to get from huggingface.co)
        """
        self.api_token = api_token or os.getenv("HUGGINGFACE_TOKEN", "")
        # Using black-forest-labs/FLUX.1-schnell - free and fast model
        self.model = "black-forest-labs/FLUX.1-schnell"
        # Hugging Face serverless inference endpoint
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        
        # Create images directory if it doesn't exist
        self.images_dir = Path(__file__).parent / "generated_images"
        self.images_dir.mkdir(exist_ok=True)
    
    async def generate_image(
        self,
        prompt: str,
        filename: str = "generated_image.png"
    ) -> Optional[str]:
        """
        Generate an image from a text prompt
        
        Args:
            prompt: Text description of the image
            filename: Name of the output file
            
        Returns:
            Path to the generated image file, or None if failed
        """
        if not self.api_token:
            print("⚠️  Hugging Face API token not configured - skipping image generation")
            return None
        
        try:
            # Enhance prompt for better AI/ML themed images
            enhanced_prompt = f"{prompt}, digital art, high quality, detailed, trending on artstation, vibrant colors"
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    json={"inputs": enhanced_prompt}
                )
                
                if response.status_code == 200:
                    # Save image
                    image_path = self.images_dir / filename
                    image_path.write_bytes(response.content)
                    print(f"✅ Generated image: {image_path}")
                    return str(image_path)
                else:
                    print(f"❌ Image generation failed: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Image generation error: {e}")
            return None
    
    def create_prompt_from_summary(self, summary: dict) -> str:
        """
        Create an image generation prompt from a news summary
        
        Args:
            summary: News summary dict with title, summary, and tags
            
        Returns:
            Image generation prompt
        """
        # Extract key themes from tags
        tags = summary.get("tags", [])
        title = summary.get("title", "")
        
        # Common AI/ML keywords to emphasize
        ai_keywords = ["ai", "ml", "neural", "deep learning", "machine learning", 
                       "llm", "gpt", "model", "training", "data"]
        
        # Check if this is AI/ML related
        is_ai_topic = any(keyword in " ".join(tags).lower() or keyword in title.lower() 
                         for keyword in ai_keywords)
        
        if is_ai_topic:
            # Create AI-themed visual
            base_prompts = [
                "futuristic AI neural network visualization",
                "abstract machine learning concept with glowing nodes",
                "digital brain with neural pathways and data streams",
                "modern AI technology dashboard with holographic displays",
                "cyberpunk AI laboratory with floating code and algorithms"
            ]
            
            # Pick based on tags
            if "neural" in " ".join(tags).lower():
                return "abstract neural network with glowing connections, digital art, cyberpunk, blue and purple gradient"
            elif "llm" in " ".join(tags).lower() or "gpt" in " ".join(tags).lower():
                return "AI language model visualization, flowing text and data, futuristic interface, neon colors"
            elif "vision" in " ".join(tags).lower() or "image" in " ".join(tags).lower():
                return "computer vision AI, digital eye scanning images, holographic display, tech aesthetic"
            else:
                return base_prompts[0]
        else:
            # Generic tech image
            return "modern technology concept, digital innovation, abstract tech background, professional"


async def generate_post_image(summary: dict, api_token: str = None) -> Optional[str]:
    """
    Convenience function to generate an image for a social media post
    
    Args:
        summary: News summary dict
        api_token: Hugging Face API token
        
    Returns:
        Path to generated image or None
    """
    generator = ImageGenerator(api_token)
    prompt = generator.create_prompt_from_summary(summary)
    
    # Create unique filename based on summary
    import hashlib
    summary_text = summary.get("three_sentence_summary", "")[:100]
    filename = f"post_{hashlib.md5(summary_text.encode()).hexdigest()[:8]}.png"
    
    return await generator.generate_image(prompt, filename)
