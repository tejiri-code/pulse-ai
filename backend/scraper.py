"""
News scraping module for multiple sources: RSS, GitHub, Blogs
Supports mock mode for testing without internet
"""
import os
import feedparser
import httpx
from typing import List, Dict
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


# Importing the newly added reddit scraping code
from scraper_reddit import get_reddit_headlines

# Change to False to enable real scraping
USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "False").lower() == "true"


# Mock data for testing
MOCK_NEWS_DATA = [
    {
        "title": "Breakthrough in Multimodal AI: GPT-4V Achieves Human-Level Vision Understanding",
        "url": "https://arxiv.org/abs/2023.12345",
        "source": "arxiv",
        "content": "Researchers have developed a new multimodal AI model that achieves human-level performance on vision-language tasks. The model, GPT-4V, combines advanced vision encoders with large language models to understand and reason about images with unprecedented accuracy. Key innovations include a novel attention mechanism and improved training techniques that enable better cross-modal understanding.",
        "published_date": datetime.utcnow() - timedelta(hours=2)
    },
    {
        "title": "LangChain Releases v0.1.0 with Major Graph-Based Agent Improvements",
        "url": "https://github.com/langchain/langchain/releases/v0.1.0",
        "source": "github",
        "content": "LangChain has released version 0.1.0, featuring LangGraph - a revolutionary framework for building stateful, graph-based AI agents. This release includes improved memory management, better tool calling, and a new visual debugger for agent workflows. Developers can now create more complex autonomous agents with branching logic and conditional execution.",
        "published_date": datetime.utcnow() - timedelta(hours=5)
    },
    {
        "title": "Meta Unveils Llama 3: Open-Source Model Rivals GPT-4 Performance",
        "url": "https://ai.meta.com/blog/llama-3-release",
        "source": "blog",
        "content": "Meta AI has released Llama 3, their most capable open-source language model to date. With 70 billion parameters and trained on 2 trillion tokens, Llama 3 achieves performance comparable to GPT-4 on many benchmarks while remaining fully open-source. The model excels at reasoning, coding, and multilingual tasks, marking a significant milestone for open AI development.",
        "published_date": datetime.utcnow() - timedelta(hours=8)
    },
    {
        "title": "Google DeepMind's AlphaCode 2 Solves Complex Programming Challenges",
        "url": "https://deepmind.google/research/alphacode-2",
        "source": "blog",
        "content": "AlphaCode 2 from Google DeepMind has achieved remarkable results in competitive programming, solving complex algorithmic problems that challenge even experienced programmers. Using a combination of large language models and reinforcement learning, AlphaCode 2 ranks in the top 15% of human competitors on Codeforces. This advancement demonstrates AI's growing capability in software engineering tasks.",
        "published_date": datetime.utcnow() - timedelta(hours=12)
    },
    {
        "title": "Anthropic Introduces Constitutional AI for Safer Language Models",
        "url": "https://www.anthropic.com/constitutional-ai",
        "source": "blog",
        "content": "Anthropic has released a new approach called Constitutional AI (CAI) that trains language models to be more helpful, harmless, and honest. The technique uses a set of principles (a 'constitution') to guide model behavior during training. Early results show CAI models refuse harmful requests more reliably while maintaining helpfulness on benign queries. This represents a significant step toward aligned AI systems.",
        "published_date": datetime.utcnow() - timedelta(hours=18)
    }
]


async def scrape_arxiv(query: str = "artificial intelligence", max_results: int = 5) -> List[Dict]:
    """
    Scrape recent papers from ArXiv (mock mode only for now)
    
    Args:
        query: Search query for arXiv
        max_results: Maximum number of results to return
        
    Returns:
        List of news items from ArXiv
    """
    # For hackathon demo, always use mock mode to avoid dependencies
    return [item for item in MOCK_NEWS_DATA if item["source"] == "arxiv"]


