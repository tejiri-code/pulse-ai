import type { Summary } from '@/types';
import TagChip from './TagChip';
import { ExternalLink, Sparkles, Calendar, Share2, Hash } from 'lucide-react';

interface SummaryCardProps {
    summary: Summary;
    newsTitle?: string;
    newsUrl?: string;
    noveltyScore?: number;
}

export default function SummaryCard({ summary, newsTitle, newsUrl, noveltyScore }: SummaryCardProps) {
    return (
        <div className="glass-panel rounded-xl p-6 transition-all duration-300 hover:shadow-[0_0_20px_rgba(139,92,246,0.15)] hover:-translate-y-1 group">
            {/* Header */}
            <div className="flex items-start justify-between mb-4 gap-4">
                <div className="flex-1">
                    {newsTitle && newsUrl ? (
                        <a
                            href={newsUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 hover:from-blue-300 hover:to-purple-300 transition-all duration-300 flex items-center gap-2 group-hover:underline decoration-blue-500/30 underline-offset-4"
                        >
                            {newsTitle}
                            <ExternalLink className="w-4 h-4 text-gray-500 group-hover:text-blue-400 transition-colors" />
                        </a>
                    ) : (
                        <span className="text-lg font-bold text-gray-200">News Summary</span>
                    )}
                </div>

                {noveltyScore !== undefined && (
                    <div className="flex flex-col items-end">
                        <div className="flex items-center gap-1.5 bg-gray-900/50 px-2 py-1 rounded-lg border border-gray-800">
                            <Sparkles className={`w-3.5 h-3.5 ${getNoveltyColor(noveltyScore)}`} />
                            <span className={`text-sm font-bold ${getNoveltyColor(noveltyScore)}`}>
                                {(noveltyScore * 100).toFixed(0)}%
                            </span>
                        </div>
                        <span className="text-[10px] text-gray-500 mt-1 uppercase tracking-wider font-medium">Novelty</span>
                    </div>
                )}
            </div>

            {/* Summary */}
            <div className="mb-5 relative">
                <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-500/50 to-transparent rounded-full"></div>
                <p className="text-gray-300 text-sm leading-relaxed pl-4 font-light tracking-wide">
                    {summary.three_sentence_summary}
                </p>
            </div>

            {/* Social Hook */}
            <div className="bg-gradient-to-r from-gray-900/80 to-gray-900/40 rounded-lg p-4 mb-5 border border-gray-800/50 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-2 opacity-10">
                    <Share2 className="w-12 h-12 text-white" />
                </div>
                <p className="text-xs text-blue-400 mb-2 uppercase tracking-wider font-semibold flex items-center gap-2">
                    <Share2 className="w-3 h-3" /> Social Hook
                </p>
                <p className="text-sm text-gray-200 italic font-medium border-l-2 border-blue-500/30 pl-3">
                    "{summary.social_hook}"
                </p>
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-800/50">
                <div className="flex flex-wrap gap-2">
                    {summary.tags.map((tag, index) => (
                        <TagChip key={index} label={tag} type="category" />
                    ))}
                </div>

                <div className="flex items-center gap-4 text-xs text-gray-500 font-mono">
                    <div className="flex items-center gap-1.5">
                        <Calendar className="w-3 h-3" />
                        <span>{new Date(summary.created_date).toLocaleDateString()}</span>
                    </div>
                    <div className="flex items-center gap-1.5" title="Summary ID">
                        <Hash className="w-3 h-3" />
                        <span>{summary.id || 'N/A'}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

function getNoveltyColor(score: number): string {
    if (score >= 0.8) return 'text-emerald-400';
    if (score >= 0.5) return 'text-amber-400';
    return 'text-rose-400';
}
