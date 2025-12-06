'use client';

import { useState, useRef, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, Download, Loader2, Headphones } from 'lucide-react';

interface AudioPlayerProps {
    reportType: 'daily' | 'weekly';
    date?: string;
    apiKey: string;
    voiceId?: string;
}

export default function AudioPlayer({ reportType, date, apiKey, voiceId }: AudioPlayerProps) {
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
        if (!apiKey) {
            setError('ElevenLabs API key required. Add it in Settings.');
            return;
        }

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
                body: JSON.stringify({
                    elevenlabs_api_key: apiKey,
                    voice_id: voiceId,
                    date: date,
                }),
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
            a.download = `${reportType}_podcast.mp3`;
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

    if (!apiKey) {
        return (
            <div className="glass-panel p-4 rounded-xl border border-amber-500/30 bg-amber-500/5">
                <div className="flex items-center gap-3">
                    <Headphones className="w-5 h-5 text-amber-400" />
                    <div>
                        <p className="text-sm text-amber-300 font-medium">Audio Podcast Available</p>
                        <p className="text-xs text-gray-400">Add your ElevenLabs API key in Settings to listen</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="glass-panel p-4 sm:p-5 rounded-xl border border-purple-500/30 bg-gradient-to-r from-purple-900/20 to-indigo-900/20">
            <audio ref={audioRef} preload="none" />

            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-600">
                    <Headphones className="w-5 h-5 text-white" />
                </div>
                <div>
                    <h3 className="text-sm font-semibold text-white">
                        {reportType === 'daily' ? 'Daily Podcast' : 'Weekly Podcast'}
                    </h3>
                    <p className="text-xs text-gray-400">AI-narrated news summary</p>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="mb-4 p-3 rounded-lg bg-red-900/30 border border-red-700/50">
                    <p className="text-sm text-red-400">{error}</p>
                </div>
            )}

            {/* Player Controls */}
            <div className="flex items-center gap-4">
                {/* Play/Pause Button */}
                <button
                    onClick={togglePlay}
                    disabled={isLoading}
                    className="w-12 h-12 flex items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 hover:from-purple-400 hover:to-indigo-500 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-500/25 disabled:opacity-50 disabled:hover:scale-100"
                >
                    {isLoading ? (
                        <Loader2 className="w-5 h-5 text-white animate-spin" />
                    ) : isPlaying ? (
                        <Pause className="w-5 h-5 text-white" />
                    ) : (
                        <Play className="w-5 h-5 text-white ml-0.5" />
                    )}
                </button>

                {/* Progress Bar */}
                <div className="flex-1">
                    <input
                        type="range"
                        min="0"
                        max={duration || 100}
                        value={progress}
                        onChange={handleSeek}
                        disabled={!audioUrl}
                        className="w-full h-2 bg-gray-700 rounded-full appearance-none cursor-pointer accent-purple-500 disabled:opacity-50"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                        <span>{formatTime(progress)}</span>
                        <span>{formatTime(duration)}</span>
                    </div>
                </div>

                {/* Volume Control */}
                <div className="flex items-center gap-2">
                    <button
                        onClick={toggleMute}
                        className="p-2 rounded-lg hover:bg-gray-800/50 transition-colors"
                    >
                        {isMuted ? (
                            <VolumeX className="w-5 h-5 text-gray-400" />
                        ) : (
                            <Volume2 className="w-5 h-5 text-gray-400" />
                        )}
                    </button>
                    <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.1"
                        value={volume}
                        onChange={handleVolumeChange}
                        className="w-16 h-1.5 bg-gray-700 rounded-full appearance-none cursor-pointer accent-purple-500 hidden sm:block"
                    />
                </div>

                {/* Download Button */}
                {audioUrl && (
                    <button
                        onClick={handleDownload}
                        className="p-2 rounded-lg hover:bg-gray-800/50 transition-colors"
                        title="Download podcast"
                    >
                        <Download className="w-5 h-5 text-gray-400" />
                    </button>
                )}
            </div>

            {/* Loading Message */}
            {isLoading && (
                <p className="text-xs text-gray-400 mt-3 text-center animate-pulse">
                    Generating your personalized podcast... This may take a moment.
                </p>
            )}
        </div>
    );
}
