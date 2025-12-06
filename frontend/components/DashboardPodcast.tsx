'use client';

import { useState, useRef, useEffect } from 'react';
import {
    Play, Pause, Volume2, VolumeX, Download, Loader2,
    Headphones, Radio, Mic2, Waves
} from 'lucide-react';

interface DashboardPodcastProps {
    reportType?: 'daily' | 'weekly';
}

export default function DashboardPodcast({ reportType = 'daily' }: DashboardPodcastProps) {
    const [isPlaying, setIsPlaying] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [progress, setProgress] = useState(0);
    const [duration, setDuration] = useState(0);
    const [isMuted, setIsMuted] = useState(false);
    const [volume, setVolume] = useState(0.8);

    const audioRef = useRef<HTMLAudioElement | null>(null);

    const generateAudio = async () => {
        setIsLoading(true);
        setError(null);

        try {
            const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const endpoint = reportType === 'daily' ? '/audio/daily' : '/audio/weekly';

            const response = await fetch(`${backendUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}), // API key now comes from backend env
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to generate audio');
            }

            const audioBlob = await response.blob();
            const url = URL.createObjectURL(audioBlob);
            setAudioUrl(url);

            // Auto-play after generation
            if (audioRef.current) {
                audioRef.current.src = url;
                audioRef.current.play();
                setIsPlaying(true);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to generate audio');
        } finally {
            setIsLoading(false);
        }
    };

    const togglePlay = () => {
        if (!audioUrl) {
            generateAudio();
            return;
        }

        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const toggleMute = () => {
        if (audioRef.current) {
            audioRef.current.muted = !isMuted;
            setIsMuted(!isMuted);
        }
    };

    const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newVolume = parseFloat(e.target.value);
        setVolume(newVolume);
        if (audioRef.current) {
            audioRef.current.volume = newVolume;
        }
    };

    const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newTime = parseFloat(e.target.value);
        if (audioRef.current) {
            audioRef.current.currentTime = newTime;
            setProgress(newTime);
        }
    };

    const handleDownload = () => {
        if (audioUrl) {
            const a = document.createElement('a');
            a.href = audioUrl;
            a.download = `pulse_${reportType}_podcast.mp3`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    };

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    useEffect(() => {
        const audio = audioRef.current;
        if (!audio) return;

        const handleTimeUpdate = () => setProgress(audio.currentTime);
        const handleDurationChange = () => setDuration(audio.duration);
        const handleEnded = () => setIsPlaying(false);

        audio.addEventListener('timeupdate', handleTimeUpdate);
        audio.addEventListener('durationchange', handleDurationChange);
        audio.addEventListener('ended', handleEnded);

        return () => {
            audio.removeEventListener('timeupdate', handleTimeUpdate);
            audio.removeEventListener('durationchange', handleDurationChange);
            audio.removeEventListener('ended', handleEnded);
        };
    }, [audioUrl]);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (audioUrl) {
                URL.revokeObjectURL(audioUrl);
            }
        };
    }, [audioUrl]);

    return (
        <div className="glass-panel rounded-2xl overflow-hidden">
            <audio ref={audioRef} preload="none" />

            {/* Podcast Header with Gradient */}
            <div className="relative bg-gradient-to-r from-purple-600/30 via-indigo-600/30 to-blue-600/30 p-5 sm:p-6">
                {/* Animated Background Pattern */}
                <div className="absolute inset-0 opacity-20">
                    <div className="absolute top-2 left-4 w-16 h-16 bg-purple-500 rounded-full blur-2xl animate-pulse" />
                    <div className="absolute bottom-2 right-8 w-20 h-20 bg-blue-500 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '0.5s' }} />
                </div>

                <div className="relative flex items-center gap-4">
                    {/* Podcast Icon */}
                    <div className="relative">
                        <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/30">
                            {isPlaying ? (
                                <Waves className="w-8 h-8 sm:w-10 sm:h-10 text-white animate-pulse" />
                            ) : (
                                <Radio className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
                            )}
                        </div>
                        {isPlaying && (
                            <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-gray-900 animate-pulse" />
                        )}
                    </div>

                    <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                            <Mic2 className="w-4 h-4 text-purple-400" />
                            <span className="text-xs text-purple-400 font-semibold uppercase tracking-wider">
                                AI-Powered Podcast
                            </span>
                        </div>
                        <h3 className="text-xl sm:text-2xl font-bold text-white">
                            {reportType === 'daily' ? "Today's AI Brief" : 'Weekly Digest'}
                        </h3>
                        <p className="text-sm text-gray-400 mt-0.5">
                            Listen to your personalized news summary
                        </p>
                    </div>
                </div>
            </div>

            {/* Player Controls */}
            <div className="p-5 sm:p-6 space-y-4">
                {/* Error Message */}
                {error && (
                    <div className="p-3 rounded-xl bg-red-900/30 border border-red-700/50">
                        <p className="text-sm text-red-400">{error}</p>
                    </div>
                )}

                {/* Main Controls Row */}
                <div className="flex items-center gap-4">
                    {/* Play/Pause Button */}
                    <button
                        onClick={togglePlay}
                        disabled={isLoading}
                        className="w-14 h-14 sm:w-16 sm:h-16 flex items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 hover:from-purple-400 hover:to-indigo-500 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/30 disabled:opacity-50 disabled:hover:scale-100 flex-shrink-0"
                    >
                        {isLoading ? (
                            <Loader2 className="w-6 h-6 sm:w-7 sm:h-7 text-white animate-spin" />
                        ) : isPlaying ? (
                            <Pause className="w-6 h-6 sm:w-7 sm:h-7 text-white" />
                        ) : (
                            <Play className="w-6 h-6 sm:w-7 sm:h-7 text-white ml-1" />
                        )}
                    </button>

                    {/* Progress Section */}
                    <div className="flex-1 space-y-2">
                        {/* Progress Bar */}
                        <div className="relative">
                            <input
                                type="range"
                                min="0"
                                max={duration || 100}
                                value={progress}
                                onChange={handleSeek}
                                disabled={!audioUrl}
                                className="w-full h-2 bg-gray-700/50 rounded-full appearance-none cursor-pointer disabled:opacity-50"
                                style={{
                                    background: audioUrl
                                        ? `linear-gradient(to right, rgb(168, 85, 247) ${(progress / (duration || 100)) * 100}%, rgb(55, 65, 81) ${(progress / (duration || 100)) * 100}%)`
                                        : undefined
                                }}
                            />
                        </div>

                        {/* Time Display */}
                        <div className="flex justify-between text-xs text-gray-500 font-mono">
                            <span>{formatTime(progress)}</span>
                            <span>{audioUrl ? formatTime(duration) : '--:--'}</span>
                        </div>
                    </div>

                    {/* Right Controls */}
                    <div className="flex items-center gap-2 sm:gap-3">
                        {/* Volume */}
                        <div className="hidden sm:flex items-center gap-2">
                            <button
                                onClick={toggleMute}
                                className="p-2 rounded-lg hover:bg-gray-800/50 transition-colors text-gray-400 hover:text-white"
                            >
                                {isMuted ? (
                                    <VolumeX className="w-5 h-5" />
                                ) : (
                                    <Volume2 className="w-5 h-5" />
                                )}
                            </button>
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.1"
                                value={volume}
                                onChange={handleVolumeChange}
                                className="w-20 h-1.5 bg-gray-700 rounded-full appearance-none cursor-pointer accent-purple-500"
                            />
                        </div>

                        {/* Download Button */}
                        {audioUrl && (
                            <button
                                onClick={handleDownload}
                                className="p-2.5 rounded-xl bg-gray-800/50 hover:bg-gray-700/50 transition-colors text-gray-400 hover:text-white"
                                title="Download podcast"
                            >
                                <Download className="w-5 h-5" />
                            </button>
                        )}
                    </div>
                </div>

                {/* Loading/Generation Message */}
                {isLoading && (
                    <div className="flex items-center justify-center gap-3 py-3 px-4 rounded-xl bg-purple-900/20 border border-purple-500/20">
                        <div className="flex gap-1">
                            <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                            <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                            <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                        </div>
                        <p className="text-sm text-purple-300">
                            Generating your personalized podcast...
                        </p>
                    </div>
                )}

                {/* CTA when not played yet */}
                {!audioUrl && !isLoading && !error && (
                    <div className="text-center py-2">
                        <p className="text-sm text-gray-400">
                            Click play to generate your AI-narrated news summary
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
