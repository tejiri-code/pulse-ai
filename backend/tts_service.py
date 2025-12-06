"""
Edge TTS Text-to-Speech Service (FREE - No API Key Required!)
Generates podcast-style audio from news summaries using Microsoft Edge voices
"""
import os
import io
import asyncio
import random
from typing import Optional
from datetime import datetime

import edge_tts


# Default voice (Jenny - clear professional voice)
DEFAULT_VOICE = "en-US-JennyNeural"


# Available Edge TTS voices for podcast
AVAILABLE_VOICES = {
    "jenny": {"id": "en-US-JennyNeural", "name": "Jenny", "description": "Clear, professional female voice"},
    "aria": {"id": "en-US-AriaNeural", "name": "Aria", "description": "Warm, engaging female voice"},
    "guy": {"id": "en-US-GuyNeural", "name": "Guy", "description": "Deep, authoritative male voice"},
    "davis": {"id": "en-US-DavisNeural", "name": "Davis", "description": "Friendly, casual male voice"},
    "sara": {"id": "en-US-SaraNeural", "name": "Sara", "description": "Energetic, young female voice"},
    "tony": {"id": "en-US-TonyNeural", "name": "Tony", "description": "Confident, professional male voice"},
    "nancy": {"id": "en-US-NancyNeural", "name": "Nancy", "description": "Warm, mature female voice"},
}