async def scrape_github_trending() -> List[Dict]:
    """
    Scrape GitHub trending repositories (AI/ML focused)
    
    Returns:
        List of trending GitHub repos
    """
    if USE_MOCK_MODE:
        return [item for item in MOCK_NEWS_DATA if item["source"] == "github"]
    
    try:
        url = "https://github.com/trending/python?since=daily"
        print(f"  Fetching GitHub trending: {url}")
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            response = await client.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            items = []
            repos = soup.find_all('article', class_='Box-row')[:10]
            
            print(f"  Found {len(repos)} trending repos")
            
            for repo in repos:
                try:
                    title_elem = repo.find('h2')
                    if not title_elem:
                        continue
                        
                    link = title_elem.find('a')
                    if not link:
                        continue
                    
                    repo_name = link.get_text(strip=True).replace(' ', '').replace('\n', '')
                    repo_url = f"https://github.com{link.get('href', '')}"
                    
                    desc_elem = repo.find('p', class_='col-9')
                    description = desc_elem.get_text(strip=True) if desc_elem else "No description"
                    
                    # Filter for AI/ML related repos
                    ai_keywords = ['ai', 'ml', 'machine learning', 'deep learning', 'neural', 'llm', 'gpt', 'transformer', 'model']
                    text_to_check = (repo_name + ' ' + description).lower()
                    
                    if any(keyword in text_to_check for keyword in ai_keywords):
                        items.append({
                            "title": f"Trending: {repo_name}",
                            "url": repo_url,
                            "source": "github",
                            "content": description,
                            "published_date": datetime.utcnow()
                        })
                except Exception as e:
                    print(f"  ✗ Error parsing repo: {e}")
                    continue
            
            print(f"  ✓ Got {len(items)} AI/ML repos")
            return items
            
    except Exception as e:
        print(f"  ✗ Error scraping GitHub: {e}")
        return []


async def scrape_rss_feeds() -> List[Dict]:
    """
    Scrape AI/ML news from RSS feeds
    
    Returns:
        List of news items from RSS feeds
    """
    if USE_MOCK_MODE:
        return [item for item in MOCK_NEWS_DATA if item["source"] == "rss"]
    
  # RSS feeds to scrape
    RSS_FEEDS = [
        "http://export.arxiv.org/rss/cs.AI",  # ArXiv AI papers
        "https://blog.google/technology/ai/feed/",  # Google AI Blog
        "https://openai.com/blog/rss.xml",  # OpenAI Blog
        "https://www.deepmind.com/blog/rss.xml",  # DeepMind Blog
        "https://blogs.nvidia.com/feed/",  # NVIDIA Blog
        "https://ai.meta.com/blog/feed/",  # Meta AI
        "https://www.anthropic.com/news/rss.xml",  # Anthropic
        "https://huggingface.co/blog/feed.xml",  # Hugging Face
    ]
    
    items = []
    
    for feed_url in RSS_FEEDS:
        try:
            print(f"  Fetching RSS feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:  # Limit to 3 per feed
                pub_date = datetime.utcnow()
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        pub_date = datetime(*entry.published_parsed[:6])
                    except:
                        pass
                
                items.append({
                    "title": entry.get('title', 'No title'),
                    "url": entry.get('link', ''),
                    "source": "rss",
                    "content": entry.get('summary', entry.get('description', ''))[:500],
                    "published_date": pub_date
                })
            print(f"  ✓ Got {len(feed.entries[:3])} items from {feed_url}")
        except Exception as e:
            print(f"  ✗ Error scraping RSS feed {feed_url}: {e}")
            continue
    
    return items


async def scrape_blogs() -> List[Dict]:
    """
    Scrape AI/ML blogs and product announcements
    
    Returns:
        List of news items from blogs
    """
    if USE_MOCK_MODE:
        return [item for item in MOCK_NEWS_DATA if item["source"] == "blog"]
    
    blog_urls = [
        "https://openai.com/blog",
        "https://blog.google/technology/ai/",
        "https://www.anthropic.com/news"
    ]
    
    items = []
    
    for url in blog_urls:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # This is a simplified scraper - in production, each blog would need custom selectors
                articles = soup.find_all('article')[:2]
                
                for article in articles:
                    title_elem = article.find(['h2', 'h3', 'h1'])
                    link_elem = article.find('a')
                    
                    if title_elem and link_elem:
                        items.append({
                            "title": title_elem.get_text(strip=True),
                            "url": link_elem.get('href', ''),
                            "source": "blog",
                            "content": article.get_text(strip=True)[:500],
                            "published_date": datetime.utcnow()
                        })
        except Exception as e:
            print(f"Error scraping blog {url}: {e}")
            continue
    
    return items


async def scrape_all_sources() -> List[Dict]:
    """
    Scrape all news sources
    
    Returns:
        Combined list of all news items
    """
    all_items = []
    
    # Scrape all sources
    arxiv_items = await scrape_arxiv()
    github_items = await scrape_github_trending()
    rss_items = await scrape_rss_feeds()
    blog_items = await scrape_blogs()
    
    # Added reddit source
    reddit_data = get_reddit_headlines()


    all_items.extend(arxiv_items)
    all_items.extend(github_items)
    all_items.extend(rss_items)
    all_items.extend(blog_items)
    all_items.extend(reddit_data)
    
    return all_items
