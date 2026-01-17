from django.conf import settings
from openai import OpenAI
import json
import io
import os

from api.timeline import fetch_accounts, fetch_posts, chunks


def extract_expert_categories(ids: list[str]):    
    """
    Categorize accounts into 4-5 expert categories based on their profiles.
    
    Args:
        ids: List of account IDs (around 100)
    
    Returns:
        dict: {
            "category_name_1": [id1, id2, ...],
            "category_name_2": [id3, id4, ...],
            ...
        }
    """    
    # Fetch accounts in chunks (Twitter API limit is 100)
    accounts = []
    for chunk in chunks(ids, 100):
        accounts += fetch_accounts(chunk)
    
    # Prepare account data for the prompt and create username->id mapping
    accounts_data = []
    username_to_id = {}  # Map username to account ID for fixing any username returns
    for account in accounts:
        account_id = account.get("id")
        username = account.get("username", "")
        accounts_data.append({
            "id": account_id,
            "username": username,
            "name": account.get("name", ""),
            "description": account.get("description", ""),
            "verified": account.get("verified", False)
        })
        if username:
            username_to_id[username] = account_id
            username_to_id[username.lower()] = account_id  # Also map lowercase for case-insensitive matching
    
    client = OpenAI(
        api_key=settings.XAI_TOKEN,
        base_url="https://api.x.ai/v1"
    )

    prompt = f"""Analyze the following social media accounts and categorize them into 4-5 distinct expert categories based on their profiles, descriptions, and expertise.

    Accounts to categorize:
    {json.dumps(accounts_data, indent=2)}

    Your task:
    1. Identify 4-5 distinct expert categories that best represent the different types of accounts (e.g., for Formula 1: "F1 Drivers", "F1 Journalists", "F1 Engineers", "F1 Teams/Companies", "F1 Analysts/Commentators")
    2. For each category, assign the relevant account IDs - CRITICAL: Use ONLY the "id" field from each account object, NEVER use the "username" field
    3. Categories should be specific and meaningful (not generic like "Other")
    4. Each account should be assigned to exactly one category
    5. Categories should reflect different roles, expertise areas, or types within the domain

    IMPORTANT: In the JSON response, use ONLY the numeric "id" values (as strings), NOT usernames. For example, if an account has id "123456" and username "example_user", use "123456" in your response, NOT "example_user".

    Return ONLY a valid JSON object with this exact structure:
    {{
        "category_1_name": [account_id1, account_id2, ...],
        "category_2_name": [account_id3, account_id4, ...],
        "category_3_name": [account_id5, account_id6, ...],
        "category_4_name": [account_id7, account_id8, ...],
        "category_5_name": [account_id9, account_id10, ...]
    }}

    Example for Formula 1 accounts:
    {{
        "F1 Drivers": ["123456", "789012"],
        "F1 Journalists": ["345678", "901234"],
        "F1 Engineers": ["567890", "123456"],
        "F1 Teams": ["789012", "345678"],
        "F1 Analysts": ["901234", "567890"]
    }}

    Example for Machine Learning accounts:
    {{
        "ML Researchers": ["123456", "789012"],
        "ML Engineers": ["345678", "901234"],
        "ML Educators": ["567890", "123456"],
        "ML Companies": ["789012", "345678"],
        "ML Enthusiasts": ["901234", "567890"]
    }}

    Return ONLY the JSON object, no additional text or explanation. Use account IDs (the "id" field) as strings, NOT usernames."""

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=messages,
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    
    result_text = response.choices[0].message.content
    
    try:
        result = json.loads(result_text)
        # Convert account IDs back to integers, and map any usernames to IDs
        categorized = {}
        for category, account_ids in result.items():
            mapped_ids = []
            for id_or_username in account_ids:
                # Check if it's a username (non-numeric string) and map to ID
                if isinstance(id_or_username, str) and not id_or_username.isdigit():
                    # Try to map username to ID
                    mapped_id = username_to_id.get(id_or_username) or username_to_id.get(id_or_username.lower())
                    if mapped_id:
                        mapped_ids.append(int(mapped_id) if isinstance(mapped_id, str) else mapped_id)
                    else:
                        # If we can't map it, skip it (or log a warning)
                        continue
                else:
                    # It's already an ID (numeric string or int)
                    mapped_ids.append(int(id_or_username) if isinstance(id_or_username, str) else id_or_username)
            categorized[category] = mapped_ids
        return categorized
    except json.JSONDecodeError:
        # Fallback: try to extract JSON from the response if it's wrapped in text
        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result_text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                categorized = {}
                for category, account_ids in result.items():
                    mapped_ids = []
                    for id_or_username in account_ids:
                        # Check if it's a username (non-numeric string) and map to ID
                        if isinstance(id_or_username, str) and not id_or_username.isdigit():
                            # Try to map username to ID
                            mapped_id = username_to_id.get(id_or_username) or username_to_id.get(id_or_username.lower())
                            if mapped_id:
                                mapped_ids.append(int(mapped_id) if isinstance(mapped_id, str) else mapped_id)
                            else:
                                # If we can't map it, skip it
                                continue
                        else:
                            # It's already an ID (numeric string or int)
                            mapped_ids.append(int(id_or_username) if isinstance(id_or_username, str) else id_or_username)
                    categorized[category] = mapped_ids
                return categorized
            except (json.JSONDecodeError, ValueError):
                pass
        
        # If all parsing fails, return accounts in a single default category
        return {
            "Uncategorized": ids
        }


