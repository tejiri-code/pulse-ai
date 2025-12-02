"""
Autonomous agent for AI news processing pipeline
Simple async pipeline: scrape → dedupe → summarize → publish
"""
import os
from typing import List, Dict
from datetime import datetime


from scraper import scrape_all_sources
from dedupe import deduplicate_items, generate_embedding
from summaries import generate_summary, batch_summarize
from publisher_x import post_to_twitter, post_daily_updates
from publisher_medium import post_to_medium, post_weekly_report

USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "True").lower() == "true"


async def run_agent(
    publish_to_x: bool = False,
    publish_to_medium: bool = False
) -> Dict:
    """
    Run the complete agent pipeline
    
    Args:
        publish_to_x: Whether to publish daily updates to X
        publish_to_medium: Whether to publish weekly report to Medium
        
    Returns:
        Final state dictionary
    """
    print("\n" + "="*60)
    print("🤖 PULSE AI AGENT - Starting Pipeline")
    print("="*60 + "\n")
    
    state = {
        "raw_items": [],
        "unique_items": [],
        "duplicate_items": [],
        "summaries": [],
        "daily_posts": [],
        "weekly_report": {},
        "errors": [],
        "step": "initialized"
    }
    
    # Step 1: Scrape
    print("🔍 Step 1: Scraping news from all sources...")
    try:
        raw_items = await scrape_all_sources()
        state["raw_items"] = raw_items
        state["step"] = "scrape_complete"
        print(f"✅ Scraped {len(raw_items)} items")
    except Exception as e:
        state["errors"].append(f"Scraping error: {str(e)}")
        print(f"❌ Scraping error: {e}")
    
    # Step 2: Deduplicate
    print("🔄 Step 2: Deduplicating items...")
    try:
        raw_items = state.get("raw_items", [])
        unique_items, duplicate_items = deduplicate_items(raw_items, existing_items=[])
        
        state["unique_items"] = unique_items
        state["duplicate_items"] = duplicate_items
        state["step"] = "dedupe_complete"
        
        print(f"✅ Found {len(unique_items)} unique items, {len(duplicate_items)} duplicates")
        
        # Log novelty scores
        for item in unique_items[:3]:
            print(f"   📊 {item['title'][:50]}... | Novelty: {item.get('novelty_score', 0):.2f}")
            
    except Exception as e:
        state["errors"].append(f"Deduplication error: {str(e)}")
        print(f"❌ Deduplication error: {e}")
    
    # Step 3: Summarize
    print("📝 Step 3: Generating summaries...")
    try:
        unique_items = state.get("unique_items", [])
        summaries = batch_summarize(unique_items)
        
        state["summaries"] = summaries
        state["step"] = "summarize_complete"
        
        print(f"✅ Generated {len(summaries)} summaries")
        
        # Log sample summary
        if summaries:
            sample = summaries[0]
            print(f"\n   Sample Summary:")
            print(f"   📰 {sample.get('three_sentence_summary', '')[:100]}...")
            print(f"   🐦 {sample.get('social_hook', '')[:80]}...")
            
    except Exception as e:
        state["errors"].append(f"Summarization error: {str(e)}")
        print(f"❌ Summarization error: {e}")
    
    # Step 4: Publish to X (optional)
    if publish_to_x:
        print("🐦 Step 4: Publishing to X (Twitter)...")
        try:
            summaries = state.get("summaries", [])
            result = await post_daily_updates(summaries)
            
            state["daily_posts"] = result.get("posts", [])
            state["step"] = "publish_x_complete"
            
            mode_str = "(MOCK MODE)" if result.get("mock_mode") else "(LIVE)"
            print(f"✅ Posted {result.get('posts_created')} tweets to X {mode_str}")
            
        except Exception as e:
            state["errors"].append(f"X publishing error: {str(e)}")
            print(f"❌ X publishing error: {e}")
    else:
        print("⏭️  Step 4: Skipping X publishing (not requested)")
        state["step"] = "publish_x_skipped"
    
    # Step 5: Publish to Medium (optional)
    if publish_to_medium:
        print("📝 Step 5: Publishing to Medium...")
        try:
            # Generate weekly report from summaries
            summaries = state.get("summaries", [])
            report = generate_weekly_report(summaries)
            
            result = await post_weekly_report(report)
            
            state["weekly_report"] = result
            state["step"] = "publish_medium_complete"
            
            mode_str = "(MOCK MODE)" if result.get("mock_mode") else "(LIVE)"
            print(f"✅ Published weekly report to Medium {mode_str}")
            
            if result.get("post_url"):
                print(f"   📎 URL: {result['post_url']}")
                
        except Exception as e:
            state["errors"].append(f"Medium publishing error: {str(e)}")
            print(f"❌ Medium publishing error: {e}")
    else:
        print("⏭️  Step 5: Skipping Medium publishing (not requested)")
        state["step"] = "publish_medium_skipped"
    
    print("\n" + "="*60)
    print("✅ PULSE AI AGENT - Pipeline Complete")
    print("="*60)
    print(f"📊 Results:")
    print(f"   • Scraped: {len(state.get('raw_items', []))} items")
    print(f"   • Unique: {len(state.get('unique_items', []))} items")
    print(f"   • Summaries: {len(state.get('summaries', []))}")
    print(f"   • X Posts: {len(state.get('daily_posts', []))}")
    print(f"   • Errors: {len(state.get('errors', []))}")
    
    if state.get("errors"):
        print(f"\n⚠️  Errors encountered:")
        for error in state["errors"]:
            print(f"   - {error}")
    
    print("="*60 + "\n")
    
    return state


def generate_weekly_report(summaries: List[Dict]) -> Dict:
    """
    Generate a long-form weekly report from summaries
    
    Args:
        summaries: List of summaries from the week
        
    Returns:
        Report dictionary with title, content, and tags
    """
    week_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Create markdown content
    content = f"""# Weekly AI Deep Dive: {week_start.strftime('%B %d, %Y')}

## Overview

This week in AI/ML has been exceptionally dynamic, with major breakthroughs across multiple domains. From advances in multimodal models to improvements in open-source LLMs, the field continues to evolve at a rapid pace.

## Key Developments

"""
    
    for i, summary in enumerate(summaries[:10], 1):
        title = summary.get('title', 'Untitled') if isinstance(summary, dict) else 'Untitled'
        three_sent = summary.get('three_sentence_summary', '') if isinstance(summary, dict) else ''
        tags = summary.get('tags', []) if isinstance(summary, dict) else []
        
        content += f"""
###  {i}. {title}

{three_sent}

**Tags:** {', '.join(tags)}

---
"""
    
    content += """
## Looking Ahead

The developments this week point to several emerging trends:

1. **Multimodal AI** continues to mature, with better integration of vision and language understanding
2. **Open-source models** are closing the gap with proprietary solutions
3. **Agent frameworks** enable more sophisticated autonomous systems
4. **Safety and alignment** remain critical areas of focus

Stay tuned for next week's deep dive!

---

*This report was generated by Pulse, an autonomous AI news intelligence agent.*
"""
    
    title = f"Weekly AI Deep Dive: {week_start.strftime('%B %d, %Y')}"
    tags = ["Artificial Intelligence", "Machine Learning", "Technology"]
    
    return {
        "title": title,
        "content": content,
        "tags": tags
    }
