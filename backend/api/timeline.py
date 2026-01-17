from django.conf import settings
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from openai import OpenAI
import json
import time

BASE_URL_SDB = "https://api.socialdatabase.com"


def chunks(input_list, end, start=0):
    for start_index in range(start, len(input_list), end):
        yield input_list[start_index : start_index + end]



def analyze_query(input_query: str):    
    # Initialize OpenAI client for xAI API
    client = OpenAI(
        api_key=settings.XAI_TOKEN,
        base_url="https://api.x.ai/v1"
    )

    prompt = f"""Analyze the following user query and extract information optimized for social media search (X/Twitter, Reddit, LinkedIn, etc.).

    Query: "{input_query}"

    Extract and return ONLY a valid JSON object with these exact keys:
    - "keywords": A list of 1-2 main keywords/terms that users would likely have in their social media bios, profiles, or mention in posts. These should be the most important, concise, and searchable terms (e.g., "machine learning" or "AI researcher").
    - "countries": A list of ISO 3166-1 alpha-2 country codes (e.g., ["US", "GB", "CA"]) if the query mentions specific countries or regions. If no countries are mentioned, return null or an empty list.
    - "query_type": Either "interest" or "profession" - determine if the query relates to a hobby/interest or a professional/career topic.

    Examples:
    - Query: "AI researchers in the US" → {{"keywords": ["AI researcher", "artificial intelligence"], "countries": ["US"], "query_type": "profession"}}
    - Query: "python developers" → {{"keywords": ["python developer"], "countries": null, "query_type": "profession"}}
    - Query: "photography enthusiasts" → {{"keywords": ["photography"], "countries": null, "query_type": "interest"}}
    - Query: "data scientists in Europe" → {{"keywords": ["data scientist"], "countries": ["DE", "FR", "GB", "IT", "ES"], "query_type": "profession"}}

    Return ONLY the JSON object, no additional text or explanation."""

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=messages,
        temperature=0.1,  # Lower temperature for faster, more deterministic responses
        response_format={"type": "json_object"},  # Force JSON response
    )
    
    result_text = response.choices[0].message.content
    
    try:
        result = json.loads(result_text)
        # Ensure all required keys exist and validate structure
        return {
            "keywords": result.get("keywords", []),
            "countries": result.get("countries") if result.get("countries") else None,
            "plan_type": result.get("query_type", "interest")
        }
    except json.JSONDecodeError:
        # Fallback: try to extract JSON from the response if it's wrapped in text
        import re
        json_match = re.search(r'\{[^{}]*\}', result_text)
        if json_match:
            try:
                result = json.loads(json_match.group())
                return {
                    "keywords": result.get("keywords", []),
                    "countries": result.get("countries") if result.get("countries") else None,
                    "plan_type": result.get("query_type", "interest")
                }
            except json.JSONDecodeError:
                pass
        
        # If all parsing fails, return a default structure
        return {
            "keywords": [input_query],
            "countries": None,
            "plan_type": "interest"
        }


