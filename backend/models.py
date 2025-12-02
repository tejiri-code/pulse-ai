"""
Pydantic models for data validation and serialization
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    """Model for a scraped news item"""
    id: Optional[int] = None
    title: str
    url: str
    source: str  # 'arxiv', 'github', 'rss', 'blog'
    content: Optional[str] = None
    published_date: Optional[datetime] = None
    scraped_date: datetime = Field(default_factory=datetime.utcnow)
    embedding: Optional[List[float]] = None
    novelty_score: Optional[float] = None
    is_duplicate: bool = False
    
    class Config:
        from_attributes = True


class Summary(BaseModel):
    """Model for a generated summary"""
    id: Optional[int] = None
    news_item_id: int
    three_sentence_summary: str
    social_hook: str  # 30-word social media hook
    tags: List[str] = []
    created_date: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class DailyReport(BaseModel):
    """Model for daily email report"""
    id: Optional[int] = None
    date: datetime = Field(default_factory=datetime.utcnow)
    title: str
    content: str  # Full email content
    summaries_included: List[int] = []  # IDs of summaries included
    sent: bool = False
    
    class Config:
        from_attributes = True


class WeeklyReport(BaseModel):
    """Model for weekly Medium article"""
    id: Optional[int] = None
    week_start: datetime
    week_end: datetime
    title: str
    content: str  # Full long-form article
    medium_draft_url: Optional[str] = None
    published: bool = False
    created_date: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class XPost(BaseModel):
    """Model for X (Twitter) post"""
    id: Optional[int] = None
    summary_id: int
    tweet_text: str
    tweet_id: Optional[str] = None  # ID from Twitter API
    posted_date: Optional[datetime] = None
    success: bool = False
    
    class Config:
        from_attributes = True


class MediumPost(BaseModel):
    """Model for Medium post"""
    id: Optional[int] = None
    weekly_report_id: int
    medium_post_id: Optional[str] = None
    medium_url: Optional[str] = None
    posted_date: Optional[datetime] = None
    success: bool = False
    
    class Config:
        from_attributes = True


class ScrapeResponse(BaseModel):
    """Response model for scraping endpoint"""
    success: bool
    items_scraped: int
    items_new: int
    items_duplicate: int
    message: str


class SummaryResponse(BaseModel):
    """Response model for summaries endpoint"""
    summaries: List[Summary]
    total: int


class PublishResponse(BaseModel):
    """Response model for publish endpoints"""
    success: bool
    posts_created: int
    message: str
    mock_mode: bool


class DailyReportResponse(BaseModel):
    """Response model for daily report endpoint"""
    report: DailyReport
    summaries: List[Summary]


class WeeklyReportResponse(BaseModel):
    """Response model for weekly report endpoint"""
    report: WeeklyReport
    summaries_count: int
