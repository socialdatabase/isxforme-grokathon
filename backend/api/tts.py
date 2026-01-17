import argparse
import asyncio
import base64
import json
import os
import wave
import pyaudio
import websockets
from dotenv import load_dotenv
from django.conf import settings


async def test_tts_websocket(
    uri: str,
    text: str,
    output_file: str,
    sample_rate: int = 24000,
    channels: int = 1,
    sample_width: int = 2
):
    """
    Test TTS WebSocket connection and generate audio from text.
    
    Args:
        uri: WebSocket URI for the TTS service
        text: Text to convert to speech
        output_file: Path to save the output WAV file
        sample_rate: Audio sample rate (default: 24000)
        channels: Number of audio channels (default: 1)
        sample_width: Sample width in bytes (default: 2)
    """
    api_key = settings.XAI_TOKEN
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    async with websockets.connect(uri, additional_headers=headers) as websocket:
        # Initialize audio output
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16 if sample_width == 2 else pyaudio.paInt32,
            channels=channels,
            rate=sample_rate,
            output=True,
        )
        
        # Send configuration message
        config_message = {"type": "config", "data": {"voice_id": "ara"}}
        await websocket.send(json.dumps(config_message))
        
        # Send text chunk
        text_message = {
            "type": "text_chunk",
            "data": {
                "text": text,
                "is_last": True,
            },
        }
        await websocket.send(json.dumps(text_message))
        print(f"Sent: {text_message}")
        
        # Receive and process audio chunks
        audio_bytes = b""
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                audio = data["data"]["data"]["audio"]
                chunk_bytes = base64.b64decode(audio)
                audio_bytes += chunk_bytes
                
                if len(chunk_bytes):
                    await asyncio.to_thread(stream.write, chunk_bytes)
                    print(f"Received audio chunk of {len(chunk_bytes)} bytes")
                
                if data.get("is_last", False):
                    print("Received last chunk")
                    break
                    
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed normally")
                break
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed with error")
                break
        
        # Close the audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save to WAV file
        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_bytes)
        print(f"Saved audio to {output_file}")


def test():
    """Main function to run the TTS WebSocket test."""
    load_dotenv()
    
    text = (
        "You are referring to the Tesla Model S. Let me pull up the details "
        "for you. The Model S is Teslas flagship sedan, first introduced in 2012, "
        "and it redefined electric vehicles with its stunning design and performance. "
        "It offers incredible acceleration, especially in the Plaid variant, and a "
        "spacious, tech-packed interior with a large center touchscreen. Want to "
        "experience its groundbreaking features for yourself with a test drive?"
    )
    
    parser = argparse.ArgumentParser(description="Test TTS WebSocket connection")
    parser.add_argument(
        "--uri",
        default="wss://api.x.ai/v1/realtime/audio/speech",
        help="WebSocket URI"
    )
    parser.add_argument(
        "--output",
        default="output.wav",
        help="Output WAV file path"
    )
    args = parser.parse_args()
    
    asyncio.run(
        test_tts_websocket(
            args.uri,
            text,
            args.output,
        )
    )
