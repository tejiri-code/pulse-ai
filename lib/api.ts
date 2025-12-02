/**
 * API client for communicating with Pulse backend
 */

import type {
    ScrapeResponse,
    SummaryResponse,
    PublishResponse,
    DailyReportResponse,
    WeeklyReportResponse,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    private async request<T>(
        endpoint: string,
        options?: RequestInit
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options?.headers,
                },
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'API request failed');
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    // Health check
    async healthCheck(): Promise<{ status: string; timestamp: string }> {
        return this.request('/health');
    }

    // Fetch and process news
    async fetchNews(): Promise<ScrapeResponse> {
        return this.request('/fetch', { method: 'POST' });
    }

    // Get all summaries
    async getSummaries(skip: number = 0, limit: number = 100): Promise<SummaryResponse> {
        return this.request(`/summaries?skip=${skip}&limit=${limit}`);
    }

    // Generate summaries
    async generateSummaries(): Promise<{ success: boolean; summaries_generated: number; message: string }> {
        return this.request('/summaries/generate', { method: 'POST' });
    }

    // Publish daily updates to X
    async publishDaily(): Promise<PublishResponse> {
        return this.request('/publish/daily', { method: 'POST' });
    }

    // Publish weekly report to Medium
    async publishWeekly(): Promise<PublishResponse> {
        return this.request('/publish/weekly', { method: 'POST' });
    }

    // Get daily report
    async getDailyReport(date?: string): Promise<DailyReportResponse> {
        const endpoint = date ? `/daily_report?date=${date}` : '/daily_report';
        return this.request(endpoint);
    }

    // Get weekly report
    async getWeeklyReport(): Promise<WeeklyReportResponse> {
        return this.request('/weekly_report');
    }
}

export const api = new ApiClient();
