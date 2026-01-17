import requests
from django.conf import settings
import time

# image_url = "https://media.formula1.com/image/upload/c_lfill,w_3392/q_auto/v1740000000/fom-website/2025/Miscellaneous/2025-start-barcelona.webp"

def generate_video_from_image(image_url: str, text: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.XAI_TOKEN}"
    }

    prompt = (
        f"Create a short video from this X post image. "
        f"Use the post text to guide the animation and bring the scene to life: {text}"
    )

    data = {
        "prompt": prompt,
        "model": "grok-imagine-video-beta",
        "image": {
            "url": image_url
        }
    }

    response = requests.post(
        "https://api.x.ai/v1/videos/generations",
        headers=headers,
        json=data
    )
    response.raise_for_status()
    result = response.json()
    request_id = result.get("request_id")
    return request_id


def fetch_video_from_request_id(request_id: str, max_sleep_time: int = 120):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.XAI_TOKEN}"
    }

    response = requests.get(
        f"https://api.x.ai/v1/videos/{request_id}",
        headers=headers
    )
    start_time = time.time()
    while response.status_code != 200:
        time.sleep(2)
        response = requests.get(
            f"https://api.x.ai/v1/videos/{request_id}",
            headers=headers
        )
        if time.time() - start_time > max_sleep_time:
            raise Exception(f"Max sleep time reached for request {request_id}")
    
    result = response.json()
    return result['video']['url']


def fetch_video_from_image(image_url: str, text: str):
    request_id = generate_video_from_image(image_url, text)
    return fetch_video_from_request_id(request_id)
