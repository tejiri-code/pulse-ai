'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import SummaryCard from '@/components/SummaryCard';
import TagChip from '@/components/TagChip';
import type { Summary, SummaryResponse } from '@/types';
import { Filter, RefreshCw, Archive, X } from 'lucide-react';

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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                    <Archive className="w-10 h-10 text-emerald-400" />
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent">
                        Archive
                    </h1>
                </div>
                <p className="text-gray-400 text-lg">
                    Browse and filter all AI/ML news summaries
                </p>
            </div>

            {/* Filters */}
            <div className="mb-8 glass-panel p-6 rounded-2xl">
                <div className="flex items-center gap-2 mb-4">
                    <Filter className="w-5 h-5 text-blue-400" />
                    <h2 className="text-lg font-semibold text-white">Filters</h2>
                    {selectedTags.length > 0 && (
                        <span className="ml-2 bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full text-xs font-medium">
                            {selectedTags.length} active
                        </span>
                    )}
                </div>

                {/* Tag Filters */}
                <div className="mb-4">
                    <p className="text-sm text-gray-400 mb-3">Filter by topic:</p>
                    <div className="flex flex-wrap gap-2">
                        {getAllTags().map(tag => (
                            <TagChip
                                key={tag}
                                label={tag}
                                active={selectedTags.includes(tag)}
                                onClick={() => toggleTag(tag)}
                            />
                        ))}
                        {getAllTags().length === 0 && (
                            <p className="text-gray-500 text-sm italic">No tags available</p>
                        )}
                    </div>
                </div>

                {/* Clear Filters */}
                {selectedTags.length > 0 && (
                    <button
                        onClick={() => setSelectedTags([])}
                        className="flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300 transition-colors group"
                    >
                        <X className="w-4 h-4 group-hover:rotate-90 transition-transform" />
                        Clear all filters
                    </button>
                )}
            </div>

            {/* Results Header */}
            <div className="mb-6 flex items-center justify-between glass-panel p-4 rounded-xl">
                <p className="text-gray-400 font-medium">
                    Showing <span className="text-white font-bold">{filteredSummaries.length}</span> of <span className="text-white font-bold">{summaries.length}</span> items
                </p>
                <button
                    onClick={loadSummaries}
                    className="flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300 transition-colors group"
                >
                    <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
                    Refresh
                </button>
            </div>

            {/* Error Message */}
            {error && (
                <div className="mb-6 bg-red-500/10 border border-red-500/30 rounded-xl p-4">
                    <p className="text-red-400">{error}</p>
                </div>
            )}

            {/* Summaries Grid */}
            {loading ? (
                <div className="flex flex-col items-center justify-center py-24 space-y-4">
                    <div className="w-12 h-12 border-4 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin"></div>
                    <p className="text-gray-400 animate-pulse">Loading archive...</p>
                </div>
            ) : filteredSummaries.length === 0 ? (
                <div className="text-center py-24 glass-panel rounded-2xl">
                    <Archive className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <p className="text-gray-400 text-xl mb-2">No summaries match your filters</p>
                    {selectedTags.length > 0 && (
                        <button
                            onClick={() => setSelectedTags([])}
                            className="text-blue-400 hover:text-blue-300 text-sm transition-colors"
                        >
                            Clear filters to see all items
                        </button>
                    )}
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-8 pb-12">
                    {filteredSummaries.map((summary) => (
                        <SummaryCard key={summary.id} summary={summary} />
                    ))}
                </div>
            )}
        </div>
    );
}
