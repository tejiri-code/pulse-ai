'use client';

import { useState } from 'react';

export default function SettingsPage() {
    const [settings, setSettings] = useState({
        autoPostToX: true,
        autoPostToMedium: false,
        dailySchedule: '09:00',
        weeklySchedule: 'monday',
        sources: {
            arxiv: true,
            github: true,
            rss: true,
            blogs: true,
        },
        mockMode: true,
    });

    const [saved, setSaved] = useState(false);

    const handleSave = () => {
        // In a real app, this would save to backend
        console.log('Saving settings:', settings);
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent mb-2">
                        Settings
                    </h1>
                    <p className="text-gray-400">
                        Configure your Pulse AI Agent
                    </p>
                </div>

                {/* Success Message */}
                {saved && (
                    <div className="mb-6 bg-green-900/30 border border-green-700 rounded-lg p-4">
                        <p className="text-green-400">✅ Settings saved successfully!</p>
                    </div>
                )}

                {/* Publishing Settings */}
                <div className="mb-6 bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                    <h2 className="text-xl font-semibold text-white mb-4">Auto-Publishing</h2>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-white font-medium">Auto-post to X (Twitter)</p>
                                <p className="text-sm text-gray-400">Automatically publish daily updates to X</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={settings.autoPostToX}
                                    onChange={(e) => setSettings({ ...settings, autoPostToX: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </label>
                        </div>

                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-white font-medium">Auto-post weekly to Medium</p>
                                <p className="text-sm text-gray-400">Automatically create draft articles on Medium</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={settings.autoPostToMedium}
                                    onChange={(e) => setSettings({ ...settings, autoPostToMedium: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </label>
                        </div>
                    </div>
                </div>

                {/* Schedule Settings */}
                <div className="mb-6 bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                    <h2 className="text-xl font-semibold text-white mb-4">Schedule</h2>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                                Daily Update Time (UTC)
                            </label>
                            <input
                                type="time"
                                value={settings.dailySchedule}
                                onChange={(e) => setSettings({ ...settings, dailySchedule: e.target.value })}
                                className="bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 w-full max-w-xs"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                                Weekly Report Day
                            </label>
                            <select
                                value={settings.weeklySchedule}
                                onChange={(e) => setSettings({ ...settings, weeklySchedule: e.target.value })}
                                className="bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 w-full max-w-xs"
                            >
                                <option value="monday">Monday</option>
                                <option value="tuesday">Tuesday</option>
                                <option value="wednesday">Wednesday</option>
                                <option value="thursday">Thursday</option>
                                <option value="friday">Friday</option>
                                <option value="saturday">Saturday</option>
                                <option value="sunday">Sunday</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* News Sources */}
                <div className="mb-6 bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                    <h2 className="text-xl font-semibold text-white mb-4">News Sources</h2>

                    <div className="space-y-3">
                        {Object.entries(settings.sources).map(([source, enabled]) => (
                            <div key={source} className="flex items-center justify-between">
                                <div className="flex items-center">
                                    <span className="text-2xl mr-3">{getSourceIcon(source)}</span>
                                    <p className="text-white font-medium capitalize">{source}</p>
                                </div>
                                <label className="relative inline-flex items-center cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={enabled}
                                        onChange={(e) => setSettings({
                                            ...settings,
                                            sources: { ...settings.sources, [source]: e.target.checked }
                                        })}
                                        className="sr-only peer"
                                    />
                                    <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                                </label>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Mock Mode */}
                <div className="mb-6 bg-gradient-to-r from-yellow-900/30 to-orange-900/30 rounded-lg p-6 border border-yellow-700/50">
                    <h2 className="text-xl font-semibold text-white mb-2">⚠️ Mock Mode</h2>
                    <p className="text-gray-300 text-sm mb-4">
                        When enabled, the agent simulates API calls without actually posting to X or Medium. Perfect for testing!
                    </p>
                    <label className="relative inline-flex items-center cursor-pointer">
                        <input
                            type="checkbox"
                            checked={settings.mockMode}
                            onChange={(e) => setSettings({ ...settings, mockMode: e.target.checked })}
                            className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-yellow-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-yellow-600"></div>
                        <span className="ml-3 text-sm font-medium text-white">
                            {settings.mockMode ? 'Enabled' : 'Disabled'}
                        </span>
                    </label>
                </div>

                {/* Save Button */}
                <button
                    onClick={handleSave}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/50"
                >
                    💾 Save Settings
                </button>
            </div>
        </div>
    );
}

function getSourceIcon(source: string): string {
    const icons: Record<string, string> = {
        arxiv: '📚',
        github: '🐙',
        rss: '📡',
        blogs: '✍️',
    };
    return icons[source] || '📰';
}
