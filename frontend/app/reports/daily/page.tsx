'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import SummaryCard from '@/components/SummaryCard';
import type { DailyReportResponse } from '@/types';
import { Calendar, FileText, Tag, CheckCircle, FileEdit, Sun } from 'lucide-react';

export default function DailyReportPage() {
    const [report, setReport] = useState<DailyReportResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedDate, setSelectedDate] = useState<string>('');

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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                    <Sun className="w-10 h-10 text-amber-400" />
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-amber-400 via-orange-400 to-red-400 bg-clip-text text-transparent">
                        Daily Brief
                    </h1>
                </div>
                <p className="text-gray-400 text-lg">
                    Your daily digest of AI/ML developments
                </p>
            </div>

            {/* Date Selector */}
            <div className="mb-8 glass-panel p-6 rounded-2xl">
                <label className="block text-sm font-medium text-gray-300 mb-3 flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-blue-400" />
                    Select Date:
                </label>
                <div className="flex gap-4 items-center">
                    <input
                        type="date"
                        value={selectedDate}
                        onChange={(e) => setSelectedDate(e.target.value)}
                        className="bg-gray-900/50 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                    />
                    <button
                        onClick={() => setSelectedDate('')}
                        className="text-sm text-blue-400 hover:text-blue-300 transition-colors font-medium"
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

                    {/* Report Stats */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
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
        <div className="glass-panel p-6 rounded-2xl hover:bg-gray-800/50 transition-colors">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-gray-400 text-sm mb-1">{label}</p>
                    <p className="text-3xl font-bold text-white">{value}</p>
                </div>
                <div className="text-4xl">{icon}</div>
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
