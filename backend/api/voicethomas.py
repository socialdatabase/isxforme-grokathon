"""
Voice API integration using xAI's realtime WebSocket API.
Supports text-to-speech and speech-to-text using Grok voice capabilities.

Based on xAI Voice API docs:
- TTS endpoint: wss://api.x.ai/v1/realtime/audio/speech
- STT endpoint: wss://api.x.ai/v1/realtime/audio/transcriptions
- Audio format: mono-channel, PCM linear16, 24kHz (TTS) / 16kHz (STT)
- Available voices: Ara, Rex, Sal, Eve, Una, Leo
"""

import asyncio
import base64
import json
import io
import wave
import os
from typing import Optional, AsyncGenerator, Generator

import websockets
from django.conf import settings


# Available xAI voices
AVAILABLE_VOICES = ["ara", "rex", "sal", "eve", "una", "leo"]
DEFAULT_VOICE = "ara"

# Audio configuration
TTS_SAMPLE_RATE = 24000
TTS_CHANNELS = 1
TTS_SAMPLE_WIDTH = 2  # 16-bit = 2 bytes

STT_SAMPLE_RATE = 16000
STT_ENCODING = "linear16"


def clean_text_for_speech(text: str) -> str:
    """
    Clean text for better speech output by removing hashtags, URLs, and other characters
    that sound awkward when spoken.
    
    Args:
        text: Raw text that may contain hashtags, URLs, markdown, etc.
    
    Returns:
        Cleaned text suitable for text-to-speech
    """
    import re
    
    cleaned_text = text
    
    # Remove hashtags (but keep the word)
    cleaned_text = re.sub(r'#(\w+)', r'\1', cleaned_text)
    
    # Remove @ mentions (but keep the username as text)
    cleaned_text = re.sub(r'@(\w+)', r'\1', cleaned_text)
    
    # Remove URLs
    cleaned_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned_text)
    cleaned_text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned_text)
    
    # Remove email addresses
    cleaned_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', cleaned_text)
    
    # Remove special markdown/social media characters that sound awkward
    cleaned_text = cleaned_text.replace('*', '')
    cleaned_text = cleaned_text.replace('_', '')
    cleaned_text = cleaned_text.replace('~', '')
    cleaned_text = cleaned_text.replace('`', '')
    
    # Replace multiple spaces/newlines with single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Remove leading/trailing whitespace
    cleaned_text = cleaned_text.strip()
    
    # If text is empty after cleaning, use original
    if not cleaned_text:
        cleaned_text = text
    
    return cleaned_text


async def text_to_speech_async(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    clean_text: bool = True
) -> bytes:
    """
    Convert text to speech using xAI's WebSocket TTS API.
    
    Args:
        text: The text to convert to speech
        voice_id: Voice to use (ara, rex, sal, eve, una, leo). Default: ara
        clean_text: Whether to clean the text for better speech output
    
    Returns:
        bytes: Raw PCM audio data (mono, linear16, 24kHz)
    """
    if voice_id.lower() not in AVAILABLE_VOICES:
        voice_id = DEFAULT_VOICE
    
    # Clean text if requested
    if clean_text:
        text = clean_text_for_speech(text)
    
    api_key = settings.XAI_TOKEN
    uri = "wss://api.x.ai/v1/realtime/audio/speech"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    audio_bytes = b""
    
    async with websockets.connect(uri, additional_headers=headers) as websocket:
        # Send config message
        config_message = {
            "type": "config",
            "data": {"voice_id": voice_id.lower()}
        }
        await websocket.send(json.dumps(config_message))
        
        # Send text chunk
        text_message = {
            "type": "text_chunk",
            "data": {
                "text": text,
                "is_last": True
            }
        }
        await websocket.send(json.dumps(text_message))
        
        # Receive audio chunks
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                
                # Extract audio from response
                # Response format: {"data": {"type": "audio", "data": {"audio": "base64...", "is_last": bool}}}
                outer_data = data.get("data", {})
                inner_data = outer_data.get("data", {}) if isinstance(outer_data, dict) else {}
                
                audio_b64 = inner_data.get("audio", "")
                is_last = inner_data.get("is_last", False)
                
                if audio_b64:
                    chunk_bytes = base64.b64decode(audio_b64)
                    audio_bytes += chunk_bytes
                
                if is_last:
                    break
                    
            except websockets.exceptions.ConnectionClosedOK:
                break
            except websockets.exceptions.ConnectionClosedError:
                break
    
    return audio_bytes


