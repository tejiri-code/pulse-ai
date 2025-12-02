/**
 * TypeScript type definitions for Pulse AI Agent
 */

export interface NewsItem {
  id?: number;
  title: string;
  url: string;
  source: 'arxiv' | 'github' | 'rss' | 'blog';
  content?: string;
  published_date?: string;
  scraped_date: string;
  embedding?: number[];
  novelty_score?: number;
  is_duplicate: boolean;
}

export interface Summary {
  id?: number;
  news_item_id: number;
  three_sentence_summary: string;
  social_hook: string;
  tags: string[];
  created_date: string;
}

export interface DailyReport {
  id?: number;
  date: string;
  title: string;
  content: string;
  summaries_included: number[];
  sent: boolean;
}

export interface WeeklyReport {
  id?: number;
  week_start: string;
  week_end: string;
  title: string;
  content: string;
  medium_draft_url?: string;
  published: boolean;
  created_date: string;
}

export interface ScrapeResponse {
  success: boolean;
  items_scraped: number;
  items_new: number;
  items_duplicate: number;
  message: string;
}

export interface SummaryResponse {
  summaries: Summary[];
  total: number;
}

export interface PublishResponse {
  success: boolean;
  posts_created: number;
  message: string;
  mock_mode: boolean;
}

export interface DailyReportResponse {
  report: DailyReport;
  summaries: Summary[];
}

export interface WeeklyReportResponse {
  report: WeeklyReport;
  summaries_count: number;
}

export interface ApiError {
  detail: string;
}
