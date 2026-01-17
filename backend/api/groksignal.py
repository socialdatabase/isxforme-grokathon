from django.conf import settings
from openai import OpenAI
import json
import io
import os
import requests

from api.timeline import fetch_accounts, fetch_posts, chunks


def fetch_account_by_username(username: str):
    """
    Fetch account information from X API (formerly Twitter API) by username(s).
    Returns the same data structure as fetch_accounts.
    
    Args:
        usernames: List of usernames (without @) to fetch
    
    Returns:
        list: List of account dictionaries with user information
    """
    headers = {"Authorization": f"Bearer {settings.X_BEARER_TOKEN}", "Content-Type": "application/json"}

    url = "https://api.twitter.com/2/users/by"
    # Remove @ symbols if present in usernames
    params = {
        "usernames": username.lstrip('@'),
        "user.fields": "id,name,username,description,profile_image_url,public_metrics,verified,verified_type,created_at,location,url,entities,pinned_tweet_id,protected,withheld", #x api doesn't work when verified_type is not seelcted
    }

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    resp_data = resp.json()

    accounts = resp_data.get("data", [])
    return accounts[0]


async def generate_ai_bio_handle(handle: str):
    """
    Generate a short AI-powered bio of an X (Twitter) account based on their profile and recent activity.
    Streams the response for fast delivery.
    
    Args:
        handle: Username (with or without @) of the account
    
    Yields:
        str: Chunks of text as the bio is being generated
    """
    # Fetch account info
    account = fetch_account_by_username(handle)
    
    # Fetch recent posts - order by engagement to get most important ones
    posts = fetch_posts([account.get("id")], n_per_account=15, order_by="like_count")
    
    if not posts:
        yield f"@{account.get('username', handle)} has no recent posts available."
        return
    
    # Prepare minimal account data for speed
    public_metrics = account.get("public_metrics", {})
    account_data = {
        "name": account.get("name", ""),
        "username": account.get("username", ""),
        "description": account.get("description", ""),
        "verified": account.get("verified", False),
        "public_metrics": public_metrics,
    }
    
    # Prepare full post data for context
    top_posts = []
    for post_item in posts[:8]:
        post = post_item.get("post", {})
        # Truncate very long posts slightly for efficiency but keep full content
        text = post.get("text", "")
        if len(text) > 500:
            text = text[:497] + "..."
        top_posts.append({
            "text": text,
            "like_count": post.get("like_count", 0),
            "retweet_count": post.get("retweet_count", 0),
            "created_at": post.get("created_at", ""),
        })
    
    client = OpenAI(
        api_key=settings.XAI_TOKEN,
        base_url="https://api.x.ai/v1"
    )
    
    prompt = f"""Generate a 4-5 sentence flowing summary bio for this X (Twitter) account. 

    Account Profile:
    - Name: {account_data['name']}
    - Username: @{account_data['username']}
    - Description: {account_data['description']}
    - Verified: {account_data['verified']}

    Recent Top Posts (use these to understand their recent activity and topics):
    {json.dumps(top_posts, indent=2)}

    IMPORTANT: Write ONLY a flowing 4-5 sentence summary. Do NOT:
    - List posts as bullet points
    - Quote post text directly
    - Use phrases like "recent posts include..." or "they posted about..."
    - Break the summary into numbered points

    Instead, synthesize the information into a natural, flowing narrative that:
    1. Describes who they are based on their profile (1-2 sentences)
    2. Weaves together their recent activity themes and topics naturally (2-3 sentences)

    Output format: Plain flowing text, no formatting, no bullets, no quotes."""
    
    messages = [{"role": "user", "content": prompt}]
    
    # Stream the response for fast delivery
    stream = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=messages,
        temperature=0.3,  # Lower temperature for more focused, consistent output
        stream=True,
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


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
                        mapped_ids.append(mapped_id if isinstance(mapped_id, str) else mapped_id)
                    else:
                        # If we can't map it, skip it (or log a warning)
                        continue
                else:
                    # It's already an ID (numeric string or int)
                    mapped_ids.append(id_or_username if isinstance(id_or_username, str) else id_or_username)
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


