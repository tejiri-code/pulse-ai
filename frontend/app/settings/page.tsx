'use client';

import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Save, Trash2, Cloud, Edit3, CheckCircle, Key } from 'lucide-react';

interface ApiKeys {
    devtoApiKey: string;
    mastodonAccessToken: string;
    mastodonInstance: string;
}

export default function SettingsPage() {
    const [keys, setKeys] = useState<ApiKeys>({
        devtoApiKey: '',
        mastodonAccessToken: '',
        mastodonInstance: 'https://mastodon.social'
    });
    const [saved, setSaved] = useState(false);

    useEffect(() => {
        const savedKeys = localStorage.getItem('apiKeys');
        if (savedKeys) {
            setKeys(JSON.parse(savedKeys));
        }
    }, []);

    const handleSave = () => {
        localStorage.setItem('apiKeys', JSON.stringify(keys));
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
    };

    const handleClear = () => {
        setKeys({
            devtoApiKey: '',
            mastodonAccessToken: '',
            mastodonInstance: 'https://mastodon.social'
        });
        localStorage.removeItem('apiKeys');
    };

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                    <SettingsIcon className="w-10 h-10 text-blue-400" />
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                        Settings
                    </h1>
                </div>
                <p className="text-gray-400 text-lg">
                    Configure your FREE platform credentials — zero subscription fees
                </p>
            </div>

            {/* Success Message */}
            {saved && (
                <div className="mb-6 glass-panel p-4 rounded-xl border-emerald-500/30 bg-emerald-500/10 animate-slide-up">
                    <div className="flex items-center gap-2 text-emerald-400">
                        <CheckCircle className="w-5 h-5" />
                        <p className="font-medium">Settings saved successfully!</p>
                    </div>
                </div>
            )}


            {/* Dev.to */}
            <div className="glass-panel p-6 rounded-2xl mb-6">
                <div className="flex items-center gap-3 mb-4">
                    <Edit3 className="w-8 h-8 text-purple-400" />
                    <h2 className="text-2xl font-bold text-white">
                        Dev.to
                    </h2>
                    <span className="ml-auto bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                        Free
                    </span>
                </div>
                <p className="text-gray-400 mb-4 text-sm">
                    Get API key: <a href="https://dev.to/settings/extensions" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline underline-offset-2">Dev.to Settings</a> → Generate API Key
                </p>

                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center gap-2">
                        <Key className="w-4 h-4 text-gray-500" />
                        API Key
                    </label>
                    <input
                        type="password"
                        value={keys.devtoApiKey}
                        onChange={(e) => setKeys({ ...keys, devtoApiKey: e.target.value })}
                        placeholder="Enter Dev.to API key"
                        className="w-full bg-gray-900/50 text-white border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                    />
                </div>
            </div>

            {/* Mastodon */}
            <div className="glass-panel p-6 rounded-2xl mb-6">
                <div className="flex items-center gap-3 mb-4">
                    <Cloud className="w-8 h-8 text-violet-400" />
                    <h2 className="text-2xl font-bold text-white">
                        Mastodon
                    </h2>
                    <span className="ml-auto bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                        Free
                    </span>
                </div>
                <p className="text-gray-400 mb-4 text-sm">
                    Get access token: <a href="https://mastodon.social/settings/applications" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline underline-offset-2">Mastodon Settings</a> → New Application → Copy Token
                </p>

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center gap-2">
                            <Key className="w-4 h-4 text-gray-500" />
                            Access Token
                        </label>
                        <input
                            type="password"
                            value={keys.mastodonAccessToken}
                            onChange={(e) => setKeys({ ...keys, mastodonAccessToken: e.target.value })}
                            placeholder="Enter Mastodon access token"
                            className="w-full bg-gray-900/50 text-white border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center gap-2">
                            <Cloud className="w-4 h-4 text-gray-500" />
                            Instance URL (Optional)
                        </label>
                        <input
                            type="text"
                            value={keys.mastodonInstance}
                            onChange={(e) => setKeys({ ...keys, mastodonInstance: e.target.value })}
                            placeholder="https://mastodon.social"
                            className="w-full bg-gray-900/50 text-white border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                        />
                        <p className="text-xs text-gray-500 mt-1">Default: https://mastodon.social</p>
                    </div>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mb-6">
                <button
                    onClick={handleSave}
                    className="flex-1 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/25 flex items-center justify-center gap-2 hover:-translate-y-0.5"
                >
                    <Save className="w-5 h-5" />
                    Save Settings
                </button>
                <button
                    onClick={handleClear}
                    className="bg-red-600 hover:bg-red-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 flex items-center justify-center gap-2"
                >
                    <Trash2 className="w-5 h-5" />
                    Clear All
                </button>
            </div>

            {/* Info Box */}
            <div className="glass-panel bg-blue-500/5 border-blue-500/20 p-5 rounded-2xl">
                <div className="flex gap-3">
                    <Cloud className="w-6 h-6 text-blue-400 flex-shrink-0 mt-0.5" />
                    <div>
                        <p className="text-sm text-blue-300 font-medium mb-1">
                            100% FREE Platforms
                        </p>
                        <p className="text-sm text-gray-400">
                            Dev.to and Mastodon both have free APIs.
                            Your keys are stored locally in your browser and only used when you publish.
                        </p>
                    </div>
                </div>
            </div>
        </div >
    );
}
