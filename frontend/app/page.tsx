'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import SummaryCard from '@/components/SummaryCard';
import type { Summary, SummaryResponse } from '@/types';

export default function Dashboard() {
  const [summaries, setSummaries] = useState<Summary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fetching, setFetching] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    loadSummaries();
  }, []);

  const loadSummaries = async () => {
    try {
      setLoading(true);
      setError(null);
      const response: SummaryResponse = await api.getSummaries(0, 20);
      setSummaries(response.summaries);
    } catch (err) {
      setError('Failed to load summaries');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchNews = async () => {
    try {
      setFetching(true);
      setError(null);
      const scrapeResult = await api.fetchNews();
      await api.generateSummaries();
      await loadSummaries();
      alert(`✅ Successfully scraped ${scrapeResult.items_new} new items!`);
    } catch (err) {
      setError('Failed to fetch news');
      console.error(err);
    } finally {
      setFetching(false);
    }
  };

  const handlePublishToX = async () => {
    try {
      setPublishing(true);
      setError(null);
      const result = await api.publishDaily();
      const mode = result.mock_mode ? ' (MOCK MODE)' : '';
      alert(`✅ Published ${result.posts_created} posts to X${mode}`);
    } catch (err) {
      setError('Failed to publish to X');
      console.error(err);
    } finally {
      setPublishing(false);
    }
  };

  const handlePublishToMedium = async () => {
    try {
      setPublishing(true);
      setError(null);
      const result = await api.publishWeekly();
      const mode = result.mock_mode ? ' (MOCK MODE)' : '';
      alert(`✅ Published weekly report to Medium${mode}`);
    } catch (err) {
      setError('Failed to publish to Medium');
      console.error(err);
    } finally {
      setPublishing(false);
    }
  };

  const handleSendEmail = async () => {
    try {
      setSending(true);
      setError(null);

      // Call backend endpoint to send email via ZeptoMail
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/email/daily-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const result = await response.json();

      if (result.success) {
        alert(`✅ ${result.message}`);
      } else {
        throw new Error(result.message || 'Failed to send email');
      }

    } catch (err: any) {
      setError('Failed to send email');
      console.error(err);
      alert(`❌ Failed to send email: ${err.message}`);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
            AI News Dashboard
          </h1>
          <p className="text-gray-400">
            Real-time AI/ML news curated by your autonomous agent
          </p>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <button
            onClick={handleFetchNews}
            disabled={fetching}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/50"
          >
            {fetching ? '⏳ Fetching...' : '🔄 Fetch Latest News'}
          </button>

          <button
            onClick={handlePublishToX}
            disabled={publishing || summaries.length === 0}
            className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 hover:shadow-lg hover:shadow-purple-500/50"
          >
            {publishing ? '⏳ Publishing...' : '🐦 Publish to X'}
          </button>

          <button
            onClick={handlePublishToMedium}
            disabled={publishing || summaries.length === 0}
            className="bg-pink-600 hover:bg-pink-700 disabled:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 hover:shadow-lg hover:shadow-pink-500/50"
          >
            {publishing ? '⏳ Publishing...' : '📝 Publish to Medium'}
          </button>

          <button
            onClick={handleSendEmail}
            disabled={sending || summaries.length === 0}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 hover:shadow-lg hover:shadow-green-500/50"
          >
            {sending ? '⏳ Sending...' : '📧 Send Daily Email'}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-900/30 border border-red-700 rounded-lg p-4">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            label="Total Summaries"
            value={summaries.length}
            icon="📊"
            gradient="from-blue-500 to-cyan-500"
          />
          <StatCard
            label="Today's Items"
            value={summaries.filter(s => isToday(s.created_date)).length}
            icon="📅"
            gradient="from-purple-500 to-pink-500"
          />
          <StatCard
            label="Avg Novelty"
            value={`${calculateAvgNovelty(summaries)}%`}
            icon="✨"
            gradient="from-pink-500 to-orange-500"
          />
        </div>

        {/* Summaries Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <p className="mt-4 text-gray-400">Loading summaries...</p>
          </div>
        ) : summaries.length === 0 ? (
          <div className="text-center py-12 bg-gray-800/30 rounded-lg border border-gray-700">
            <p className="text-gray-400 text-lg mb-4">No summaries yet</p>
            <button
              onClick={handleFetchNews}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Fetch Your First News
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {summaries.map((summary) => (
              <SummaryCard key={summary.id} summary={summary} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value, icon, gradient }: { label: string; value: number | string; icon: string; gradient: string }) {
  return (
    <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm mb-1">{label}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
        </div>
        <div className={`text-4xl bg-gradient-to-br ${gradient} w-16 h-16 rounded-lg flex items-center justify-center`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function isToday(dateString: string): boolean {
  const date = new Date(dateString);
  const today = new Date();
  return date.toDateString() === today.toDateString();
}

function calculateAvgNovelty(summaries: Summary[]): number {
  if (summaries.length === 0) return 0;
  // This would need to be calculated from the news items
  return 75; // Placeholder
}
