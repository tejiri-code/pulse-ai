"""
ElevenLabs Text-to-Speech Service
Generates podcast-style audio from news summaries
"""
import os
import io
from typing import Optional
from datetime import datetime

# Try to import elevenlabs, gracefully handle if not installed
try:
    from elevenlabs import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False


# Default voice ID (Rachel - a clear, professional voice)
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"


def get_client(api_key: str) -> Optional[object]:
    """
    Get ElevenLabs client with the provided API key
    """
    if not ELEVENLABS_AVAILABLE:
        raise ImportError("ElevenLabs SDK not installed. Run: pip install elevenlabs")
    
    if not api_key:
        raise ValueError("ElevenLabs API key is required")
    
    return ElevenLabs(api_key=api_key)


def generate_audio(
    text: str,
    api_key: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = "eleven_flash_v2_5"  # Free tier compatible model
) -> bytes:
    """
    Generate audio from text using ElevenLabs API
    
    Args:
        text: The text to convert to speech
        api_key: ElevenLabs API key
        voice_id: ElevenLabs voice ID (default: Rachel)
        model_id: ElevenLabs model to use
        
    Returns:
        Audio data as bytes (MP3 format)
    """
    client = get_client(api_key)
    
    # Generate audio using the SDK
    audio_generator = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=model_id,
        output_format="mp3_44100_128"
    )
    
    # Collect all audio chunks into bytes
    audio_chunks = []
    for chunk in audio_generator:
        audio_chunks.append(chunk)
    
    return b''.join(audio_chunks)


import random

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
    api_key: str,
    voice_id: str = DEFAULT_VOICE_ID
) -> bytes:
    """
    Generate a complete daily podcast audio from summaries
    
    Args:
        summaries: List of summary dicts
        api_key: ElevenLabs API key
        voice_id: Voice to use for narration
        
    Returns:
        Audio data as bytes (MP3)
    """
    # Create the podcast script
    script = create_podcast_script(summaries, report_type="daily")
    
    # Generate audio
    audio_data = generate_audio(script, api_key, voice_id)
    
    return audio_data


async def generate_weekly_podcast(
    summaries: list,
    api_key: str,
    voice_id: str = DEFAULT_VOICE_ID
) -> bytes:
    """
    Generate a complete weekly podcast audio from summaries
    
    Args:
        summaries: List of summary dicts
        api_key: ElevenLabs API key
        voice_id: Voice to use for narration
        
    Returns:
        Audio data as bytes (MP3)
    """
    # Create the podcast script
    script = create_podcast_script(summaries, report_type="weekly")
    
    # Generate audio
    audio_data = generate_audio(script, api_key, voice_id)
    
    return audio_data


# Available voices for users to choose from
AVAILABLE_VOICES = {
    "rachel": {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "description": "Clear, professional female voice"},
    "drew": {"id": "29vD33N1CtxCmqQRPOHJ", "name": "Drew", "description": "Warm, engaging male voice"},
    "clyde": {"id": "2EiwWnXFnvU5JabPnv8n", "name": "Clyde", "description": "Deep, authoritative male voice"},
    "domi": {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi", "description": "Energetic, young female voice"},
    "bella": {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "description": "Soft, calming female voice"},
}


def get_available_voices() -> dict:
    """Return dict of available voices for the frontend"""
    return AVAILABLE_VOICES
