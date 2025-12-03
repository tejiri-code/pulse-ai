'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import SummaryCard from '@/components/SummaryCard';
import type { Summary, SummaryResponse } from '@/types';
import { RefreshCw, Mail, Sparkles, BarChart3, Calendar, ArrowRight, ArrowLeft, Edit3, Cloud } from 'lucide-react';
import { clsx } from 'clsx';

export default function Dashboard() {
  const [summaries, setSummaries] = useState<Summary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fetching, setFetching] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [sending, setSending] = useState(false);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [recipientEmail, setRecipientEmail] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    loadSummaries();
  }, [currentPage]);

  const loadSummaries = async () => {
    try {
      setLoading(true);
      setError(null);
      const skip = (currentPage - 1) * itemsPerPage;
      const response: SummaryResponse = await api.getSummaries(skip, itemsPerPage);
      setSummaries(response.summaries);
      setHasMore(response.summaries.length === itemsPerPage);
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

  const handlePublishToDevTo = async () => {
    try {
      setPublishing(true);
      const result = await api.publishDevTo();
      alert(`✅ ${result.message}`);
    } catch (err: any) {
      alert(`❌ Dev.to publish failed: ${err.message}`);
    } finally {
      setPublishing(false);
    }
  };

  const handlePublishToMastodon = async () => {
    try {
      setPublishing(true);
      const result = await api.publishMastodon();
      alert(`✅ ${result.message}`);
    } catch (err: any) {
      alert(`❌ Mastodon publish failed: ${err.message}`);
    } finally {
      setPublishing(false);
    }
  };

  const handleSendEmail = async () => {
    try {
      setSending(true);
      setError(null);

      if (!recipientEmail || !recipientEmail.includes('@')) {
        alert('⚠️ Please enter a valid email address');
        setSending(false);
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/email/daily-report?recipient=${encodeURIComponent(recipientEmail)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const result = await response.json();

      if (result.success) {
        alert(`✅ ${result.message}`);
        setShowEmailModal(false);
        setRecipientEmail('');
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="relative py-12 mb-12">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 blur-3xl -z-10 rounded-full opacity-50"></div>
        <div className="text-center space-y-4">
          <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-fade-in tracking-tight">
            Pulse AI Agent
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto font-light animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Autonomous intelligence curating the future of AI & Tech
          </p>
        </div>
      </div>

      {/* Action Bar */}
      <div className="glass-panel p-4 rounded-2xl mb-12 animate-slide-up flex flex-wrap gap-4 justify-center md:justify-between items-center" style={{ animationDelay: '0.2s' }}>
        <div className="flex gap-4">
          <ActionButton
            onClick={handleFetchNews}
            loading={fetching}
            icon={<RefreshCw className={clsx("w-5 h-5", fetching && "animate-spin")} />}
            label="Fetch News"
            variant="primary"
          />
        </div>

        <div className="flex gap-4">
          <ActionButton
            onClick={handlePublishToDevTo}
            loading={publishing}
            disabled={summaries.length === 0}
            icon={<Edit3 className="w-5 h-5" />}
            label="Publish to Dev.to"
            variant="secondary"
          />
          <ActionButton
            onClick={handlePublishToMastodon}
            loading={publishing}
            disabled={summaries.length === 0}
            icon={<Cloud className="w-5 h-5" />}
            label="Publish to Mastodon"
            variant="secondary"
          />
          <ActionButton
            onClick={() => setShowEmailModal(true)}
            disabled={summaries.length === 0}
            icon={<Mail className="w-5 h-5" />}
            label="Daily Report"
            variant="accent"
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 animate-slide-up" style={{ animationDelay: '0.3s' }}>
        <StatCard
          label="Total Insights"
          value={summaries.length}
          icon={<BarChart3 className="w-8 h-8 text-blue-400" />}
          trend="+12% this week"
        />
        <StatCard
          label="Today's Pulse"
          value={summaries.filter(s => isToday(s.created_date)).length}
          icon={<Calendar className="w-8 h-8 text-purple-400" />}
          trend="Active now"
        />
        <StatCard
          label="Novelty Score"
          value={`${calculateAvgNovelty(summaries)}%`}
          icon={<Sparkles className="w-8 h-8 text-pink-400" />}
          trend="High quality"
        />
      </div>

      {/* Content Grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 space-y-4">
          <div className="w-12 h-12 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
          <p className="text-gray-400 animate-pulse">Syncing with the matrix...</p>
        </div>
      ) : summaries.length === 0 ? (
        <div className="text-center py-24 glass-panel rounded-2xl">
          <p className="text-gray-400 text-xl mb-6">No insights generated yet.</p>
          <ActionButton
            onClick={handleFetchNews}
            loading={fetching}
            icon={<RefreshCw className="w-5 h-5" />}
            label="Initialize Scraper"
            variant="primary"
          />
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-8 animate-slide-up" style={{ animationDelay: '0.4s' }}>
          {summaries.map((summary) => (
            <SummaryCard key={summary.id} summary={summary} />
          ))}
        </div>
      )}

      {/* Pagination */}
      {summaries.length > 0 && (
        <div className="flex justify-center items-center gap-6 mt-12 mb-8">
          <button
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="glass-button p-3 rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:text-blue-400"
          >
            <ArrowLeft className="w-6 h-6" />
          </button>
          <span className="text-gray-400 font-mono">Page {currentPage}</span>
          <button
            onClick={() => setCurrentPage(prev => prev + 1)}
            disabled={!hasMore}
            className="glass-button p-3 rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:text-blue-400"
          >
            <ArrowRight className="w-6 h-6" />
          </button>
        </div>
      )}

      {/* Email Modal */}
      {showEmailModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in" onClick={() => setShowEmailModal(false)}>
          <div className="glass-panel p-8 rounded-2xl max-w-md w-full mx-4 transform transition-all scale-100" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold text-white mb-2">Subscribe to Daily Digest</h3>
            <p className="text-gray-400 mb-6">Get the latest AI insights delivered to your inbox.</p>

            <input
              type="email"
              placeholder="name@company.com"
              value={recipientEmail}
              onChange={(e) => setRecipientEmail(e.target.value)}
              className="w-full bg-gray-900/50 text-white border border-gray-700 rounded-xl px-4 py-3 mb-6 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
            />

            <div className="flex gap-4">
              <button
                onClick={handleSendEmail}
                disabled={sending || !recipientEmail}
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold py-3 px-6 rounded-xl transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {sending ? 'Sending...' : 'Subscribe'}
              </button>
              <button
                onClick={() => setShowEmailModal(false)}
                className="flex-1 glass-button text-gray-300 hover:text-white font-semibold py-3 px-6 rounded-xl"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function ActionButton({ onClick, loading, disabled, icon, label, variant }: any) {
  const variants = {
    primary: "bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 shadow-blue-500/25",
    secondary: "bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 shadow-purple-500/25",
    accent: "bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 shadow-emerald-500/25",
  };

  return (
    <button
      onClick={onClick}
      disabled={loading || disabled}
      className={clsx(
        "flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-white transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-none",
        variants[variant as keyof typeof variants]
      )}
    >
      {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : icon}
      <span>{loading ? 'Processing...' : label}</span>
    </button>
  );
}

function StatCard({ label, value, icon, trend }: any) {
  return (
    <div className="glass-panel p-6 rounded-2xl hover:bg-gray-800/50 transition-colors group">
      <div className="flex justify-between items-start mb-4">
        <div className="p-3 bg-gray-900/50 rounded-xl group-hover:scale-110 transition-transform duration-300">
          {icon}
        </div>
        <span className="text-xs font-medium text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-full border border-emerald-500/20">
          {trend}
        </span>
      </div>
      <div className="space-y-1">
        <h3 className="text-3xl font-bold text-white">{value}</h3>
        <p className="text-gray-400 text-sm">{label}</p>
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
  return 85; // Placeholder for now
}
