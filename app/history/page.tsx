'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import SummaryCard from '@/components/SummaryCard';
import TagChip from '@/components/TagChip';
import type { Summary, SummaryResponse } from '@/types';

export default function HistoryPage() {
    const [summaries, setSummaries] = useState<Summary[]>([]);
    const [filteredSummaries, setFilteredSummaries] = useState<Summary[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [selectedSource, setSelectedSource] = useState<string>('all');

    useEffect(() => {
        loadSummaries();
    }, []);

    useEffect(() => {
        filterSummaries();
    }, [summaries, selectedTags, selectedSource]);

    const loadSummaries = async () => {
        try {
            setLoading(true);
            setError(null);
            const response: SummaryResponse = await api.getSummaries(0, 100);
            setSummaries(response.summaries);
        } catch (err) {
            setError('Failed to load summaries');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const filterSummaries = () => {
        let filtered = summaries;

        // Filter by tags
        if (selectedTags.length > 0) {
            filtered = filtered.filter(summary =>
                selectedTags.some(tag => summary.tags.includes(tag))
            );
        }

        // Filter by source (would need news_item data from backend)
        // For now just showing all

        setFilteredSummaries(filtered);
    };

    const getAllTags = (): string[] => {
        const tagSet = new Set<string>();
        summaries.forEach(summary => {
            summary.tags.forEach(tag => tagSet.add(tag));
        });
        return Array.from(tagSet).sort();
    };

    const toggleTag = (tag: string) => {
        setSelectedTags(prev =>
            prev.includes(tag)
                ? prev.filter(t => t !== tag)
                : [...prev, tag]
        );
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold bg-gradient-to-r from-green-400 via-teal-400 to-blue-400 bg-clip-text text-transparent mb-2">
                        News Archive
                    </h1>
                    <p className="text-gray-400">
                        Browse and filter all AI/ML news summaries
                    </p>
                </div>

                {/* Filters */}
                <div className="mb-8 bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                    <h2 className="text-lg font-semibold text-white mb-4">Filters</h2>

                    {/* Tag Filters */}
                    <div className="mb-4">
                        <p className="text-sm text-gray-400 mb-2">Tags:</p>
                        <div className="flex flex-wrap gap-2">
                            {getAllTags().map(tag => (
                                <TagChip
                                    key={tag}
                                    tag={tag}
                                    active={selectedTags.includes(tag)}
                                    onClick={() => toggleTag(tag)}
                                />
                            ))}
                            {getAllTags().length === 0 && (
                                <p className="text-gray-500 text-sm">No tags available</p>
                            )}
                        </div>
                    </div>

                    {/* Clear Filters */}
                    {selectedTags.length > 0 && (
                        <button
                            onClick={() => setSelectedTags([])}
                            className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
                        >
                            Clear all filters
                        </button>
                    )}
                </div>

                {/* Results Count */}
                <div className="mb-4 flex items-center justify-between">
                    <p className="text-gray-400">
                        Showing {filteredSummaries.length} of {summaries.length} items
                    </p>
                    <button
                        onClick={loadSummaries}
                        className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
                    >
                        🔄 Refresh
                    </button>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="mb-6 bg-red-900/30 border border-red-700 rounded-lg p-4">
                        <p className="text-red-400">{error}</p>
                    </div>
                )}

                {/* Summaries Grid */}
                {loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
                        <p className="mt-4 text-gray-400">Loading history...</p>
                    </div>
                ) : filteredSummaries.length === 0 ? (
                    <div className="text-center py-12 bg-gray-800/30 rounded-lg border border-gray-700">
                        <p className="text-gray-400 text-lg">No summaries match your filters</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 gap-6">
                        {filteredSummaries.map((summary) => (
                            <SummaryCard key={summary.id} summary={summary} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
