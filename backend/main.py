"""
FastAPI main application
Exposes REST API endpoints for the Pulse AI Agent
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import os

from models import (
    ScrapeResponse, SummaryResponse, PublishResponse,
    DailyReportResponse, WeeklyReportResponse, Summary, NewsItem
)
from db import (
    init_db, get_db, get_news_items, get_summaries,
    get_summaries_by_date, save_news_item, save_summary,
    NewsItemDB, SummaryDB, save_subscriber, get_active_subscribers, 
    unsubscribe_email, update_subscriber_last_sent
)
from agent import run_agent
from scraper import scrape_all_sources
from dedupe import deduplicate_items
from summaries import batch_summarize
from tasks import generate_daily_report_content

# Initialize FastAPI app
app = FastAPI(
    title="Pulse AI Agent API",
    description="Autonomous AI news intelligence agent with auto-publishing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", os.getenv("FRONTEND_URL", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables and start scheduler"""
    init_db()
    print("✅ Database initialized")
    
    # Start cron scheduler for automated tasks
    from cron_jobs import start_scheduler
    start_scheduler()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 Pulse AI Agent API",
        "version": "1.0.0",
        "status": "running",
        "mock_mode": os.getenv("USE_MOCK_MODE", "True").lower() == "true"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/fetch", response_model=ScrapeResponse)
async def fetch_news(db: Session = Depends(get_db)):
    """
    Fetch and process new AI/ML news
    Scrapes all sources, deduplicates, and stores in database
    """
    try:
        # Scrape all sources
        raw_items = await scrape_all_sources()
        print(f"  Scraped {len(raw_items)} total items")
        
        # Get existing items from database
        existing_items_db = get_news_items(db, limit=1000)
        existing_items = [
            {
                "title": item.title,
                "url": item.url,
                "embedding": item.embedding if item.embedding else []
            }
            for item in existing_items_db
        ]
        print(f"  Found {len(existing_items)} existing items in DB")
        
        # Deduplicate
        unique_items, duplicate_items = deduplicate_items(raw_items, existing_items)
        print(f"  After dedup: {len(unique_items)} unique, {len(duplicate_items)} duplicates")
        
        # Save unique items to database
        saved_count = 0
        for item in unique_items:
            try:
                save_news_item(db, item)
                saved_count += 1
            except Exception as e:
                print(f"  ⚠️  Error saving item '{item.get('title', 'Unknown')[:50]}': {e}")
                continue
        
        print(f"  ✅ Saved {saved_count} items to database")
        
        return ScrapeResponse(
            success=True,
            items_scraped=len(raw_items),
            items_new=len(unique_items),
            items_duplicate=len(duplicate_items),
            message=f"Successfully scraped {len(unique_items)} new items"
        )
        
    except Exception as e:
        print(f"  ❌ Error in /fetch endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/summaries", response_model=SummaryResponse)
