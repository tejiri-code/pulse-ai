"use client";
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, History, FileText, Newspaper, Settings, Zap } from 'lucide-react';
import { clsx } from 'clsx';

export default function Navbar() {
    const pathname = usePathname();

    return (
        <nav className="fixed top-2 sm:top-4 left-1/2 -translate-x-1/2 w-[98%] sm:w-[95%] max-w-7xl z-50 glass-panel rounded-xl sm:rounded-2xl px-3 sm:px-6 py-2 sm:py-3 transition-all duration-300 hover:bg-gray-900/80">
            <div className="flex justify-between items-center gap-2">
                <div className="flex items-center space-x-2 sm:space-x-3 flex-shrink-0">
                    <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg sm:rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
                        <Zap className="w-4 h-4 sm:w-6 sm:h-6 text-white fill-white" />
                    </div>
                    <Link href="/" className="text-base sm:text-xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
                        <span className="hidden xs:inline">Pulse AI</span>
                        <span className="xs:hidden">Pulse</span>
                    </Link>
                </div>

                <div className="flex items-center gap-0.5 sm:gap-1 bg-gray-900/50 p-0.5 sm:p-1 rounded-lg sm:rounded-xl border border-gray-800/50 overflow-x-auto">
                    <NavLink href="/" icon={<LayoutDashboard className="w-4 h-4" />} label="Dashboard" active={pathname === '/'} />
                    <NavLink href="/history" icon={<History className="w-4 h-4" />} label="History" active={pathname === '/history'} />
                    <NavLink href="/reports/daily" icon={<FileText className="w-4 h-4" />} label="Daily" active={pathname === '/reports/daily'} />
                    <NavLink href="/reports/weekly" icon={<Newspaper className="w-4 h-4" />} label="Weekly" active={pathname === '/reports/weekly'} />
                    <NavLink href="/settings" icon={<Settings className="w-4 h-4" />} label="Settings" active={pathname === '/settings'} />
                </div>
            </div>
        </nav>
    );
}

function NavLink({ href, icon, label, active }: { href: string; icon: React.ReactNode; label: string; active: boolean }) {
    return (
        <Link
            href={href}
            className={clsx(
                "flex items-center gap-1.5 sm:gap-2 px-2 sm:px-4 py-2 sm:py-2 rounded-md sm:rounded-lg text-xs sm:text-sm font-medium transition-all duration-200 whitespace-nowrap",
                active
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-500/25"
                    : "text-gray-400 hover:text-white hover:bg-gray-800"
            )}
        >
            {icon}
            <span className="hidden sm:inline">{label}</span>
        </Link>
    );
}
