"use client";
import Link from 'next/link';
import { useState, useEffect } from 'react';

export default function Navbar() {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    return (
        <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    <div className="flex items-center space-x-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-xl">P</span>
                        </div>
                        <Link href="/" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                            Pulse AI Agent
                        </Link>
                    </div>

                    <div className="flex space-x-1">
                        <NavLink href="/" label="Dashboard" />
                        <NavLink href="/history" label="History" />
                        <NavLink href="/reports/daily" label="Daily" />
                        <NavLink href="/reports/weekly" label="Weekly" />
                        <NavLink href="/settings" label="Settings" />
                    </div>
                </div>
            </div>
        </nav>
    );
}

function NavLink({ href, label }: { href: string; label: string }) {
    return (
        <Link
            href={href}
            className="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
        >
            {label}
        </Link>
    );
}
