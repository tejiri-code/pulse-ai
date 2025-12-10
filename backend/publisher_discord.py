import httpx
import os
import asyncio
from typing import List, Dict
from datetime import datetime

async def publish_to_discord(summary: str, source_url: str = None, title: str = "AI Pulse Update"):
    """Publishes a single rich Embed summary to Discord."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url: return False

    embed = {
        "title": title,
        "description": summary[:4096],
        "color": 5814783, # Blurple
        "footer": {"text": "Pulse AI Bot • Automated Update"},
        "timestamp": datetime.utcnow().isoformat()
    }
    if source_url: embed["url"] = source_url

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(webhook_url, json={"username": "Pulse AI", "embeds": [embed]})
            resp.raise_for_status()
            return True
    except Exception as e:
        print(f"✗ Discord Error: {e}")
        return False

async def post_daily_updates(summaries: List[Dict]) -> Dict:
    """Iterates through summaries and posts them to Discord."""
    count = 0
    for item in summaries:
        title = item.get('title', 'AI Pulse Update')
        content = item.get('three_sentence_summary') or item.get('summary', '')
        url = item.get('source_url') or item.get('url')
        
        if await publish_to_discord(content, url, title):
            count += 1
            await asyncio.sleep(1) # Prevent rate limits
            
    return {"posted_count": count}