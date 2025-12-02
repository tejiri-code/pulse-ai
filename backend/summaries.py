"""
LLM-powered summarization using Groq API
Generates 3-sentence summaries, social hooks, and auto-tags
"""
import os
from typing import Dict, List
from groq import Groq

USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "False").lower() == "true"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Configure Groq client
if GROQ_API_KEY and not USE_MOCK_MODE:
    client = Groq(api_key=GROQ_API_KEY)
    model = "llama-3.3-70b-versatile"  # Current fast model
else:
    client = None
    model = None


MOCK_SUMMARIES = {
    "default": {
        "three_sentence_summary": "This article discusses a significant advancement in artificial intelligence technology. Researchers have developed a new approach that improves performance on key benchmarks. The innovation has potential applications across multiple domains.",
        "social_hook": "🚀 AI breakthrough alert! New technology achieves state-of-the-art results and opens doors to exciting applications. #AI #MachineLearning #Tech",
        "tags": ["AI", "Machine Learning", "Research", "Innovation"]
    }
}


def generate_summary(news_item: Dict) -> Dict:
    """
    Generate a comprehensive summary for a news item using Groq
    
    Args:
        news_item: News item with title and content
        
    Returns:
        Dictionary with summary, social hook, and tags
    """
    if USE_MOCK_MODE or not client:
        print("⚠️ Using mock mode for summaries")
        return generate_mock_summary(news_item)
    
    title = news_item.get("title", "")
    content = news_item.get("content", "")[:2000]  # Limit content length
    
    # If content is too short, use title as the main context
    if len(content) < 50:
        content = title
    
    prompt = f"""Analyze this AI/ML news and create:

1. A 3-sentence summary (specific, technical, informative)
2. A 30-word social media hook (engaging with hashtags)
3. 3-5 relevant tags

Title: {title}
Content: {content}

IMPORTANT: Make each summary unique and specific to THIS article. Mention specific technologies, companies, or achievements from the content.

Format:
SUMMARY: [your unique 3-sentence summary]
HOOK: [your 30-word hook]
TAGS: [tag1, tag2, tag3, tag4, tag5]"""

    try:
        print(f"🤖 Generating summary for: {title[:50]}...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI news analyst. Create unique, specific summaries. Never use generic phrases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content
        print(f"✅ Generated summary successfully")
        
        # Parse the response
        parsed = parse_llm_response(result_text)
        
        return {
            "news_item_id": news_item.get("id"),
            "three_sentence_summary": parsed["three_sentence_summary"],
            "social_hook": parsed["social_hook"],
            "tags": parsed["tags"]
        }
    except Exception as e:
        print(f"❌ Error generating summary with Groq: {e}")
        print(f"   Falling back to mock for: {title[:50]}")
        return generate_mock_summary(news_item)


def generate_mock_summary(news_item: Dict) -> Dict:
    """
    Generate a mock summary based on title and content
    
    Args:
        news_item: Dictionary with title and content
        
    Returns:
        Dictionary with summary, hook, and tags
    """
    title = news_item.get("title", "")
    content = news_item.get("content", "")
    
    # Extract key terms for more realistic mocking
    key_terms = extract_key_terms(title + " " + content)
    
    summary = f"{title} represents a significant development in AI/ML. "
    summary += "The research introduces novel techniques that advance the state-of-the-art. "
    summary += "This work has important implications for future AI applications."
    
    hook = f"🚀 Exciting AI news: {title[:50]}... A game-changer for ML! #AI #MachineLearning #Tech #Innovation #Research"
    
    tags = key_terms[:5] if len(key_terms) >= 5 else key_terms + ["AI", "Research", "Technology"]
    
    return {
        "news_item_id": news_item.get("id"),
        "three_sentence_summary": summary,
        "social_hook": hook[:280],  # Twitter character limit
        "tags": tags
    }


def extract_key_terms(text: str) -> List[str]:
    """
    Extract key terms from text for tagging
    
    Args:
        text: Input text
        
    Returns:
        List of key terms
    """
    # Common AI/ML terms
    ai_terms = [
        "GPT", "LLM", "Transformer", "Neural Network", "Deep Learning",
        "Machine Learning", "AI", "AGI", "Multimodal", "Vision",
        "NLP", "Computer Vision", "Reinforcement Learning", "LangChain",
        "LangGraph", "OpenAI", "Anthropic", "Meta", "Google", "DeepMind",
        "Research", "Model", "Training", "Fine-tuning", "Agent"
    ]
    
    found_terms = []
    text_lower = text.lower()
    
    for term in ai_terms:
        if term.lower() in text_lower:
            found_terms.append(term)
    
    return found_terms[:10]


def parse_llm_response(response: str) -> Dict:
    """
    Parse LLM response into structured format
    
    Args:
        response: Raw LLM response
        
    Returns:
        Structured dictionary
    """
    lines = response.strip().split('\n')
    
    summary = ""
    hook = ""
    tags = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()
        elif line.startswith("HOOK:"):
            hook = line.replace("HOOK:", "").strip()
        elif line.startswith("TAGS:"):
            tags_str = line.replace("TAGS:", "").strip()
            tags = [t.strip() for t in tags_str.replace("[", "").replace("]", "").split(",")]
    
    # Fallback if parsing fails
    if not summary or not hook:
        return MOCK_SUMMARIES["default"]
    
    return {
        "three_sentence_summary": summary,
        "social_hook": hook,
        "tags": tags
    }


def batch_summarize(news_items: List[Dict]) -> List[Dict]:
    """
    Generate summaries for multiple news items
    
    Args:
        news_items: List of news items
        
    Returns:
        List of summaries
    """
    summaries = []
    
    for item in news_items:
        summary = generate_summary(item)
        summary["news_item_id"] = item.get("id")
        summaries.append(summary)
    
    return summaries
