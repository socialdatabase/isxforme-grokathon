"""
Test script to play audio from text-to-speech endpoint.
Run this from Django shell (python manage.py shell):
"""

from django.test import Client

client = Client()

# Test text-to-speech
# text = "Hello, this is a test of the text to speech endpoint. How does it sound?"
text = text[:4096]
print(f"Converting text to speech: '{text}'")

response = client.get('/api/grokathon/text-to-speech/', {
    'text': text
})

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")
print(f"Content-Length: {len(response.content)} bytes")

# Option 1: Save to file (works in Docker container)
output_path = '/app/test_speech.mp3'  # Inside container
# Or use mounted volume:
# output_path = '/app/backend/test_speech.mp3'

with open(output_path, 'wb') as f:
    f.write(response.content)
print(f"\n✓ Saved audio to {output_path}")
print("\nDone!")
