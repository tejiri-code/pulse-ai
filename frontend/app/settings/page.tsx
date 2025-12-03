'use client';

import { useState, useEffect } from 'react';

interface ApiKeys {
    blueskyHandle: string;
    blueskyAppPassword: string;
    linkedinAccessToken: string;
    devtoApiKey: string;
}

export default function SettingsPage() {
    const [keys, setKeys] = useState<ApiKeys>({
        blueskyHandle: '',
        blueskyAppPassword: '',
        linkedinAccessToken: '',
        devtoApiKey: ''
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
            blueskyHandle: '',
            blueskyAppPassword: '',
            linkedinAccessToken: '',
            devtoApiKey: ''
        });
        localStorage.removeItem('apiKeys');
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                        Settings
                    </h1>
                    <p className="text-gray-400">
                        Configure your FREE platform credentials 🎉
                    </p>
                </div>

                {/* Success Message */}
                {saved && (
                    <div className="mb-6 bg-green-900/30 border border-green-700 rounded-lg p-4">
                        <p className="text-green-400">✅ Settings saved successfully!</p>
                    </div>
                )}

                {/* Bluesky */}
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700 mb-6">
                    <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                        🦋 Bluesky - FREE Twitter Alternative
                    </h2>
                    <p className="text-gray-400 mb-4 text-sm">
                        Get app password: <a href="https://bsky.app/settings/app-passwords" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline">Bluesky Settings</a>
                    </p>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                                Handle (e.g., username.bsky.social)
                            </label>
                            <input
                                type="text"
                                value={keys.blueskyHandle}
                                onChange={(e) => setKeys({ ...keys, blueskyHandle: e.target.value })}
                                placeholder="username.bsky.social"
                                className="w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                                App Password
                            </label>
                            <input
                                type="password"
                                value={keys.blueskyAppPassword}
                                onChange={(e) => setKeys({ ...keys, blueskyAppPassword: e.target.value })}
                                placeholder="xxxx-xxxx-xxxx-xxxx"
                                className="w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
                            />
                        </div>
                    </div>
                </div>

                {/* LinkedIn */}
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700 mb-6">
                    <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                        💼 LinkedIn - FREE Professional Network
                    </h2>
                    <p className="text-gray-400 mb-4 text-sm">
                        Get access token: <a href="https://www.linkedin.com/developers/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline">LinkedIn Developers</a> (Create app → OAuth → Copy token)
                    </p>

                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            Access Token
                        </label>
                        <input
                            type="password"
                            value={keys.linkedinAccessToken}
                            onChange={(e) => setKeys({ ...keys, linkedinAccessToken: e.target.value })}
                            placeholder="Enter LinkedIn access token"
                            className="w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
                        />
                    </div>
                </div>

                {/* Dev.to */}
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700 mb-6">
                    <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                        ✍️ Dev.to - FREE Medium Alternative
                    </h2>
                    <p className="text-gray-400 mb-4 text-sm">
                        Get API key: <a href="https://dev.to/settings/extensions" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline">Dev.to Settings</a> → Generate API Key
                    </p>

                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            API Key
                        </label>
                        <input
                            type="password"
                            value={keys.devtoApiKey}
                            onChange={(e) => setKeys({ ...keys, devtoApiKey: e.target.value })}
                            placeholder="Enter Dev.to API key"
                            className="w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
                        />
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4">
                    <button
                        onClick={handleSave}
                        className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 hover:shadow-lg hover:shadow-green-500/50"
                    >
                        💾 Save Settings
                    </button>
                    <button
                        onClick={handleClear}
                        className="bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200"
                    >
                        🗑️ Clear All
                    </button>
                </div>

                {/* Info Box */}
                <div className="mt-6 bg-blue-900/20 border border-blue-700/50 rounded-lg p-4">
                    <p className="text-sm text-blue-300">
                        <strong>ℹ️ All FREE platforms!</strong> No $100/month Twitter fees. Bluesky, LinkedIn, and Dev.to all have free APIs.
                        Your keys are stored locally and only used when you publish.
                    </p>
                </div>
            </div>
        </div>
    );
}
