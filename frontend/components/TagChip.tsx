import { clsx } from 'clsx';

interface TagChipProps {
    label: string;
    type?: 'category' | 'source' | 'sentiment' | 'default';
    onClick?: () => void;
    active?: boolean;
}

export default function TagChip({ label, type = 'default', onClick, active }: TagChipProps) {
    const styles = {
        category: "bg-purple-500/10 text-purple-400 border-purple-500/20 hover:shadow-[0_0_10px_rgba(168,85,247,0.4)]",
        source: "bg-blue-500/10 text-blue-400 border-blue-500/20 hover:shadow-[0_0_10px_rgba(59,130,246,0.4)]",
        sentiment: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 hover:shadow-[0_0_10px_rgba(16,185,129,0.4)]",
        default: "bg-gray-500/10 text-gray-400 border-gray-500/20 hover:shadow-[0_0_10px_rgba(156,163,175,0.4)]",
    };

    const activeStyle = "bg-blue-500 text-white border-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.5)]";

    return (
        <span
            onClick={onClick}
            className={clsx(
                "px-3 py-1 rounded-full text-xs font-medium border transition-all duration-300 select-none",
                onClick ? "cursor-pointer hover:-translate-y-0.5" : "cursor-default",
                active ? activeStyle : (styles[type] || styles.default)
            )}
        >
            {label}
        </span>
    );
}
