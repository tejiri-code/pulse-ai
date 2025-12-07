import praw
import os

# Load these from environment variables 
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "PulseAI_Scraper/1.0"

def get_reddit_headlines(subreddits=["MachineLearning", "artificial"], limit=5):
    """
    Fetches top hot headlines from specified subreddits.
    """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        
        results = []
        
        for sub_name in subreddits:
            subreddit = reddit.subreddit(sub_name)
            # scraping 'hot' posts
            for post in subreddit.hot(limit=limit):
                if not post.stickied:  # Ignore pinned posts
                    results.append({
                        "source": f"r/{sub_name}",
                        "title": post.title,
                        "url": post.url,
                        "score": post.score,
                        "content": post.selftext[:500]  # First 500 chars of content
                    })
        return results

    except Exception as e:
        print(f"Error scraping Reddit: {e}")
        return []

if __name__ == "__main__":
    data = get_reddit_headlines()
    for item in data:
        print(f"[{item['source']}] {item['title']} ({item['score']} upvotes)")