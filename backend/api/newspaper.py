from django.conf import settings
from openai import OpenAI
import json


def generate_newspaper_articles(keyword: str, posts: list[dict]):
    """
    Generate newspaper-style articles from social media posts using Grok.
    
    Args:
        keyword: The topic/keyword for the newspaper edition
        posts: List of post objects with author, username, text, likes, retweets
    
    Returns:
        dict: {
            "articles": [
                {
                    "headline": "...",
                    "author": "...",
                    "section": "...",
                    "content": "...",
                    "imageCaption": "...",
                    "source_usernames": ["user1", "user2"]
                },
                ...
            ]
        }
    """
    if not posts:
        return {"articles": []}
    
    # Prepare posts data for the prompt
    posts_text = "\n\n".join([
        f"Post by {p.get('author', 'Unknown')} (@{p.get('username', 'unknown')}):\n"
        f"\"{p.get('text', '')}\"\n"
        f"Engagement: {p.get('likes', 0)} likes, {p.get('retweets', 0)} retweets"
        for p in posts[:50]  # Limit to 50 posts
    ])
    
    client = OpenAI(
        api_key=settings.XAI_TOKEN,
        base_url="https://api.x.ai/v1"
    )
    
    prompt = f"""You are the editor-in-chief of "The Grok Times", a prestigious newspaper combining the journalistic excellence of The New York Times with the magical charm of the Daily Prophet from Harry Potter.

Your task: Transform the following social media posts about "{keyword}" into compelling newspaper articles.

SOCIAL MEDIA POSTS:
{posts_text}

INSTRUCTIONS:
1. Write 5-7 newspaper articles based on the posts above
2. The FIRST article should be the lead story - the most important/interesting news, comprehensive coverage
3. Remaining articles should cover different angles, perspectives, or sub-topics
4. Write in classic newspaper style - factual, authoritative, but with a touch of wit
5. Each article should synthesize information from multiple posts when relevant
6. Create dramatic but accurate headlines (like NYT meets Daily Prophet)
7. Attribute quotes and information to the original posters
8. For each article, list the source_usernames: the usernames (without the @ symbol) of the primary posters whose posts were used to generate this article

For each article provide:
- headline: A compelling newspaper headline (dramatic but factual)
- author: A fitting byline (can be creative like "Special Correspondent" or "Our {keyword} Editor")
- section: The newspaper section (e.g., "Front Page", "Sports", "Technology", "Opinion", "Breaking News")
- content: The article text (2-4 paragraphs, proper newspaper style)
- imageCaption: A caption for an accompanying image
- source_usernames: Array of usernames (without @) of the main sources used

Return ONLY a valid JSON object with this structure:
{{
    "articles": [
        {{
            "headline": "string",
            "author": "string", 
            "section": "string",
            "content": "string",
            "imageCaption": "string",
            "source_usernames": ["string", "string"]
        }}
    ]
}}"""

    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = client.chat.completions.create(
            model="grok-3-fast",
            messages=messages,
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        return result
        
    except Exception as e:
        print(f"Error generating newspaper articles: {e}")
        return {"articles": []}
