"""
Test script for stream-expert-perspective endpoint.

Option 1: Run from Django shell (python manage.py shell):
"""

def test():
    from django.test import Client

    client = Client()

    # Test parameters
    expert_ids = [130745589,
    68746721,
    3918111614,
    2815077014,
    96999384,
    2815077014,
    86481377,
    2956121356,
    1007413134,
    153196789,
    990433714948661250,
    990433714948661250,
    2577596593,
    180993910,
    1007413134,
    314395154,
    25263396,
    44073696,
    2309105822,
    2902658140,
    796584325,
    3442793834]
    input_query = "What are AI researchers positive or negative about regarding latest developments in AI?"
    expert_category = "Academic AI Researchers"

    print(f"\n{'='*60}")
    print(f"Testing stream-expert-perspective endpoint")
    print(f"Query: {input_query}")
    print(f"Category: {expert_category}")
    print(f"IDs: {expert_ids}")
    print(f"{'='*60}\n")

    # Make the request
    response = client.get('/api/grokathon/stream-expert-perspective/', {
        'input_query': input_query,
        'expert_category': expert_category,
        'ids': expert_ids
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
