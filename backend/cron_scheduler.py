"""
Daily Cron Job Scheduler
Automatically sends daily email reports
"""
import schedule
import time
import asyncio
import os
from datetime import datetime
from email_service import send_daily_report_email
from db import get_db, get_summaries_by_date, NewsItemDB
from sqlalchemy.orm import Session


async def send_daily_email_job():
    """Job to send daily email report"""
    print(f"\n🕐 {datetime.now()} - Running daily email job...")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Get today's summaries
        summaries_db = get_summaries_by_date(db, datetime.utcnow())
        
        if not summaries_db:
            print("⚠️  No summaries found for today, skipping email")
            return
        
        # Prepare summaries with titles
        summaries = []
        for s in summaries_db:
            news_item = db.query(NewsItemDB).filter(NewsItemDB.id == s.news_item_id).first()
            summaries.append({
                'title': news_item.title if news_item else 'Untitled',
                'three_sentence_summary': s.three_sentence_summary,
                'social_hook': s.social_hook,
                'tags': s.tags
            })
        
        # Get recipient from environment variable
        recipient = os.getenv("DAILY_EMAIL_RECIPIENT", os.getenv("RECIPIENT_EMAIL", ""))
        
        if not recipient:
            print("❌ No recipient email configured! Set DAILY_EMAIL_RECIPIENT in .env")
            return
        
        # Send email
        print(f"📧 Sending daily report to {recipient}...")
        result = await send_daily_report_email(summaries, recipient)
        
        if result.get("success"):
            print(f"✅ Daily email sent successfully to {recipient}!")
        else:
            print(f"❌ Failed to send daily email: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in daily email job: {e}")
    finally:
        if db:
            db.close()


def run_async_job(job_func):
    """Helper to run async functions in schedule"""
    asyncio.run(job_func())


def start_cron_scheduler():
    """Start the cron scheduler"""
    # Schedule daily email at 9 AM
    schedule.every().day.at("09:00").do(run_async_job, send_daily_email_job)
    
    print("🚀 Cron scheduler started!")
    print("📅 Daily email scheduled for 9:00 AM")
    print("⏰ Current time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    print("="*50)
    print("🤖 Pulse AI Agent - Cron Scheduler")
    print("="*50)
    start_cron_scheduler()
