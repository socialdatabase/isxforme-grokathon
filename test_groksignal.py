import asyncio
from api.groksignal import get_expert_category_perspective, extract_expert_categories

# Replace with your actual IDs and query
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

async def test():
    async for chunk in get_expert_category_perspective(input_query, expert_category, expert_ids):
        print(chunk, end='', flush=True)
    print("\n")

# Run it
# asyncio.run(test())