async def generate_audio(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    """
    Generate audio from text using Edge TTS (FREE!)
    
    Args:
        text: The text to convert to speech
        voice: Edge TTS voice name
        
    Returns:
        Audio data as bytes (MP3 format)
    """
    # Create TTS instance
    communicate = edge_tts.Communicate(text, voice)
    
    # Generate audio to memory
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    
    return b''.join(audio_chunks)


# Transition phrases to vary the delivery
STORY_TRANSITIONS = [
    "Moving on to our next story.",
    "Now, let's shift gears to something interesting.",
    "Up next, we have a fascinating development.",
    "Here's another story that caught our attention.",
    "And now for something that's making waves in the industry.",
    "Next up on our radar.",
    "Switching topics now.",
    "This next one is particularly noteworthy.",
]

STORY_INTROS = [
    "So here's the deal:",
    "Here's what you need to know:",
    "Let me break this down for you:",
    "The key takeaway here is:",
    "What's really interesting about this is:",
    "Here's why this matters:",
]

COMMENTARY_PHRASES = [
    "This is a significant development because",
    "What makes this particularly interesting is that",
    "The implications here are quite substantial.",
    "This could reshape how we think about",
    "Industry experts are paying close attention to this.",
    "This aligns with broader trends we've been seeing in",
]


def create_podcast_script(summaries: list, report_type: str = "daily") -> str:
    """
    Create a professional podcast-style script from news summaries
    
    Args:
        summaries: List of summary dicts with title, three_sentence_summary, tags
        report_type: "daily" or "weekly"
        
    Returns:
        Formatted podcast script text optimized for natural TTS delivery
    """
    today = datetime.utcnow().strftime("%A, %B %d, %Y")
    
    if not summaries:
        return (
            f"Hey there, and welcome to Pulse AI. "
            f"It's {today}, and we were hoping to bring you the latest in AI news... "
            "but it looks like our news feed is taking a coffee break today. "
            "No worries though! Check back tomorrow for fresh updates on artificial intelligence and machine learning. "
            "Until then, stay curious!"
        )
    
    script_parts = []
    
    # Engaging intro with personality
    if report_type == "daily":
        intro_options = [
            f"Hey there, and welcome back to Pulse AI! I'm your host, and today is {today}. "
            f"We've got {len(summaries)} {'stories' if len(summaries) > 1 else 'story'} lined up for you today, "
            "covering the latest developments shaking up the world of artificial intelligence. "
            "Grab your coffee, get comfortable, and let's get into it.",
            
            f"Good day, listeners! Welcome to Pulse AI, your daily dose of AI news. "
            f"Today is {today}, and we've curated the top {len(summaries)} {'stories' if len(summaries) > 1 else 'story'} "
            "from across the tech landscape. From breakthroughs to business moves, "
            "we've got you covered. Let's dive right in.",
            
            f"What's going on, everyone? Welcome to another episode of Pulse AI. "
            f"It's {today}, and the AI world never sleeps. "
            f"We've got {len(summaries)} {'stories' if len(summaries) > 1 else 'story'} to get through today, "
            "so let's not waste any time. Here we go.",
        ]
        script_parts.append(random.choice(intro_options))
    else:
        script_parts.append(
            f"Hello and welcome to your Pulse AI Weekly Roundup! "
            f"It's the week of {today}, and what a week it's been in the world of AI. "
            f"We've gathered {len(summaries)} of the most impactful stories for you. "
            "Whether you've been following along or playing catch-up, "
            "we've got everything you need to know. Let's break it down."
        )
    
    # Small pause before first story
    script_parts.append("")
    
    # Add each story with varied, natural delivery
    used_transitions = []
    for i, summary in enumerate(summaries, 1):
        title = summary.get("title", "Untitled Story")
        content = summary.get("three_sentence_summary", "")
        tags = summary.get("tags", [])
        
        # Add transition for stories after the first one
        if i > 1:
            available_transitions = [t for t in STORY_TRANSITIONS if t not in used_transitions]
            if not available_transitions:
                used_transitions = []
                available_transitions = STORY_TRANSITIONS
            transition = random.choice(available_transitions)
            used_transitions.append(transition)
            script_parts.append(transition)
        
        # Story number with varied phrasing
        if len(summaries) > 1:
            number_phrases = [
                f"Story number {i}:",
                f"Our {'first' if i == 1 else 'next'} story:",
                f"Number {i} on our list:",
                f"Coming in at number {i}:",
            ]
            if i == len(summaries):
                number_phrases = [
                    "And finally, our last story for today:",
                    "Wrapping up with our final story:",
                    "And for our last story:",
                    "To close things out:",
                ]
            script_parts.append(random.choice(number_phrases))
        
        # Title with emphasis
        script_parts.append(f'"{title}."')
        
        # Story intro phrase
        if content:
            intro_phrase = random.choice(STORY_INTROS)
            script_parts.append(f"{intro_phrase} {content}")
        
        # Add tags with natural commentary
        if tags and len(tags) > 0:
            tag_str = ", ".join(tags[:3])
            tag_outros = [
                f"This touches on {tag_str}, areas we'll definitely be keeping an eye on.",
                f"Key topics here include {tag_str}.",
                f"This one falls under {tag_str}, for those tracking these spaces.",
            ]
            script_parts.append(random.choice(tag_outros))
        
        # Natural pause between stories
        if i < len(summaries):
            script_parts.append("")
    
    # Engaging outro
    outro_options = [
        "And that's a wrap on today's episode of Pulse AI! "
        "Thanks for tuning in. If you found this helpful, make sure to come back tomorrow. "
        "Remember, in the fast-moving world of AI, staying informed is your superpower. "
        "Until next time, stay curious, stay innovative, and keep pushing boundaries. "
        "This is Pulse AI, signing off.",
        
        "Alright, that's all the time we have for today's Pulse AI. "
        "We covered some really exciting developments, and I can't wait to see what tomorrow brings. "
        "Thanks for listening, and as always, stay ahead of the curve. "
        "See you in the next episode!",
        
        "And there you have it, folks! Another episode of Pulse AI in the books. "
        "The AI landscape is evolving faster than ever, and we're here to help you keep up. "
        "Thanks for spending your time with us today. "
        "Stay sharp, stay informed, and we'll catch you next time. Take care!",
    ]
    script_parts.append("")
    script_parts.append(random.choice(outro_options))
    
    return " ".join(filter(None, script_parts))


async def generate_daily_podcast(
    summaries: list,
    api_key: str = None,  # Kept for API compatibility, not needed for Edge TTS
    voice_id: str = DEFAULT_VOICE
) -> bytes:
    """
    Generate a complete daily podcast audio from summaries
    
    Args:
        summaries: List of summary dicts
        api_key: Not needed for Edge TTS (kept for API compatibility)
        voice_id: Voice to use for narration
        
    Returns:
        Audio data as bytes (MP3)
    """
    # Create the podcast script
    script = create_podcast_script(summaries, report_type="daily")
    
    # Map voice_id to Edge TTS voice if needed
    voice = voice_id
    for v in AVAILABLE_VOICES.values():
        if v["id"] == voice_id or voice_id.lower() == v["name"].lower():
            voice = v["id"]
            break
    
    # Generate audio with Edge TTS (FREE!)
    print(f"🎙️ Generating podcast with Edge TTS (voice: {voice})")
    audio_data = await generate_audio(script, voice)
    print(f"✅ Podcast generated successfully ({len(audio_data)} bytes)")
    
    return audio_data


async def generate_weekly_podcast(
    summaries: list,
    api_key: str = None,  # Kept for API compatibility
    voice_id: str = DEFAULT_VOICE
) -> bytes:
    """
    Generate a complete weekly podcast audio from summaries
    
    Args:
        summaries: List of summary dicts
        api_key: Not needed for Edge TTS (kept for API compatibility)
        voice_id: Voice to use for narration
        
    Returns:
        Audio data as bytes (MP3)
    """
    # Create the podcast script
    script = create_podcast_script(summaries, report_type="weekly")
    
    # Map voice_id to Edge TTS voice if needed
    voice = voice_id
    for v in AVAILABLE_VOICES.values():
        if v["id"] == voice_id or voice_id.lower() == v["name"].lower():
            voice = v["id"]
            break
    
    # Generate audio with Edge TTS (FREE!)
    print(f"🎙️ Generating weekly podcast with Edge TTS (voice: {voice})")
    audio_data = await generate_audio(script, voice)
    print(f"✅ Weekly podcast generated successfully ({len(audio_data)} bytes)")
    
    return audio_data


def get_available_voices() -> dict:
    """Return dict of available voices for the frontend"""
    return AVAILABLE_VOICES


# Backwards compatibility - keep the old default voice ID reference
DEFAULT_VOICE_ID = DEFAULT_VOICE
