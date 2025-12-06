'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import SummaryCard from '@/components/SummaryCard';
import AudioPlayer from '@/components/AudioPlayer';
import type { DailyReportResponse } from '@/types';
import { Calendar, FileText, Tag, CheckCircle, FileEdit, Sun } from 'lucide-react';

export default function DailyReportPage() {
    const [report, setReport] = useState<DailyReportResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedDate, setSelectedDate] = useState<string>('');
    const [elevenlabsApiKey, setElevenlabsApiKey] = useState<string>('');

    useEffect(() => {
        // Load ElevenLabs API key from localStorage
        const savedKeys = localStorage.getItem('apiKeys');
        if (savedKeys) {
            const keys = JSON.parse(savedKeys);
            setElevenlabsApiKey(keys.elevenlabsApiKey || '');
        }
    }, []);

    useEffect(() => {
        loadReport();
    }, [selectedDate]);

    const loadReport = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await api.getDailyReport(selectedDate || undefined);
            setReport(response);
        } catch (err) {
            setError('Failed to load daily report');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8">
            {/* Header */}
            <div className="mb-6 sm:mb-8">
                <div className="flex items-center gap-2 sm:gap-3 mb-2">
                    <Sun className="w-8 h-8 sm:w-10 sm:h-10 text-amber-400" />
                    <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-amber-400 via-orange-400 to-red-400 bg-clip-text text-transparent">
                        Daily Brief
                    </h1>
                </div>
                <p className="text-gray-400 text-sm sm:text-base md:text-lg">
                    Your daily digest of AI/ML developments
                </p>
            </div>

            {/* Date Selector */}
            <div className="mb-6 sm:mb-8 glass-panel p-4 sm:p-5 md:p-6 rounded-xl sm:rounded-2xl">
                <label className="block text-xs sm:text-sm font-medium text-gray-300 mb-2 sm:mb-3 flex items-center gap-2">
                    <Calendar className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-400" />
                    Select Date:
                </label>
                <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 items-stretch sm:items-center">
                    <input
                        type="date"
                        value={selectedDate}
                        onChange={(e) => setSelectedDate(e.target.value)}
                        className="flex-1 bg-gray-900/50 border border-gray-700 rounded-xl px-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all min-h-[44px]"
                    />
                    <button
                        onClick={() => setSelectedDate('')}
                        className="text-xs sm:text-sm text-blue-400 hover:text-blue-300 transition-colors font-medium py-2.5 sm:py-0 min-h-[44px] sm:min-h-0"
                    >
                        Today
                    </button>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="mb-6 bg-red-900/30 border border-red-700 rounded-lg p-4">
                    <p className="text-red-400">{error}</p>
                </div>
            )}

            {/* Report Content */}
            {loading ? (
                <div className="text-center py-12">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500"></div>
                    <p className="mt-4 text-gray-400">Loading report...</p>
                </div>
            ) : report ? (
                <div>
                    {/* Report Header */}
                    <div className="mb-8 bg-gradient-to-r from-yellow-900/30 to-orange-900/30 rounded-lg p-6 border border-yellow-700/50">
                        <h2 className="text-2xl font-bold text-white mb-2">
                            {report.report.title}
                        </h2>
                        <p className="text-gray-300">
                            {new Date(report.report.date).toLocaleDateString('en-US', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                            })}
                        </p>
                    </div>

                    {/* Audio Podcast Player */}
                    <div className="mb-8">
                        <AudioPlayer
                            reportType="daily"
                            date={selectedDate || undefined}
                            apiKey={elevenlabsApiKey}
                        />
                    </div>

                    {/* Report Stats */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5 md:gap-6 mb-6 sm:mb-8">
                        <StatCard
                            label="Items Covered"
                            value={report.summaries.length}
                            icon="📰"
                        />
                        <StatCard
                            label="Unique Tags"
                            value={getUniqueTags(report.summaries).length}
                            icon="🏷️"
                        />
                        <StatCard
                            label="Status"
                            value={report.report.sent ? 'Sent' : 'Draft'}
                            icon={report.report.sent ? '✅' : '📝'}
                        />
                    </div>

                    {/* Summaries */}
                    <div className="mb-8">
                        <h3 className="text-xl font-semibold text-white mb-4">
                            Today's Highlights
                        </h3>
                        <div className="grid grid-cols-1 gap-6">
                            {report.summaries.map((summary) => (
                                <SummaryCard key={summary.id} summary={summary} />
                            ))}
                        </div>
                    </div>

                    {/* Email Preview */}
                    <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                        <h3 className="text-xl font-semibold text-white mb-4">
                            Email Brief Preview
                        </h3>
                        <div className="prose prose-invert max-w-none">
                            <pre className="whitespace-pre-wrap text-sm text-gray-300 bg-gray-900/50 p-4 rounded-lg overflow-x-auto">
                                {report.report.content}
                            </pre>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="text-center py-12 bg-gray-800/30 rounded-lg border border-gray-700">
                    <p className="text-gray-400 text-lg">No report available for this date</p>
                </div>
            )}
        </div>
    );
}

function StatCard({ label, value, icon }: { label: string; value: number | string; icon: string }) {
    return (
        <div className="glass-panel p-4 sm:p-5 md:p-6 rounded-xl sm:rounded-2xl hover:bg-gray-800/50 transition-colors">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-gray-400 text-xs sm:text-sm mb-1">{label}</p>
                    <p className="text-2xl sm:text-2xl md:text-3xl font-bold text-white">{value}</p>
                </div>
                <div className="text-3xl sm:text-4xl">{icon}</div>
            </div>
        </div>
    );
}

function getUniqueTags(summaries: any[]): string[] {
    const tagSet = new Set<string>();
    summaries.forEach(summary => {
        summary.tags.forEach((tag: string) => tagSet.add(tag));
    });
    return Array.from(tagSet);
}