async def get_expert_overview(input_query: str, ids: list[str]):
    """
    Stream an overview of expert views on a given query by analyzing recent posts from multiple accounts.
    This is the initial response when the user asks "What are the latest expert views on [topic]?"
    
    Args:
        input_query: The user's query/topic of interest
        ids: List of account IDs to analyze (typically top 100 from the index)
    
    Yields:
        str: Chunks of text as the response is being generated
    """
    # Fetch posts for these accounts (get posts per account for analysis)
    posts = fetch_posts(ids, n_per_account=10, order_by="like_count")
    
    if not posts:
        yield f"No recent posts found related to {input_query}."
        return
    
    # Prepare post data for analysis (limit to most relevant posts)
    posts_data = []
    for post_item in posts[:60]:  # Limit to top 60 posts for analysis
        post = post_item.get("post", {})
        account = post_item.get("account", {})
        posts_data.append({
            "account_username": account.get("username", ""),
            "account_name": account.get("name", ""),
            "text": post.get("text", ""),
            "created_at": post.get("created_at", ""),
            "like_count": post.get("like_count", 0),
            "retweet_count": post.get("retweet_count", 0),
        })
    
    client = OpenAI(
        api_key=settings.XAI_TOKEN,
        base_url="https://api.x.ai/v1"
    )
    
    prompt = f"""You are an expert analyst providing a comprehensive overview of the latest discussions and perspectives on a given topic, based on recent social media posts from relevant experts and thought leaders.

User Question: "What are the latest expert views on {input_query}?"

Recent posts from experts and thought leaders on this topic:
{json.dumps(posts_data, indent=2)}

Your task is to provide a comprehensive, well-structured response that:
1. Opens with a brief overview of the current state of discussions around "{input_query}"
2. Identifies and explains the key themes, trends, and talking points
3. Highlights notable insights, opinions, and developments from the experts
4. References specific experts using @username format inline in your text
5. Organizes the information into clear sections with <h4> headings
6. Uses <strong> tags to emphasize key terms and important points
7. Uses <ul> and <li> tags for lists where appropriate

IMPORTANT formatting rules:
- Keep any direct quotes SHORT (max 1-2 sentences). Paraphrase longer content.
- Reference experts inline like: According to <strong>@username</strong>, ...
- Do NOT use <blockquote> tags
- Do NOT include markdown or code fences
- Write clean, properly nested HTML

Write in a clear, engaging, and informative style. The response should be comprehensive (aim for 4-6 paragraphs/sections) but focused on what's most relevant and interesting."""

    messages = [{"role": "user", "content": prompt}]
    
    # Stream the response
    stream = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=messages,
        temperature=0.4,
        stream=True,
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


async def get_followup_response(
    followup_question: str,
    conversation_history: list[dict],
    input_query: str,
    ids: list[str],
    expert_category: str = None
):
    """
    Stream a response to a follow-up question, continuing the conversation context.
    
    Args:
        followup_question: The user's follow-up question
        conversation_history: Previous messages in the conversation (list of {role, content} dicts)
        input_query: The original topic/keyword
        ids: List of account IDs for context (used to fetch recent posts)
        expert_category: Optional expert category for filtering context
    
    Yields:
        str: Chunks of text as the response is being generated
    """
    # Fetch posts for context (use same posts as the conversation)
    posts = fetch_posts(ids, n_per_account=10, order_by="like_count")
    
    # Prepare post data for context
    posts_data = []
    for post_item in posts[:40]:  # Limit for follow-ups
        post = post_item.get("post", {})
        account = post_item.get("account", {})
        posts_data.append({
            "account_username": account.get("username", ""),
            "text": post.get("text", ""),
            "like_count": post.get("like_count", 0),
        })
    
    client = OpenAI(
        api_key=settings.XAI_TOKEN,
        base_url="https://api.x.ai/v1"
    )
    
    # Build the system message with context
    context_description = f"about {expert_category}" if expert_category else "from various experts"
    system_message = f"""You are an expert analyst helping users understand discussions and perspectives on "{input_query}" {context_description}.

You have access to recent posts from relevant experts on this topic:
{json.dumps(posts_data, indent=2)}

When answering follow-up questions:
1. Continue the conversation naturally, building on previous responses
2. Reference specific experts inline using <strong>@username</strong> format
3. Use HTML formatting: <strong> for emphasis, <h4> for section headings if needed, <ul>/<li> for lists
4. Keep any direct quotes SHORT (max 1-2 sentences). Paraphrase longer content.
5. Be comprehensive but focused on answering the specific question

IMPORTANT: Do NOT use <blockquote> tags. Do NOT use markdown. Write clean HTML only."""

    # Build messages with conversation history
    messages = [{"role": "system", "content": system_message}]
    
    # Add conversation history
    for msg in conversation_history:
        messages.append(msg)
    
    # Add the new follow-up question
    messages.append({"role": "user", "content": followup_question})
    
    # Stream the response
    stream = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=messages,
        temperature=0.4,
        stream=True,
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


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
    
    prompt = f"""You are analyzing the latest from a specific expert category on a given topic. Your task is to provide a comprehensive, detailed analysis.

User Question: "What's the latest from {expert_category} on {input_query}?"

Recent posts from {expert_category}:
{json.dumps(posts_data, indent=2)}

Your task is to write a comprehensive response that:
1. Covers the latest discussions and developments from {expert_category} on "{input_query}"
2. Synthesizes their collective perspective - identify common themes, concerns, insights, and patterns
3. References specific experts inline using <strong>@username</strong> format
4. Explains the context and significance of their viewpoints
5. Highlights what makes their perspective unique or valuable

Structure your response with:
- <h4> tags for section headings
- <strong> tags to emphasize key terms and expert names
- <ul> and <li> tags for lists where appropriate
- Keep any direct quotes SHORT (max 1-2 sentences). Paraphrase longer content.

IMPORTANT formatting rules:
- Do NOT use <blockquote> tags
- Do NOT use markdown or code fences
- Write clean, properly nested HTML

The response should be substantial (4-6 sections) but focused and well-organized."""

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