async def text_to_speech_stream_async(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    clean_text: bool = True
) -> AsyncGenerator[bytes, None]:
    """
    Stream text to speech using xAI's WebSocket TTS API.
    Yields audio chunks as they arrive for real-time playback.
    
    Args:
        text: The text to convert to speech
        voice_id: Voice to use (ara, rex, sal, eve, una, leo). Default: ara
        clean_text: Whether to clean the text for better speech output
    
    Yields:
        bytes: Audio chunks as they arrive (PCM linear16, 24kHz)
    """
    if voice_id.lower() not in AVAILABLE_VOICES:
        voice_id = DEFAULT_VOICE
    
    if clean_text:
        text = clean_text_for_speech(text)
    
    api_key = settings.XAI_TOKEN
    uri = "wss://api.x.ai/v1/realtime/audio/speech"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    async with websockets.connect(uri, additional_headers=headers) as websocket:
        # Send config message
        config_message = {
            "type": "config",
            "data": {"voice_id": voice_id.lower()}
        }
        await websocket.send(json.dumps(config_message))
        
        # Send text chunk
        text_message = {
            "type": "text_chunk",
            "data": {
                "text": text,
                "is_last": True
            }
        }
        await websocket.send(json.dumps(text_message))
        
        # Receive and yield audio chunks
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                
                # Response format: {"data": {"type": "audio", "data": {"audio": "base64...", "is_last": bool}}}
                outer_data = data.get("data", {})
                inner_data = outer_data.get("data", {}) if isinstance(outer_data, dict) else {}
                
                audio_b64 = inner_data.get("audio", "")
                is_last = inner_data.get("is_last", False)
                
                if audio_b64:
                    chunk_bytes = base64.b64decode(audio_b64)
                    yield chunk_bytes
                
                if is_last:
                    break
                    
            except websockets.exceptions.ConnectionClosedOK:
                break
            except websockets.exceptions.ConnectionClosedError:
                break


def text_to_speech(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    clean_text: bool = True,
    output_format: str = "wav"
) -> bytes:
    """
    Synchronous wrapper for text-to-speech conversion.
    
    Args:
        text: The text to convert to speech
        voice_id: Voice to use (ara, rex, sal, eve, una, leo). Default: ara
        clean_text: Whether to clean the text for better speech output
        output_format: Output format - "wav" for WAV file, "pcm" for raw PCM data
    
    Returns:
        bytes: Audio data in the specified format
    """
    # Run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        pcm_audio = loop.run_until_complete(
            text_to_speech_async(text, voice_id, clean_text)
        )
    finally:
        loop.close()
    
    if output_format == "pcm":
        return pcm_audio
    
    # Convert to WAV format
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(TTS_CHANNELS)
        wf.setsampwidth(TTS_SAMPLE_WIDTH)
        wf.setframerate(TTS_SAMPLE_RATE)
        wf.writeframes(pcm_audio)
    
    wav_buffer.seek(0)
    return wav_buffer.read()


