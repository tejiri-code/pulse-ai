'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import type { WeeklyReportResponse } from '@/types';
import { Calendar, FileText, ExternalLink, RefreshCw, Printer, TrendingUp } from 'lucide-react';

export default function WeeklyReportPage() {
    const [report, setReport] = useState<WeeklyReportResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadReport();
    }, []);

    const loadReport = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await api.getWeeklyReport();
            setReport(response);
        } catch (err) {
            setError('Failed to load weekly report');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-5xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8">
            {/* Header */}
            <div className="mb-6 sm:mb-8">
                <div className="flex items-center gap-2 sm:gap-3 mb-2">
                    <TrendingUp className="w-8 h-8 sm:w-10 sm:h-10 text-violet-400" />
                    <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                        Weekly Deep Dive
                    </h1>
                </div>
                <p className="text-gray-400 text-sm sm:text-base md:text-lg">
                    Comprehensive weekly analysis and insights
                </p>
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
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
                    <p className="mt-4 text-gray-400">Loading report...</p>
                </div>
            ) : report ? (
                <div>
                    {/* Report Header */}
                    <div className="mb-6 sm:mb-8 glass-panel p-5 sm:p-6 md:p-8 rounded-xl sm:rounded-2xl bg-gradient-to-br from-indigo-500/5 to-purple-500/5">
                        <h2 className="text-2xl sm:text-2xl md:text-3xl font-bold text-white mb-3 sm:mb-4">
                            {report.report.title}
                        </h2>
                        <div className="flex flex-col sm:flex-row sm:flex-wrap items-start sm:items-center gap-3 sm:gap-4 md:gap-6 text-gray-300 mb-3 sm:mb-4">
                            <div className="flex items-center gap-2">
                                <Calendar className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-400" />
                                <span className="text-xs sm:text-sm text-gray-400">From:</span>
                                <span className="font-medium text-sm sm:text-base">{new Date(report.report.week_start).toLocaleDateString()}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Calendar className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-purple-400" />
                                <span className="text-xs sm:text-sm text-gray-400">To:</span>
                                <span className="font-medium text-sm sm:text-base">{new Date(report.report.week_end).toLocaleDateString()}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <FileText className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-pink-400" />
                                <span className="text-xs sm:text-sm text-gray-400">Articles:</span>
                                <span className="font-bold text-white text-sm sm:text-base">{report.summaries_count}</span>
                            </div>
                        </div>

                        {report.report.medium_draft_url && (
                            <a
                                href={report.report.medium_draft_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors font-medium text-sm sm:text-base"
                            >
                                <ExternalLink className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                                View on Medium
                            </a>
                        )}
                    </div>

                    {/* Status Badge */}
                    <div className="mb-6">
                        <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${report.report.published
                            ? 'bg-green-900/30 text-green-400 border border-green-700'
                            : 'bg-yellow-900/30 text-yellow-400 border border-yellow-700'
                            }`}>
                            {report.report.published ? '✅ Published to Medium' : '📝 Draft Mode'}
                        </span>
                    </div>

                    {/* Article Content */}
                    <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg border border-gray-700 overflow-hidden">
                        <div className="bg-gradient-to-r from-indigo-600/20 to-purple-600/20 px-8 py-4 border-b border-gray-700">
                            <h3 className="text-lg font-semibold text-white">Article Content</h3>
                        </div>

                        <div className="p-8">
                            <article className="prose prose-invert prose-lg max-w-none">
                                <div
                                    className="markdown-content"
                                    dangerouslySetInnerHTML={{
                                        __html: formatMarkdown(report.report.content)
                                    }}
                                />
                            </article>
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="mt-6 sm:mt-8 flex flex-col sm:flex-row gap-3 sm:gap-4">
                        <button
                            onClick={loadReport}
                            className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold py-2.5 sm:py-3 px-4 sm:px-6 rounded-xl transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/25 flex items-center justify-center gap-2 hover:-translate-y-0.5 text-sm sm:text-base min-h-[44px]"
                        >
                            <RefreshCw className="w-4 h-4 sm:w-5 sm:h-5" />
                            Refresh Report
                        </button>

                        <button
                            onClick={() => window.print()}
                            className="glass-button text-white font-semibold py-2.5 sm:py-3 px-4 sm:px-6 rounded-xl flex items-center justify-center gap-2 text-sm sm:text-base min-h-[44px]"
                        >
                            <Printer className="w-4 h-4 sm:w-5 sm:h-5" />
                            Print
                        </button>
                    </div>
                </div>
            ) : (
                <div className="text-center py-12 bg-gray-800/30 rounded-lg border border-gray-700">
                    <p className="text-gray-400 text-lg mb-4">No weekly report available yet</p>
                    <p className="text-gray-500 text-sm">Weekly reports are generated every Monday</p>
                </div>
            )}
        </div>
    );
}

// Simple markdown formatter (for demonstration)
function formatMarkdown(markdown: string): string {
    return markdown
        .replace(/^### (.*$)/gim, '<h3 class="text-xl font-bold text-white mt-6 mb-3">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold text-white mt-8 mb-4">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold text-white mt-10 mb-5">$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-white">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
        .replace(/^---$/gim, '<hr class="my-6 border-gray-700">')
        .replace(/\n\n/g, '</p><p class="text-gray-300 mb-4">')
        .replace(/^(.+)$/gim, '<p class="text-gray-300 mb-4">$1</p>');
}