async def get_all_summaries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all summaries from database
    """
    try:
        summaries_db = get_summaries(db, skip=skip, limit=limit)
        
        summaries = [
            Summary(
                id=s.id,
                news_item_id=s.news_item_id,
                three_sentence_summary=s.three_sentence_summary,
                social_hook=s.social_hook,
                tags=s.tags,
                created_date=s.created_date
            )
            for s in summaries_db
        ]
        
        return SummaryResponse(
            summaries=summaries,
            total=len(summaries)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summaries/generate")
async def generate_summaries(db: Session = Depends(get_db)):
    """
    Generate summaries for news items that don't have them yet
    """
    try:
        # Get news items
        news_items_db = get_news_items(db, limit=100)
        
        # Convert to dict format
        news_items = [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "url": item.url
            }
            for item in news_items_db
        ]
        
        # Generate summaries
        summaries = batch_summarize(news_items)
        
        # Save to database
        for summary in summaries:
            save_summary(db, summary)
        
        return {
            "success": True,
            "summaries_generated": len(summaries),
            "message": f"Generated {len(summaries)} summaries"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/publish/daily", response_model=PublishResponse)
async def publish_daily():
    """
    Run daily publishing workflow
    Scrapes, processes, summarizes, and posts to X (Twitter)
    """
    try:
        final_state = await run_agent(
            publish_to_x=True,
            publish_to_medium=False
        )
        
        posts_created = len(final_state.get("daily_posts", []))
        mock_mode = os.getenv("USE_MOCK_MODE", "True").lower() == "true"
        
        return PublishResponse(
            success=len(final_state.get("errors", [])) == 0,
            posts_created=posts_created,
            message=f"Published {posts_created} posts to X",
            mock_mode=mock_mode
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/publish/weekly", response_model=PublishResponse)
async def publish_weekly():
    """
    Run weekly publishing workflow
    Generates deep dive report and posts to Medium as draft
    """
    try:
        final_state = await run_agent(
            publish_to_x=False,
            publish_to_medium=True
        )
        
        weekly_report = final_state.get("weekly_report", {})
        success = weekly_report.get("success", False)
        mock_mode = os.getenv("USE_MOCK_MODE", "True").lower() == "true"
        
        return PublishResponse(
            success=success,
            posts_created=1 if success else 0,
            message="Published weekly report to Medium" if success else "Failed to publish",
            mock_mode=mock_mode
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/daily_report", response_model=DailyReportResponse)
async def get_daily_report(
    date: str = None,
    db: Session = Depends(get_db)
):
    """
    Get daily report for a specific date
    If no date provided, returns today's report
    """
    try:
        if date:
            target_date = datetime.fromisoformat(date)
        else:
            target_date = datetime.utcnow()
        
        summaries_db = get_summaries_by_date(db, target_date)
        
        summaries = [
            Summary(
                id=s.id,
                news_item_id=s.news_item_id,
                three_sentence_summary=s.three_sentence_summary,
                social_hook=s.social_hook,
                tags=s.tags,
                created_date=s.created_date
            )
            for s in summaries_db
        ]
        
        # Generate report content
        content = generate_daily_report_content([s.dict() for s in summaries])
        
        from models import DailyReport
        report = DailyReport(
            date=target_date,
            title=f"Daily AI Brief - {target_date.strftime('%Y-%m-%d')}",
            content=content,
            summaries_included=[s.id for s in summaries],
            sent=False
        )
        
        return DailyReportResponse(
            report=report,
            summaries=summaries
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weekly_report", response_model=WeeklyReportResponse)
async def get_weekly_report(db: Session = Depends(get_db)):
    """
    Get weekly report for the current week
    """
    try:
        # Get summaries from the last 7 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        # This is simplified - in production, you'd query across date range
        summaries_db = get_summaries(db, limit=50)
        
        from agent import generate_weekly_report
        from models import WeeklyReport
        
        summaries_dict = [
            {
                "title": s.news_item_id,  # Would need to join with news_items
                "three_sentence_summary": s.three_sentence_summary,
                "tags": s.tags
            }
            for s in summaries_db
        ]
        
        report_data = generate_weekly_report(summaries_dict)
        
        report = WeeklyReport(
            week_start=start_date,
            week_end=end_date,
            title=report_data["title"],
            content=report_data["content"],
            published=False
        )
        
        return WeeklyReportResponse(
            report=report,
            summaries_count=len(summaries_db)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/email/daily-report")
async def send_daily_email(recipient: str = None, db: Session = Depends(get_db)):
    """
    Send daily report via Gmail SMTP
    """
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient email is required")
    
    try:
        from email_service import send_daily_report_email
        
        # Get today's summaries
        summaries_db = get_summaries_by_date(db, datetime.utcnow())
        
        if not summaries_db:
            return {
                "success": False,
                "message": "No summaries available for today"
            }
        
        # Fetch news items and combine with summaries
        summaries = []
        for s in summaries_db:
            # Get the corresponding news item
            news_item = db.query(NewsItemDB).filter(NewsItemDB.id == s.news_item_id).first()
            
            summaries.append({
                "title": news_item.title if news_item else "Untitled",
                "three_sentence_summary": s.three_sentence_summary,
                "tags": s.tags,
                "created_date": s.created_date
            })
        
        result = await send_daily_report_email(summaries, recipient)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/email/test")
async def send_test_email():
    """
    Send test email to verify EmailJS configuration
    """
    try:
        from email_service import send_test_email
        result = await send_test_email()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# NEW FREE PLATFORM ENDPOINTS

@app.post("/publish/bluesky")
async def publish_bluesky(request: Request, db: Session = Depends(get_db)):
    """Publish to Bluesky (free)"""
    body = await request.json()
    from publisher_bluesky import publish_daily_to_bluesky
    summaries = [{"social_hook": s.social_hook, "tags": s.tags} for s in get_summaries_by_date(db, datetime.utcnow())]
    return await publish_daily_to_bluesky(summaries, body.get("blueskyHandle"), body.get("blueskyAppPassword"))

@app.post("/publish/linkedin")
async def publish_linkedin(request: Request, db: Session = Depends(get_db)):
    """Publish to LinkedIn (free)"""
    body = await request.json()
    from publisher_linkedin import publish_to_linkedin  
    summaries = [{"social_hook": s.social_hook} for s in get_summaries_by_date(db, datetime.utcnow())]
    return await publish_to_linkedin(summaries, body.get("linkedinAccessToken"))

@app.post("/publish/devto")
async def publish_devto(request: Request, db: Session = Depends(get_db)):
    """Publish to Dev.to (free)"""
    body = await request.json()
    from publisher_devto import publish_weekly_to_devto
    summaries_db = get_summaries_by_date(db, datetime.utcnow())
    summaries = []
    for s in summaries_db:
        news = db.query(NewsItemDB).filter(NewsItemDB.id == s.news_item_id).first()
        summaries.append({"title": news.title if news else "Untitled", "three_sentence_summary": s.three_sentence_summary, "tags": s.tags})
    return await publish_weekly_to_devto(summaries, body.get("devtoApiKey"))

@app.post("/publish/mastodon")
async def publish_mastodon(request: Request, db: Session = Depends(get_db)):
    """Publish to Mastodon (free)"""
    body = await request.json()
    from publisher_mastodon import publish_daily_to_mastodon
    summaries_db = get_summaries_by_date(db, datetime.utcnow())
    summaries = [{"three_sentence_summary": s.three_sentence_summary, "social_hook": s.social_hook, "tags": s.tags} for s in summaries_db]
    return await publish_daily_to_mastodon(summaries, body.get("mastodonAccessToken"), body.get("mastodonInstance", "https://mastodon.social"))


# EMAIL SUBSCRIPTION ENDPOINTS

@app.post("/subscribe")
async def subscribe_email(request: Request, db: Session = Depends(get_db)):
    """Subscribe an email to daily reports"""
    try:
        body = await request.json()
        email = body.get("email")
        
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        subscriber = save_subscriber(db, email)
        
        if subscriber:
            return {
                "success": True,
                "message": f"Successfully subscribed {email} to daily reports"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to subscribe email")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/subscribe/{email}")
async def unsubscribe(email: str, db: Session = Depends(get_db)):
    """Unsubscribe an email from daily reports"""
    try:
        success = unsubscribe_email(db, email)
        
        if success:
            return {
                "success": True,
                "message": f"Successfully unsubscribed {email}"
            }
        else:
            raise HTTPException(status_code=404, detail="Email not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/subscribers")
async def list_subscribers(db: Session = Depends(get_db)):
    """Get all active subscribers (admin only in production)"""
    try:
        subscribers = get_active_subscribers(db)
        return {
            "subscribers": [{"email": s.email, "created_date": s.created_date} for s in subscribers],
            "total": len(subscribers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# EDGE TTS AUDIO PODCAST ENDPOINTS (FREE - No API Key Required!)

@app.post("/audio/daily")
async def generate_daily_audio(request: Request, db: Session = Depends(get_db)):
    """
    Generate podcast-style audio for daily news summary
    Uses Edge TTS (FREE - no API key needed!)
    """
    try:
        # Optional: get voice_id, date, and rate from request body
        try:
            body = await request.json()
            voice_id = body.get("voice_id")
            date_str = body.get("date")
            rate = body.get("rate", "+15%")  # Speech speed: +15% is default
        except:
            voice_id = None
            date_str = None
            rate = "+15%"
        
        # Get summaries for the date
        from datetime import datetime
        if date_str:
            target_date = datetime.fromisoformat(date_str)
        else:
            target_date = datetime.utcnow()
        
        summaries_db = get_summaries_by_date(db, target_date)
        
        if not summaries_db:
            raise HTTPException(status_code=404, detail="No summaries available for this date")
        
        # Build summary list with titles
        summaries = []
        for s in summaries_db:
            news_item = db.query(NewsItemDB).filter(NewsItemDB.id == s.news_item_id).first()
            summaries.append({
                "title": news_item.title if news_item else "Untitled",
                "three_sentence_summary": s.three_sentence_summary,
                "tags": s.tags
            })
        
        # Generate audio with Edge TTS (FREE!)
        from tts_service import generate_daily_podcast, DEFAULT_VOICE_ID
        audio_data = await generate_daily_podcast(
            summaries, 
            api_key=None,  # Not needed for Edge TTS
            voice_id=voice_id or DEFAULT_VOICE_ID,
            rate=rate  # Speech speed from frontend
        )
        
        # Return as streaming audio response
        from fastapi.responses import Response
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=daily_podcast.mp3"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating daily audio: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/audio/weekly")
async def generate_weekly_audio(request: Request, db: Session = Depends(get_db)):
    """
    Generate podcast-style audio for weekly news summary
    Uses Edge TTS (FREE - no API key needed!)
    """
    try:
        # Optional: get voice_id from request body
        try:
            body = await request.json()
            voice_id = body.get("voice_id")
        except:
            voice_id = None
        
        # Get summaries from the last 7 days
        from datetime import datetime, timedelta
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        # Get all recent summaries
        summaries_db = get_summaries(db, limit=50)
        
        if not summaries_db:
            raise HTTPException(status_code=404, detail="No summaries available")
        
        # Build summary list with titles
        summaries = []
        for s in summaries_db:
            news_item = db.query(NewsItemDB).filter(NewsItemDB.id == s.news_item_id).first()
            summaries.append({
                "title": news_item.title if news_item else "Untitled",
                "three_sentence_summary": s.three_sentence_summary,
                "tags": s.tags
            })
        
        # Generate audio with Edge TTS (FREE!)
        from tts_service import generate_weekly_podcast, DEFAULT_VOICE_ID
        audio_data = await generate_weekly_podcast(
            summaries, 
            api_key=None,  # Not needed for Edge TTS
            voice_id=voice_id or DEFAULT_VOICE_ID
        )
        
        # Return as streaming audio response
        from fastapi.responses import Response
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=weekly_podcast.mp3"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating weekly audio: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audio/voices")
async def get_voices():
    """Get available Edge TTS voices"""
    from tts_service import get_available_voices
    return get_available_voices()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

