"""
Autonomous agent for AI news processing pipeline using LangGraph
Implements a state graph: scrape → dedupe → summarize → publish
"""
import os
from typing import List, Dict, TypedDict, Annotated
from datetime import datetime
import operator

from langgraph.graph import StateGraph, END

from scraper import scrape_all_sources
from dedupe import deduplicate_items
from summaries import batch_summarize
from publisher_x import post_daily_updates
from publisher_medium import post_weekly_report
from publisher_discord import post_daily_updates as post_discord

# Importing the newly added reddit scraping code
from scraper_reddit import get_reddit_headlines

USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "True").lower() == "true"


# Define the agent state using TypedDict
class AgentState(TypedDict):
    """State that flows through the LangGraph pipeline"""
    raw_items: List[Dict]
    unique_items: List[Dict]
    duplicate_items: List[Dict]
    summaries: List[Dict]
    daily_posts: List[Dict]
    weekly_report: Dict
    errors: Annotated[List[str], operator.add]
    step: str
    publish_to_x: bool
    publish_to_medium: bool
    publish_to_discord: bool


# ============================================
# LANGGRAPH NODE DEFINITIONS
# ============================================

async def scrape_node(state: AgentState) -> AgentState:
    """
    Node 1: Scrape AI/ML news from all sources
    """
    print("\n🔍 [LangGraph Node] SCRAPE: Fetching news from sources...")
    
    try:
        raw_items = await scrape_all_sources()
        print(f"   ✅ Scraped {len(raw_items)} items")
        
        return {
            **state,
            "raw_items": raw_items,
            "step": "scrape_complete"
        }
    except Exception as e:
        print(f"   ❌ Scraping error: {e}")
        return {
            **state,
            "errors": [f"Scraping error: {str(e)}"],
            "step": "scrape_failed"
        }


async def dedupe_node(state: AgentState) -> AgentState:
    """
    Node 2: Deduplicate items using embedding similarity
    """
    print("\n🔄 [LangGraph Node] DEDUPE: Removing duplicates...")
    
    try:
        raw_items = state.get("raw_items", [])
        unique_items, duplicate_items = deduplicate_items(raw_items, existing_items=[])
        
        print(f"   ✅ Found {len(unique_items)} unique, {len(duplicate_items)} duplicates")
        
        # Log novelty scores for top items
        for item in unique_items[:3]:
            print(f"   📊 {item['title'][:50]}... | Novelty: {item.get('novelty_score', 0):.2f}")
        
        return {
            **state,
            "unique_items": unique_items,
            "duplicate_items": duplicate_items,
            "step": "dedupe_complete"
        }
    except Exception as e:
        print(f"   ❌ Deduplication error: {e}")
        return {
            **state,
            "errors": [f"Deduplication error: {str(e)}"],
            "step": "dedupe_failed"
        }


async def summarize_node(state: AgentState) -> AgentState:
    """
    Node 3: Generate LLM-powered summaries using Groq
    """
    print("\n📝 [LangGraph Node] SUMMARIZE: Generating AI summaries...")
    
    try:
        unique_items = state.get("unique_items", [])
        summaries = batch_summarize(unique_items)
        
        print(f"   ✅ Generated {len(summaries)} summaries")
        
        # Log sample summary
        if summaries:
            sample = summaries[0]
            print(f"\n   Sample Summary:")
            print(f"   📰 {sample.get('three_sentence_summary', '')[:100]}...")
            print(f"   🐦 {sample.get('social_hook', '')[:80]}...")
        
        return {
            **state,
            "summaries": summaries,
            "step": "summarize_complete"
        }
    except Exception as e:
        print(f"   ❌ Summarization error: {e}")
        return {
            **state,
            "errors": [f"Summarization error: {str(e)}"],
            "step": "summarize_failed"
        }


async def publish_x_node(state: AgentState) -> AgentState:
    """
    Node 4a: Publish to X (Twitter) - conditional
    """
    if not state.get("publish_to_x", False):
        print("\n⏭️  [LangGraph Node] PUBLISH_X: Skipped (not requested)")
        return {**state, "step": "publish_x_skipped"}
    
    print("\n🐦 [LangGraph Node] PUBLISH_X: Posting to Twitter...")
    
    try:
        summaries = state.get("summaries", [])
        result = await post_daily_updates(summaries)
        
        mode_str = "(MOCK MODE)" if result.get("mock_mode") else "(LIVE)"
        print(f"   ✅ Posted {result.get('posts_created')} tweets {mode_str}")
        
        return {
            **state,
            "daily_posts": result.get("posts", []),
            "step": "publish_x_complete"
        }
    except Exception as e:
        print(f"   ❌ X publishing error: {e}")
        return {
            **state,
            "errors": [f"X publishing error: {str(e)}"],
            "step": "publish_x_failed"
        }


