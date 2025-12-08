import arxiv
from datetime import datetime

def get_latest_arxiv_papers(max_results=5):
    """
    Fetches real papers from ArXiv API.
    """
    try:
        # This Searches for AI (cs.AI), Machine Learning (cs.LG), and NLP (cs.CL)
        search = arxiv.Search(
            query = "cat:cs.AI OR cat:cs.LG OR cat:cs.CL",
            max_results = max_results,
            sort_by = arxiv.SortCriterion.SubmittedDate,
            sort_order = arxiv.SortOrder.Descending
        )

        results = []
        client = arxiv.Client()
        
        for result in client.results(search):
            results.append({
                "source": "arxiv", # matches the key used in scraper.py
                "title": result.title,
                "url": result.entry_id,
                "score": 0,
                "content": result.summary[:500],
                "published_date": result.published
            })
            
        return results

    except Exception as e:
        print(f"Error scraping ArXiv: {e}")
        return []