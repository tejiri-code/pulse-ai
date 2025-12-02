interface TagChipProps {
    tag: string;
    onClick?: () => void;
    active?: boolean;
}

export default function TagChip({ tag, onClick, active = false }: TagChipProps) {
    const baseClasses = "inline-flex items-center px-3 py-1 rounded-full text-xs font-medium transition-all duration-200";
    const activeClasses = active
        ? "bg-blue-600 text-white border-blue-400"
        : "bg-blue-900/30 text-blue-300 border-blue-700/50 hover:bg-blue-900/50 hover:border-blue-600/70";
    const clickableClasses = onClick ? "cursor-pointer" : "";

    return (
        <span
            className={`${baseClasses} ${activeClasses} ${clickableClasses} border`}
            onClick={onClick}
        >
            {tag}
        </span>
    );
}