async def get_expert_category_perspective(input_query: str, expert_category: str, ids: list[str]):
    """
    Stream the perspective of an expert category on a given query by analyzing their recent posts.
    This is an async generator that yields chunks of text as the perspective is generated.
    
    Args:
        input_query: The user's query/topic of interest
        expert_category: The name of the expert category (e.g., "F1 Drivers", "ML Researchers")
        ids: List of account IDs belonging to this expert category
    
    Yields:
        str: Chunks of text as the perspective is being generated
    """
    # Fetch accounts and their recent posts
    accounts = []
    for chunk in chunks(ids, 100):
        accounts += fetch_accounts(chunk)
    
    # Fetch posts for these accounts (get more posts per account for better analysis)
    posts = fetch_posts(ids, n_per_account=10, order_by="like_count")
    
    if not posts:
        yield f"No recent posts found from {expert_category} accounts related to this topic."
        return
    
    # Prepare post data for analysis (limit to most relevant/recent posts)
    # Take top posts by engagement and recency
    posts_data = []
    for post_item in posts[:50]:  # Limit to top 50 posts for analysis
        post = post_item.get("post", {})
        account = post_item.get("account", {})
        posts_data.append({
            "account_username": account.get("username", ""),
            "text": post.get("text", ""),
            "created_at": post.get("created_at", ""),
            "like_count": post.get("like_count", 0),
            "retweet_count": post.get("retweet_count", 0),
        })
    
    client = OpenAI(
        api_key=settings.XAI_TOKEN,
        base_url="https://api.x.ai/v1"
    )
    
    prompt = f"""You are analyzing the perspective of a specific expert category on a given topic. Your task is to provide a comprehensive, detailed, and elaborative analysis.

    Expert Category: {expert_category}
    User Query/Topic: {input_query}

    Recent posts from accounts in this expert category:
    {json.dumps(posts_data, indent=2)}

    Your task is to write a comprehensive, detailed, and elaborative perspective that:
    1. Analyzes how this expert category views and discusses the topic "{input_query}"
    2. Synthesizes their collective perspective - identify common themes, concerns, insights, viewpoints, and patterns
    3. Provides specific examples and quotes from their posts where relevant
    4. Explains the context and significance of their viewpoints
    5. Highlights what makes their perspective unique or valuable
    6. Discusses any trends, developments, or emerging discussions they're having
    7. Elaborates on the implications of their views and what it means for the broader conversation

    Write in a clear, engaging, and comprehensive style. Be detailed and elaborative - don't just summarize, but provide deep analysis and context. The response should be substantial (aim for 5-8 paragraphs or more if needed to fully cover the topic).

    Structure your response as a flowing narrative that:
    - Opens with an overview of how this expert category approaches the topic
    - Dives deep into specific themes, viewpoints, and discussions
    - Provides concrete examples and highlights from their recent posts
    - Explores the nuances and implications of their perspective
    - Concludes with key takeaways or emerging patterns

    Write the perspective directly, without any JSON formatting or additional structure. Just provide the comprehensive analysis as flowing text."""

    messages = [{"role": "user", "content": prompt}]
    
    # Stream the response
    stream = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=messages,
        temperature=0.4,  # Higher temperature for more creative and elaborative responses
        stream=True,  # Enable streaming
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


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
    
    # Remove URLs (replace with "link" or remove)
    cleaned_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned_text)
    cleaned_text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned_text)
    
    # Remove email addresses
    cleaned_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', cleaned_text)
    
    # Remove special markdown/social media characters that sound awkward
    cleaned_text = cleaned_text.replace('*', '')  # Bold/italic markers
    cleaned_text = cleaned_text.replace('_', '')  # Underscores
    cleaned_text = cleaned_text.replace('~', '')  # Strikethrough
    cleaned_text = cleaned_text.replace('`', '')  # Code markers
    
    # Replace multiple spaces/newlines with single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Remove leading/trailing whitespace
    cleaned_text = cleaned_text.strip()
    
    # If text is empty after cleaning, use original
    if not cleaned_text:
        cleaned_text = text
    
    return cleaned_text


def text_to_speech(text: str):
    """
    Convert text to speech using the OpenAI/Grok TTS API.
    """
    from openai import OpenAI

    # Clean the text for better speech output
    cleaned_text = clean_text_for_speech(text)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Generate speech from cleaned text
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=cleaned_text,
    )
    return speech.content


def speech_to_text(audio_file):
    """
    Convert speech to text using the OpenAI API.
    
    Args:
        audio_file: Django UploadedFile object, file-like object, bytes, or file path string
    
    Returns:
        str: Transcribed text
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Handle different input types and convert to bytes or BytesIO
    filename = "audio.mp3"
    
    if hasattr(audio_file, 'read'):
        # Django UploadedFile or file-like object - read as bytes
        # Reset file pointer to beginning in case it was already read
        audio_file.seek(0)
        audio_bytes = audio_file.read()
        # Get filename from uploaded file if available
        if hasattr(audio_file, 'name') and audio_file.name:
            filename = os.path.basename(audio_file.name)
        # Wrap in BytesIO for OpenAI/Grok API (which expects io.IOBase)
        file_obj = io.BytesIO(audio_bytes)
    elif isinstance(audio_file, bytes):
        # Bytes data - wrap in BytesIO
        file_obj = io.BytesIO(audio_file)
    elif isinstance(audio_file, str):
        # File path string - use directly (OpenAI/Grok accepts file paths)
        file_obj = audio_file
        filename = os.path.basename(audio_file)
    else:
        raise ValueError(f"Unsupported audio_file type: {type(audio_file)}")

    # OpenAI/Grok API accepts file paths directly, or (filename, file_obj) tuple for BytesIO
    if isinstance(file_obj, io.BytesIO):
        # For BytesIO, pass as tuple with filename so OpenAI can detect format
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, file_obj, "audio/mpeg") 
        )
    else:
        # For file paths, pass directly
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file_obj
        )
    return transcript.text