def fetch_topics():
    url = f"{BASE_URL_SDB}/api/external/bigdipper/fetch-topics-grokathon/"
    headers = {"Authorization": f"Token {settings.SOCIAL_DATABASE_TOKEN}", "Content-Type": "application/json"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    resp_data = resp.json()
    topics = resp_data.get("topics", [])
    all_topics = resp_data.get("all_topics", [])
    return topics, all_topics


def infer_topic_in_query(input_query: str):
    _, all_topics = fetch_topics()
    input_query = input_query.lower()
    for topic in all_topics:
        if topic in input_query:
            return topic
    return None


def fetch_grokathon_ids(input_query: str):
    start_time = time.time()
    if "@" in input_query:
        keywords = [word.strip() for word in input_query.split(" ") if word.startswith("@")]
        params = {"keywords": keywords, "plan_type": "interest", "countries": []}
    else:
        params = analyze_query(input_query)
        if not params.get("countries"):
            params["countries"] = ["us"]
    print(f"Time taken to analyze query: {time.time() - start_time} seconds")

    url = f"{BASE_URL_SDB}/api/external/bigdipper/fetch-grokathon-ids/"
    headers = {
        "Authorization": f"Token {settings.SOCIAL_DATABASE_TOKEN}",
        "Content-Type": "application/json"
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    resp_data = resp.json()
    ids = resp_data.get("ids", [])
    print(f"Time taken to fetch ids: {time.time() - start_time} seconds")
    ids = [str(account_id) for account_id in ids]
    return ids


def fetch_grokathon_size(ids: list[str]):
    headers = {"Authorization": f"Token {settings.SOCIAL_DATABASE_TOKEN}", "Content-Type": "application/json"}
    url = f"{BASE_URL_SDB}/api/external/bigdipper/fetch-size-grokathon-ids/"
    ids = [int(account_id) for account_id in ids]
    params = {"ids": ids}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    resp_data = resp.json()
    size = resp_data.get("size", 0)
    return size


def fetch_accounts(ids: list[str]):
    headers = {"Authorization": f"Bearer {settings.X_BEARER_TOKEN}", "Content-Type": "application/json"}

    url = "https://api.twitter.com/2/users"
    params = {
        "ids": ",".join([str(i) for i in ids]),
        "user.fields": "id,name,username,description,profile_image_url,public_metrics,verified,verified_type,created_at,location,url,entities,pinned_tweet_id,protected,withheld", #x api doesn't work when verified_type is not seelcted
    }

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    resp_data = resp.json()

    accounts = resp_data.get("data", [])
    return accounts


def process_media_data(media_data: list[dict]):
    media_dict = {}
    for media in media_data:
        if "variants" in media:
            media_url = [variant["url"] for variant in media["variants"] if variant.get("content_type") == "video/mp4"][
                -1
            ]
        elif "url" in media:
            media_url = media.get("url")
        else:
            media_url = None
        media_key = media.get("media_key")
        media_type = media.get("type")
        media_width = media.get("width")
        media_height = media.get("height")
        preview_image_url = media.get("preview_image_url")  # Thumbnail for videos
        media_dict[media_key] = {
            "url": media_url, 
            "type": media_type, 
            "width": media_width, 
            "height": media_height,
            "preview_image_url": preview_image_url
        }
    return media_dict


def process_post_items(
    post_items: list[dict],
    media_dict: dict,
    accounts_dict: dict = None,
    order_by: str = "created_at"
):
    posts = []
    for item in post_items:
        post = item["public_metrics"]
        post["created_at"] = item["created_at"]
        post["account_id"] = item["author_id"]
        post["id"] = item["id"]
        post["text"] = item["text"]

        # Determine post type from referenced_tweets
        post_type = "original"
        if "referenced_tweets" in item and item["referenced_tweets"]:
            referenced_types = [ref["type"] for ref in item["referenced_tweets"]]
            if "quoted" in referenced_types:
                post_type = "quote"
        post["post_type"] = post_type

        if "entities" in item:
            urls = item.get("entities", {}).get("urls")
            if urls:
                medias = []
                new_urls = []
                for url in urls:
                    media_key = url.get("media_key")
                    media = media_dict.get(media_key, {})
                    if media:
                        media["start"] = url.get("start")
                        media["end"] = url.get("end")
                        medias.append(media)
                    else:
                        new_urls.append(url)

                post["urls"] = new_urls
                post["media"] = medias

        account = accounts_dict.get(post["account_id"], {})
        if not account:
            continue

        posts.append(
            {
                "post": post,
                "account": {
                    "id": account["id"],
                    "username": account["username"],
                    "verified": account["verified"],
                    "profile_image_url": account["profile_image_url"],
                },
            }
        )
    posts = sorted(posts, key=lambda x: x["post"][order_by], reverse=True)
    return posts


def fetch_posts(ids: list[str], n_per_account: int = 5, order_by: str = "created_at"):
    headers = {"Authorization": f"Bearer {settings.X_BEARER_TOKEN}", "Content-Type": "application/json"}

    # Fetch posts per account concurrently
    post_items = []
    media_data = []
    users_data = []

    def _fetch_user_posts(user_id):
        url = f"https://api.twitter.com/2/users/{user_id}/tweets"

        # Calculate max start_time (1 month ago)
        one_month_ago = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

        params = {
            "max_results": n_per_account,  # API limit is 100
            "tweet.fields": "public_metrics,entities,attachments,created_at,author_id,referenced_tweets",
            "expansions": "attachments.media_keys,author_id",
            "media.fields": "media_key,type,url,preview_image_url,alt_text,variants,width,height",
            "user.fields": "id,username,verified,profile_image_url",
            "exclude": "retweets,replies",  # Exclude retweets and replies by default
            "start_time": one_month_ago,  # Maximum 1 month old
        }

        resp = requests.get(url, params=params, headers=headers)
        resp_data = resp.json()
        includes = resp_data.get("includes", {})
        return {
            "post_items": resp_data.get("data", []),
            "media_data": includes.get("media", []),
            "users_data": includes.get("users", []),
        }

    max_workers = min(5, len(ids)) or 1

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_user = {executor.submit(_fetch_user_posts, user_id): user_id for user_id in ids}
        for future in as_completed(future_to_user):
            try:
                result = future.result()
            except Exception:
                # If one user fails, skip it and continue with others
                continue
            post_items.extend(result.get("post_items", []))
            media_data.extend(result.get("media_data", []))
            users_data.extend(result.get("users_data", []))

    # Build accounts_dict from users_data (keyed by user id as int)
    accounts_dict = {}
    for user in users_data:
        accounts_dict[user["id"]] = {
            "id": user["id"],
            "username": user.get("username", ""),
            "verified": user.get("verified", False),
            "profile_image_url": user.get("profile_image_url", ""),
        }

    media_dict = process_media_data(media_data)
    posts = process_post_items(post_items, media_dict, accounts_dict, order_by)

    # Order by likes or recency, default is likes
    posts = sorted(posts, key=lambda x: x["post"][order_by], reverse=True)
    return posts


def fetch_posts_timeline(ids: list[str], n_per_account: int = 5, order_by: str = "created_at"):
    posts = fetch_posts(ids, n_per_account, order_by)
    
    if not posts:
        return posts
    
    # Calculate median like count without numpy
    like_counts = [post["post"].get("like_count", 0) for post in posts]
    sorted_counts = sorted(like_counts)
    n = len(sorted_counts)
    if n == 0:
        median_like_count = 0
    elif n % 2 == 0:
        median_like_count = (sorted_counts[n // 2 - 1] + sorted_counts[n // 2]) / 2
    else:
        median_like_count = sorted_counts[n // 2]
    
    # Filter posts to only include those with like_count > median
    filtered_posts = [post for post in posts if post["post"].get("like_count", 0) > median_like_count]
    
    # If no posts pass the filter, return original posts
    if not filtered_posts:
        return posts
    
    # Distribute posts evenly across authors
    # Priority: authors not yet in the list get priority
    distributed_posts = []
    authors_in_list = set()  # Track which authors are already represented
    posts_to_append = []  # Posts from authors already in list (to append at the end)
    
    # Get all unique authors from filtered posts
    all_unique_authors = set(post["post"].get("account_id") for post in filtered_posts)
    
    # First pass: prioritize posts from authors not yet in the list
    for post in filtered_posts:
        account_id = post["post"].get("account_id")
        if account_id not in authors_in_list:
            # This author is not yet in the list, add the post immediately
            distributed_posts.append(post)
            authors_in_list.add(account_id)
        else:
            # This author is already in the list, save for later
            posts_to_append.append(post)
    
    # Second pass: only add posts from authors already in list if all authors are represented
    all_authors_represented = len(authors_in_list) == len(all_unique_authors)
    
    if all_authors_represented:
        # All authors have at least one post, now we can add additional posts
        # Sort by engagement to prioritize high-engagement posts
        posts_to_append.sort(key=lambda x: x["post"].get("like_count", 0), reverse=True)
        
        # Track post counts per author to maintain even distribution
        author_post_counts = {account_id: 1 for account_id in authors_in_list}
        
        for post in posts_to_append:
            account_id = post["post"].get("account_id")
            # Find the minimum number of posts any author has
            min_posts = min(author_post_counts.values())
            
            # Only add if this author doesn't have more posts than the minimum
            if author_post_counts.get(account_id, 0) <= min_posts:
                distributed_posts.append(post)
                author_post_counts[account_id] = author_post_counts.get(account_id, 0) + 1
    
    # Track which posts have been added to distributed_posts
    added_post_ids = {post["post"].get("id") for post in distributed_posts}
    
    # Append all leftover posts from filtered_posts that weren't added yet
    leftover_posts = [post for post in filtered_posts if post["post"].get("id") not in added_post_ids]
    
    # Sort leftover posts by engagement and append at the end
    leftover_posts.sort(key=lambda x: x["post"].get("created_at", 0), reverse=True)
    distributed_posts.extend(leftover_posts)
    
    return distributed_posts


def fetch_ids_handle_topics(handle: str, topics: list[str]):
    # To get ids outside of the community of the handle
    url = f"{BASE_URL_SDB}/api/external/bigdipper/fetch-ids-handles-topics/"
    headers = {"Authorization": f"Token {settings.SOCIAL_DATABASE_TOKEN}", "Content-Type": "application/json"}
    params = {"handle": handle, "topics": topics, "limit": 100}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    resp_data = resp.json()
    ids = resp_data.get("ids", [])
    ids = [str(account_id) for account_id in ids]
    return ids


def fetch_topics_and_ranks_ids(ids: list[str]):
    # To fetch the top topics (of ids) and the ranks of the ids
    url = f"{BASE_URL_SDB}/api/external/bigdipper/fetch-topics-and-ranks-ids/"
    headers = {"Authorization": f"Token {settings.SOCIAL_DATABASE_TOKEN}", "Content-Type": "application/json"}
    ids = [int(account_id) for account_id in ids]
    params = {"ids": ids, "top_n": 10}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    resp_data = resp.json()
    topics = resp_data.get("topics", [])
    ranks = resp_data.get("accounts_ranks", [])
    return topics, ranks


def get_accounts_with_ranks(input_query: str):
    ids = fetch_grokathon_ids(input_query)
    accounts = fetch_accounts(ids)
    _, ranks = fetch_topics_and_ranks_ids(ids)
    for account in accounts:
        account["rank"] = ranks.get(account["id"], [])
    return accounts


def fetch_topics_ranks_handle(handle: str):
    # Fetch the ranks of the handle and the top topics the handle is interested in
    url = f"{BASE_URL_SDB}/api/external/bigdipper/fetch-topics-ranks-handle/"
    headers = {"Authorization": f"Token {settings.SOCIAL_DATABASE_TOKEN}", "Content-Type": "application/json"}
    params = {"handle": handle}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    resp_data = resp.json()
    topics = resp_data.get("topics", [])
    ranks = resp_data.get("accounts_ranks", [])
    return topics, ranks
