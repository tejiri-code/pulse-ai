import type { Summary } from '@/types';

interface SummaryCardProps {
    summary: Summary;
    newsTitle?: string;
    newsUrl?: string;
    noveltyScore?: number;
}

export default function SummaryCard({ summary, newsTitle, newsUrl, noveltyScore }: SummaryCardProps) {
    return (
        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-lg p-6 hover:border-blue-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10">
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                    {newsTitle && newsUrl && (
                        <a
                            href={newsUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-lg font-semibold text-blue-400 hover:text-blue-300 transition-colors line-clamp-2"
                        >
                            {newsTitle}
                        </a>
                    )}
                </div>
                {noveltyScore !== undefined && (
                    <div className="ml-4 flex-shrink-0">
                        <div className="flex flex-col items-center">
                            <span className="text-xs text-gray-400 mb-1">Novelty</span>
                            <span className={`text-sm font-bold ${getNoveltyColor(noveltyScore)}`}>
                                {(noveltyScore * 100).toFixed(0)}%
                            </span>
                        </div>
                    </div>
                )}
            </div>

            {/* Summary */}
            <p className="text-gray-300 text-sm leading-relaxed mb-4">
                {summary.three_sentence_summary}
            </p>

            {/* Social Hook */}
            <div className="bg-gray-900/50 rounded-md p-3 mb-4 border border-gray-700">
                <p className="text-xs text-gray-400 mb-1">Social Hook:</p>
                <p className="text-sm text-gray-200 italic">{summary.social_hook}</p>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mb-3">
                {summary.tags.map((tag, index) => (
                    <TagChip key={index} tag={tag} />
                ))}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{new Date(summary.created_date).toLocaleDateString()}</span>
                <span>ID: {summary.id || 'N/A'}</span>
            </div>
        </div>
    );
}

function TagChip({ tag }: { tag: string }) {
    return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/30 text-blue-300 border border-blue-700/50">
            {tag}
        </span>
    );
}

function getNoveltyColor(score: number): string {
    if (score >= 0.8) return 'text-green-400';
    if (score >= 0.5) return 'text-yellow-400';
    return 'text-orange-400';
}
