"""
Cron jobs for automated tasks using APScheduler
"""
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from db import SessionLocal, get_active_subscribers, update_subscriber_last_sent
from email_service import send_daily_report_email
from db import get_summaries_by_date, NewsItemDB, get_news_items, save_news_item, save_summary
from scraper import scrape_all_sources
from dedupe import deduplicate_items
from summaries import batch_summarize


async def refresh_content(db):
    """
    Fetch new content and generate summaries
    Called before sending daily emails to ensure fresh content
    """
    print("🔄 Refreshing content before sending daily emails...")
    
    try:
        # Step 1: Scrape all sources
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
                print(f"  ⚠️  Error saving item: {e}")
                continue
        
        print(f"  ✅ Saved {saved_count} new items")
        
        # Step 2: Generate summaries for new items
        if saved_count > 0:
            news_items_db = get_news_items(db, limit=100)
            news_items = [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "url": item.url
                }
                for item in news_items_db
            ]
            
            summaries = batch_summarize(news_items)
            
            for summary in summaries:
                save_summary(db, summary)
            
            print(f"  ✅ Generated {len(summaries)} summaries")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error refreshing content: {e}")
        import traceback
        traceback.print_exc()
        return False


async def send_daily_emails_to_subscribers():
    """
    Send daily email reports to all active subscribers
    Runs every day at 8 AM UTC
    First refreshes content, then sends emails
    """
    print(f"🕐 Starting daily email job at {datetime.utcnow()}")
    
    db = SessionLocal()
    try:
        # Get all active subscribers
        subscribers = get_active_subscribers(db)
        
        if not subscribers:
            print("📭 No active subscribers found")
            return
        
        print(f"📧 Found {len(subscribers)} active subscribers")
        
        # Refresh content first - fetch and summarize new items
        await refresh_content(db)
        
        # Get today's summaries
        summaries_db = get_summaries_by_date(db, datetime.utcnow())
        
        if not summaries_db:
            print("📭 No summaries available for today")
            return
        
        print(f"📰 Found {len(summaries_db)} summaries for today")
        
        # Fetch news items and combine with summaries
        summaries = []
        for s in summaries_db:
            news_item = db.query(NewsItemDB).filter(NewsItemDB.id == s.news_item_id).first()
            
            summaries.append({
                "title": news_item.title if news_item else "Untitled",
                "three_sentence_summary": s.three_sentence_summary,
                "tags": s.tags,
                "created_date": s.created_date
            })
        
        # Send email to each subscriber
        sent_count = 0
        failed_count = 0
        
        for subscriber in subscribers:
            try:
                result = await send_daily_report_email(summaries, subscriber.email)
                
                if result.get("success"):
                    update_subscriber_last_sent(db, subscriber.email)
                    sent_count += 1
                    print(f"✅ Sent to {subscriber.email}")
                else:
                    failed_count += 1
                    print(f"❌ Failed to send to {subscriber.email}")
            except Exception as e:
                failed_count += 1
                print(f"❌ Error sending to {subscriber.email}: {e}")
        
        print(f"📊 Email job complete: {sent_count} sent, {failed_count} failed")
        
    except Exception as e:
        print(f"❌ Error in daily email job: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def start_scheduler():
    """
    Start the APScheduler with daily email job
    Runs at 8:00 AM UTC every day
    """
    scheduler = AsyncIOScheduler()
    
    # Add job to run daily at 8 AM UTC
    scheduler.add_job(
        send_daily_emails_to_subscribers,
        CronTrigger(hour=8, minute=0),
        id="daily_email_job",
        name="Send daily emails to subscribers",
        replace_existing=True
    )
    
    # For testing: also run every hour
    # scheduler.add_job(
    #     send_daily_emails_to_subscribers,
    #     CronTrigger(minute=0),
    #     id="hourly_email_test",
    #     name="Hourly email test",
    #     replace_existing=True
    # )
    
    scheduler.start()
    print("✅ Scheduler started - Daily emails will be sent at 8:00 AM UTC")
    
    return scheduler
