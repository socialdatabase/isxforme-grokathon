"""
Test script for speech-to-text endpoint.
Run this from Django shell (python manage.py shell):
"""

import os
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

def test():
    client = Client()
    
    # Path to the test audio file
    audio_file_path = '/app/output.mp3'
    
    # Check if file exists
    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
        print("Please ensure output.mp3 exists in the backend directory")
        # return
    
    print(f"\n{'='*60}")
    print(f"Testing speech-to-text endpoint")
    print(f"Audio file: {audio_file_path}")
    print(f"{'='*60}\n")
    
    # Read the audio file
    with open(audio_file_path, 'rb') as f:
        audio_content = f.read()
    
    print(f"Audio file size: {len(audio_content)} bytes")
    
    # Create a SimpleUploadedFile for the request
    audio_file = SimpleUploadedFile(
        name="output.mp3",
        content=audio_content,
        content_type="audio/mpeg"
    )
    
    # Make POST request with file upload
    print("Sending request to endpoint...")
    response = client.post(
        '/api/grokathon/speech-to-text/',
        {'audio': audio_file},
        format='multipart'
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.get('Content-Type', 'N/A')}")
    
    if response.status_code == 200:
        result = response.json()
        transcribed_text = result.get('text', '')
        print(f"\n{'='*60}")
        print("Transcribed Text:")
        print(f"{'='*60}")
        print(transcribed_text)
        print(f"{'='*60}")
        print(f"Text length: {len(transcribed_text)} characters")
    else:
        print(f"\nError: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {error_data}")
        except:
            print(f"Error content: {response.content.decode('utf-8')}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    test()
