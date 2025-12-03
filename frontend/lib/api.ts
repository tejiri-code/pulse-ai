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
        // Get API keys from localStorage if available
        const apiKeys = this.getStoredApiKeys();

        const response = await fetch(`${this.baseUrl}/publish/daily`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(apiKeys)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        return response.json();
    }

    // Publish weekly report to Medium
    async publishWeekly(): Promise<PublishResponse> {
        // Get API keys from localStorage if available
        const apiKeys = this.getStoredApiKeys();

        const response = await fetch(`${this.baseUrl}/publish/weekly`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(apiKeys)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        return response.json();
    }

    private getStoredApiKeys(): Record<string, string> {
        // Get API keys from localStorage (client-side only)
        if (typeof window === 'undefined') return {};

        const savedKeys = localStorage.getItem('apiKeys');
        if (!savedKeys) return {};

        try {
            return JSON.parse(savedKeys);
        } catch {
            return {};
        }
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

    // Publish to Bluesky
    async publishBluesky(): Promise<PublishResponse> {
        const apiKeys = this.getStoredApiKeys();
        const response = await fetch(`${this.baseUrl}/publish/bluesky`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(apiKeys)
        });
        if (!response.ok) throw new Error('Bluesky publish failed');
        return response.json();
    }

    // Publish to LinkedIn
    async publishLinkedIn(): Promise<PublishResponse> {
        const apiKeys = this.getStoredApiKeys();
        const response = await fetch(`${this.baseUrl}/publish/linkedin`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(apiKeys)
        });
        if (!response.ok) throw new Error('LinkedIn publish failed');
        return response.json();
    }

    // Publish to Dev.to
    async publishDevTo(): Promise<PublishResponse> {
        const apiKeys = this.getStoredApiKeys();
        const response = await fetch(`${this.baseUrl}/publish/devto`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(apiKeys)
        });
        if (!response.ok) throw new Error('Dev.to publish failed');
        return response.json();
    }

    // Publish to Mastodon
    async publishMastodon(): Promise<PublishResponse> {
        const apiKeys = this.getStoredApiKeys();
        const response = await fetch(`${this.baseUrl}/publish/mastodon`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(apiKeys)
        });
        if (!response.ok) throw new Error('Mastodon publish failed');
        return response.json();
    }

    // Subscribe to daily emails
    async subscribeEmail(email: string): Promise<{ success: boolean; message: string }> {
        const response = await fetch(`${this.baseUrl}/subscribe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        if (!response.ok) throw new Error('Subscription failed');
        return response.json();
    }

    // Unsubscribe from daily emails
    async unsubscribeEmail(email: string): Promise<{ success: boolean; message: string }> {
        const response = await fetch(`${this.baseUrl}/subscribe/${email}`, {
            method: 'DELETE',
        });
        if (!response.ok) throw new Error('Unsubscribe failed');
        return response.json();
    }
}

export const api = new ApiClient();