def text_to_speech_stream(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    clean_text: bool = True
) -> Generator[bytes, None, None]:
    """
    Synchronous generator wrapper for streaming text-to-speech.
    Yields audio chunks for real-time playback.
    
    Args:
        text: The text to convert to speech
        voice_id: Voice to use (ara, rex, sal, eve, una, leo). Default: ara
        clean_text: Whether to clean the text for better speech output
    
    Yields:
        bytes: Audio chunks (PCM linear16, 24kHz)
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        async_gen = text_to_speech_stream_async(text, voice_id, clean_text)
        while True:
            try:
                chunk = loop.run_until_complete(async_gen.__anext__())
                yield chunk
            except StopAsyncIteration:
                break
    finally:
        loop.close()


async def speech_to_text_async(
    audio_data: bytes,
    enable_interim_results: bool = False
) -> str:
    """
    Convert speech to text using xAI's WebSocket STT API.
    
    Args:
        audio_data: Raw audio data (PCM linear16, 16kHz recommended)
        enable_interim_results: Whether to receive interim (non-final) transcripts
    
    Returns:
        str: Transcribed text
    """
    api_key = settings.XAI_TOKEN
    uri = "wss://api.x.ai/v1/realtime/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    transcript = ""
    
    async with websockets.connect(uri, additional_headers=headers) as websocket:
        # Send config message
        config_message = {
            "type": "config",
            "data": {
                "encoding": STT_ENCODING,
                "sample_rate_hertz": STT_SAMPLE_RATE,
                "enable_interim_results": enable_interim_results
            }
        }
        await websocket.send(json.dumps(config_message))
        
        # Send audio data in chunks (to avoid overwhelming the WebSocket)
        chunk_size = 32000  # ~1 second of audio at 16kHz, 16-bit
        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i + chunk_size]
            audio_b64 = base64.b64encode(chunk).decode('utf-8')
            audio_message = {
                "type": "audio",
                "data": {
                    "audio": audio_b64
                }
            }
            await websocket.send(json.dumps(audio_message))
        
        # Signal end of audio by closing the send side or waiting for response
        # Receive transcript
        try:
            while True:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                data = json.loads(response)
                
                speech_data = data.get("data", {})
                if speech_data.get("type") == "speech_recognized":
                    transcript_data = speech_data.get("data", {})
                    text = transcript_data.get("transcript", "")
                    is_final = transcript_data.get("is_final", True)
                    
                    if is_final:
                        transcript += text
                        break
                    elif not enable_interim_results:
                        # Wait for final result
                        continue
                    else:
                        # For interim results, we could yield them
                        # but for now just wait for final
                        continue
                        
        except asyncio.TimeoutError:
            pass
        except websockets.exceptions.ConnectionClosedOK:
            pass
        except websockets.exceptions.ConnectionClosedError:
            pass
    
    return transcript


def speech_to_text(audio_file) -> str:
    """
    Synchronous wrapper for speech-to-text conversion.
    
    Args:
        audio_file: Django UploadedFile object, file-like object, bytes, or file path string
    
    Returns:
        str: Transcribed text
    """
    # Handle different input types and convert to bytes
    if hasattr(audio_file, 'read'):
        # Django UploadedFile or file-like object
        audio_file.seek(0)
        audio_bytes = audio_file.read()
    elif isinstance(audio_file, bytes):
        audio_bytes = audio_file
    elif isinstance(audio_file, str):
        # File path string
        with open(audio_file, 'rb') as f:
            audio_bytes = f.read()
    else:
        raise ValueError(f"Unsupported audio_file type: {type(audio_file)}")
    
    # Check if it's a WAV file and extract PCM data
    audio_bytes = extract_pcm_from_audio(audio_bytes)
    
    # Run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        transcript = loop.run_until_complete(
            speech_to_text_async(audio_bytes)
        )
    finally:
        loop.close()
    
    return transcript


def extract_pcm_from_audio(audio_bytes: bytes, target_sample_rate: int = 16000) -> bytes:
    """
    Extract and convert audio to raw PCM data suitable for xAI STT.
    Handles WAV, WebM, MP3, and other formats via ffmpeg/pydub.
    
    Args:
        audio_bytes: Raw audio file bytes (any format)
        target_sample_rate: Target sample rate (default 16kHz for STT)
    
    Returns:
        bytes: PCM audio data (mono, 16-bit, target sample rate)
    """
    try:
        from pydub import AudioSegment
        
        # Create a BytesIO object from the audio bytes
        audio_buffer = io.BytesIO(audio_bytes)
        
        # Detect format and load audio
        # Try different formats based on magic bytes
        audio = None
        
        # Check for WAV (RIFF header)
        if audio_bytes[:4] == b'RIFF':
            try:
                audio = AudioSegment.from_wav(audio_buffer)
            except Exception:
                pass
        
        # Check for WebM (EBML header: 0x1A45DFA3)
        if audio is None and audio_bytes[:4] == b'\x1aE\xdf\xa3':
            try:
                audio_buffer.seek(0)
                audio = AudioSegment.from_file(audio_buffer, format="webm")
            except Exception:
                pass
        
        # Check for MP3 (ID3 or 0xFF sync)
        if audio is None and (audio_bytes[:3] == b'ID3' or audio_bytes[:2] == b'\xff\xfb'):
            try:
                audio_buffer.seek(0)
                audio = AudioSegment.from_mp3(audio_buffer)
            except Exception:
                pass
        
        # Check for Ogg (OggS header)
        if audio is None and audio_bytes[:4] == b'OggS':
            try:
                audio_buffer.seek(0)
                audio = AudioSegment.from_ogg(audio_buffer)
            except Exception:
                pass
        
        # Try generic format detection as fallback
        if audio is None:
            try:
                audio_buffer.seek(0)
                audio = AudioSegment.from_file(audio_buffer)
            except Exception as e:
                print(f"Failed to load audio with pydub: {e}")
                # Last resort: return original bytes and hope for the best
                return audio_bytes
        
        # Convert to mono, 16-bit, target sample rate
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)  # 16-bit = 2 bytes
        audio = audio.set_frame_rate(target_sample_rate)
        
        # Export as raw PCM
        pcm_data = audio.raw_data
        
        print(f"Converted audio: {len(audio_bytes)} bytes -> {len(pcm_data)} bytes PCM @ {target_sample_rate}Hz")
        
        return pcm_data
        
    except ImportError:
        print("pydub not installed, falling back to basic WAV handling")
        # Fallback: basic WAV handling without pydub
        if audio_bytes[:4] == b'RIFF':
            try:
                wav_buffer = io.BytesIO(audio_bytes)
                with wave.open(wav_buffer, 'rb') as wf:
                    pcm_data = wf.readframes(wf.getnframes())
                    return pcm_data
            except wave.Error:
                pass
        
        return audio_bytes
    except Exception as e:
        print(f"Error converting audio: {e}")
        return audio_bytes


async def speech_to_text_stream_async(
    enable_interim_results: bool = True
) -> AsyncGenerator[tuple[str, bool], bytes]:
    """
    Stream speech-to-text using xAI's WebSocket STT API.
    This is a two-way async generator that:
    - Receives audio bytes via send()
    - Yields (transcript, is_final) tuples
    
    Usage:
        gen = speech_to_text_stream_async()
        await gen.asend(None)  # Initialize
        result = await gen.asend(audio_chunk)  # Send audio, get transcript
    
    Args:
        enable_interim_results: Whether to receive interim transcripts
    
    Yields:
        tuple[str, bool]: (transcript_text, is_final)
    """
    api_key = settings.XAI_TOKEN
    uri = "wss://api.x.ai/v1/realtime/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    async with websockets.connect(uri, additional_headers=headers) as websocket:
        # Send config message
        config_message = {
            "type": "config",
            "data": {
                "encoding": STT_ENCODING,
                "sample_rate_hertz": STT_SAMPLE_RATE,
                "enable_interim_results": enable_interim_results
            }
        }
        await websocket.send(json.dumps(config_message))
        
        while True:
            # Receive audio chunk from caller
            audio_chunk = yield
            
            if audio_chunk is None:
                break
            
            # Send audio chunk
            audio_b64 = base64.b64encode(audio_chunk).decode('utf-8')
            audio_message = {
                "type": "audio",
                "data": {
                    "audio": audio_b64
                }
            }
            await websocket.send(json.dumps(audio_message))
            
            # Try to receive any available transcripts (non-blocking)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                data = json.loads(response)
                
                speech_data = data.get("data", {})
                if speech_data.get("type") == "speech_recognized":
                    transcript_data = speech_data.get("data", {})
                    text = transcript_data.get("transcript", "")
                    is_final = transcript_data.get("is_final", False)
                    yield (text, is_final)
            except asyncio.TimeoutError:
                # No transcript available yet
                pass


def get_available_voices() -> list[str]:
    """
    Get the list of available voices for text-to-speech.
    
    Returns:
        list[str]: List of voice IDs
    """
    return AVAILABLE_VOICES.copy()


# Convenience functions for specific voices
def text_to_speech_ara(text: str, clean_text: bool = True, output_format: str = "wav") -> bytes:
    """Convert text to speech using Ara voice."""
    return text_to_speech(text, voice_id="ara", clean_text=clean_text, output_format=output_format)


def text_to_speech_rex(text: str, clean_text: bool = True, output_format: str = "wav") -> bytes:
    """Convert text to speech using Rex voice."""
    return text_to_speech(text, voice_id="rex", clean_text=clean_text, output_format=output_format)


def text_to_speech_sal(text: str, clean_text: bool = True, output_format: str = "wav") -> bytes:
    """Convert text to speech using Sal voice."""
    return text_to_speech(text, voice_id="sal", clean_text=clean_text, output_format=output_format)


def text_to_speech_eve(text: str, clean_text: bool = True, output_format: str = "wav") -> bytes:
    """Convert text to speech using Eve voice."""
    return text_to_speech(text, voice_id="eve", clean_text=clean_text, output_format=output_format)


def text_to_speech_una(text: str, clean_text: bool = True, output_format: str = "wav") -> bytes:
    """Convert text to speech using Una voice."""
    return text_to_speech(text, voice_id="una", clean_text=clean_text, output_format=output_format)


def text_to_speech_leo(text: str, clean_text: bool = True, output_format: str = "wav") -> bytes:
    """Convert text to speech using Leo voice."""
    return text_to_speech(text, voice_id="leo", clean_text=clean_text, output_format=output_format)
