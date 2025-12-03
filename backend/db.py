"""
Database setup and helper functions using SQLite
"""
import os
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pulse.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class NewsItemDB(Base):
    """SQLAlchemy model for news items"""
    __tablename__ = "news_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    source = Column(String, index=True)
    content = Column(Text, nullable=True)
    published_date = Column(DateTime, nullable=True)
    scraped_date = Column(DateTime, default=datetime.utcnow)
    embedding = Column(JSON, nullable=True)  # Stored as JSON array
    novelty_score = Column(Float, nullable=True)
    is_duplicate = Column(Boolean, default=False)


class SummaryDB(Base):
    """SQLAlchemy model for summaries"""
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    news_item_id = Column(Integer, index=True)
    three_sentence_summary = Column(Text)
    social_hook = Column(String)
    tags = Column(JSON)  # Stored as JSON array
    created_date = Column(DateTime, default=datetime.utcnow)


class DailyReportDB(Base):
    """SQLAlchemy model for daily reports"""
    __tablename__ = "daily_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    title = Column(String)
    content = Column(Text)
    summaries_included = Column(JSON)  # Array of summary IDs
    sent = Column(Boolean, default=False)


class WeeklyReportDB(Base):
    """SQLAlchemy model for weekly reports"""
    __tablename__ = "weekly_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    week_start = Column(DateTime, index=True)
    week_end = Column(DateTime)
    title = Column(String)
    content = Column(Text)
    medium_draft_url = Column(String, nullable=True)
    published = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.utcnow)


class XPostDB(Base):
    """SQLAlchemy model for X posts"""
    __tablename__ = "x_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    summary_id = Column(Integer, index=True)
    tweet_text = Column(String)
    tweet_id = Column(String, nullable=True)
    posted_date = Column(DateTime, nullable=True)
    success = Column(Boolean, default=False)


class MediumPostDB(Base):
    """SQLAlchemy model for Medium posts"""
    __tablename__ = "medium_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    weekly_report_id = Column(Integer, index=True)
    medium_post_id = Column(String, nullable=True)
    medium_url = Column(String, nullable=True)
    posted_date = Column(DateTime, nullable=True)
    success = Column(Boolean, default=False)


# Create all tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


# Database helper functions
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_news_item(db: Session, item: dict) -> Optional[NewsItemDB]:
    """
    Save a news item to database
    Skips if URL already exists
    """
    try:
        # Check if item already exists
        existing = get_news_item_by_url(db, item.get("url", ""))
        if existing:
            return existing
        
        db_item = NewsItemDB(**item)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        print(f"Error saving news item: {e}")
        return None


def get_news_items(db: Session, skip: int = 0, limit: int = 100) -> List[NewsItemDB]:
    """Get news items from database"""
    return db.query(NewsItemDB).offset(skip).limit(limit).all()


def get_news_item_by_url(db: Session, url: str) -> Optional[NewsItemDB]:
    """Get news item by URL"""
    return db.query(NewsItemDB).filter(NewsItemDB.url == url).first()


def save_summary(db: Session, summary: dict) -> Optional[SummaryDB]:
    """
    Save a summary to database
    Skips if summary for this news_item_id already exists
    """
    try:
        # Check if summary for this news item already exists
        existing = db.query(SummaryDB).filter(
            SummaryDB.news_item_id == summary.get("news_item_id")
        ).first()
        
        if existing:
            return existing
        
        db_summary = SummaryDB(**summary)
        db.add(db_summary)
        db.commit()
        db.refresh(db_summary)
        return db_summary
    except Exception as e:
        db.rollback()
        print(f"Error saving summary: {e}")
        return None


def get_summaries(db: Session, skip: int = 0, limit: int = 100) -> List[SummaryDB]:
    """
    Get all summaries with pagination, newest first
    """
    return db.query(SummaryDB)\
        .order_by(SummaryDB.created_date.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_summaries_by_date(db: Session, date: datetime) -> List[SummaryDB]:
    """Get summaries created on a specific date"""
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    return db.query(SummaryDB).filter(
        SummaryDB.created_date >= start,
        SummaryDB.created_date <= end
    ).all()


def save_daily_report(db: Session, report: dict) -> DailyReportDB:
    """Save a daily report to database"""
    db_report = DailyReportDB(**report)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def save_weekly_report(db: Session, report: dict) -> WeeklyReportDB:
    """Save a weekly report to database"""
    db_report = WeeklyReportDB(**report)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def save_x_post(db: Session, post: dict) -> XPostDB:
    """Save an X post to database"""
    db_post = XPostDB(**post)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def save_medium_post(db: Session, post: dict) -> MediumPostDB:
    """Save a Medium post to database"""
    db_post = MediumPostDB(**post)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
