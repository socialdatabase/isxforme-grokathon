"""
Test script for stream-expert-perspective endpoint.

Option 1: Run from Django shell (python manage.py shell):
"""

def test():
    from django.test import Client

    client = Client()

    # Make the request
    response = client.get('/api/grokathon/generate-ai-bio-handle/', {
        'handle': '@f1'
    })

    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.get('Content-Type', 'N/A')}")
    print(f"\nStreaming content:\n{'-'*60}\n")

    # Read the streaming response
    if response.status_code == 200:
        content = b''.join(response.streaming_content)
        text = content.decode('utf-8')
        print(text)
        print(f"\n{'-'*60}")
        print(f"Total length: {len(text)} characters")
    else:
        print(f"Error: {response.content.decode('utf-8')}")

    print(f"{'='*60}\n")
