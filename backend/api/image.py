from xai_sdk import Client
from django.conf import settings

client = Client(api_key=settings.XAI_TOKEN)

empire_state_building = (
    "https://images.unsplash.com/photo-1761301006532-fa8143787a88?"
    "ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3"
    "D%3D&auto=format&fit=crop&q=80&w=987"
)

response = client.video.generate(
    prompt="Make lightning strike the top of the empire state building",
    model="grok-imagine-video-beta",
    image_url=empire_state_building,
)

print(response.url)