async def publish_discord_node(state: AgentState) -> AgentState:
    """
    Node 4b: Publish to Discord - conditional
    """
    if not state.get("publish_to_discord", False):
        print("\n⏭️  [LangGraph Node] PUBLISH_DISCORD: Skipped (not requested)")
        return {**state, "step": "publish_discord_skipped"}
    
    print("\n💬 [LangGraph Node] PUBLISH_DISCORD: Posting to Discord...")
    
    try:
        # Pass the list of summaries to the batch poster
        result = await post_discord(state.get("summaries", []))
        
        print(f"   ✅ Posted {result.get('posted_count', 0)} updates to Discord")
        
        return {
            **state,
            "step": "publish_discord_complete"
        }
    except Exception as e:
        print(f"   ❌ Discord publishing error: {e}")
        return {
            **state,
            "errors": [f"Discord publishing error: {str(e)}"],
            "step": "publish_discord_failed"
        }


async def publish_medium_node(state: AgentState) -> AgentState:
    """
    Node 4c: Publish to Medium - conditional
    """
    if not state.get("publish_to_medium", False):
        print("\n⏭️  [LangGraph Node] PUBLISH_MEDIUM: Skipped (not requested)")
        return {**state, "step": "publish_medium_skipped"}
    
    print("\n📝 [LangGraph Node] PUBLISH_MEDIUM: Publishing to Medium...")
    
    try:
        summaries = state.get("summaries", [])
        report = generate_weekly_report(summaries)
        result = await post_weekly_report(report)
        
        mode_str = "(MOCK MODE)" if result.get("mock_mode") else "(LIVE)"
        print(f"   ✅ Published weekly report {mode_str}")
        
        if result.get("post_url"):
            print(f"   📎 URL: {result['post_url']}")
        
        return {
            **state,
            "weekly_report": result,
            "step": "publish_medium_complete"
        }
    except Exception as e:
        print(f"   ❌ Medium publishing error: {e}")
        return {
            **state,
            "errors": [f"Medium publishing error: {str(e)}"],
            "step": "publish_medium_failed"
        }


async def finalize_node(state: AgentState) -> AgentState:
    """
    Final node: Log results and return final state
    """
    print("\n" + "=" * 60)
    print("✅ LANGGRAPH AGENT - Pipeline Complete")
    print("=" * 60)
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
    
    print("=" * 60 + "\n")
    
    return {**state, "step": "completed"}


# ============================================
# BUILD THE LANGGRAPH WORKFLOW
# ============================================

def build_agent_graph() -> StateGraph:
    """
    Construct the LangGraph StateGraph for the agent pipeline
    
    Pipeline Flow:
    scrape → dedupe → summarize → publish_x → publish_discord → publish_medium → finalize → END
    """
    # Create the graph with our state schema
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("scrape", scrape_node)
    workflow.add_node("dedupe", dedupe_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("publish_x", publish_x_node)
    workflow.add_node("publish_discord", publish_discord_node)
    workflow.add_node("publish_medium", publish_medium_node)
    workflow.add_node("finalize", finalize_node)
    
    # Define the edges (linear flow)
    workflow.add_edge("scrape", "dedupe")
    workflow.add_edge("dedupe", "summarize")
    workflow.add_edge("summarize", "publish_x")
    workflow.add_edge("publish_x", "publish_discord")
    workflow.add_edge("publish_discord", "publish_medium")
    workflow.add_edge("publish_medium", "finalize")
    workflow.add_edge("finalize", END)
    
    # Set entry point
    workflow.set_entry_point("scrape")
    
    return workflow


# Compile the graph once for reuse
agent_graph = build_agent_graph().compile()


async def run_agent(
    publish_to_x: bool = False,
    publish_to_medium: bool = False,
    publish_to_discord: bool = False
) -> Dict:
    """
    Run the complete agent pipeline using LangGraph
    
    Args:
        publish_to_x: Whether to publish daily updates to X
        publish_to_medium: Whether to publish weekly report to Medium
        publish_to_discord: Whether to publish daily updates to Discord
        
    Returns:
        Final state dictionary
    """
    print("\n" + "=" * 60)
    print("🤖 PULSE AI AGENT - LangGraph Pipeline Starting")
    print("=" * 60 + "\n")
    
    # Initialize state
    initial_state: AgentState = {
        "raw_items": [],
        "unique_items": [],
        "duplicate_items": [],
        "summaries": [],
        "daily_posts": [],
        "weekly_report": {},
        "errors": [],
        "step": "initialized",
        "publish_to_x": publish_to_x,
        "publish_to_medium": publish_to_medium,
        "publish_to_discord": publish_to_discord
    }
    
    # Run the graph
    final_state = await agent_graph.ainvoke(initial_state)
    
    return final_state


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

*This report was generated by Pulse, an autonomous AI news intelligence agent powered by LangGraph.*
"""
    
    title = f"Weekly AI Deep Dive: {week_start.strftime('%B %d, %Y')}"
    tags = ["Artificial Intelligence", "Machine Learning", "Technology"]
    
    return {
        "title": title,
        "content": content,
        "tags": tags
    }