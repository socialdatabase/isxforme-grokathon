from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import StreamingHttpResponse, HttpResponse
import asyncio

from api.serializers import (
    FetchIdsSerializer, 
    FetchAccountsSerializer, 
    FetchPostsSerializer, 
    FetchGrokathonSizeSerializer,
    FetchIdsHandleTopicsSerializer,
    FetchTopicsAndRanksIdsSerializer,
    FetchTopicsRanksHandleSerializer,
    FetchExpertCategoriesSerializer,
    TextToSpeechSerializer,
    SpeechToTextSerializer,
)
from api.core import QueryFilter
from api.groksignal import get_expert_category_perspective, get_expert_overview, get_followup_response
from api.newspaper import generate_newspaper_articles


def test():
    from django.test import Client
    
    client = Client()
    
    # Test fetch-ids
    print("Testing fetch-ids...")
    response = client.get('/api/grokathon/fetch-ids/', {
        'input_query': 'Robotics'
    })
    result = response.json()
    ids = result.get("ids", [])
    print(f"✓ Fetched {len(ids)} IDs")
    
    if ids:
        # Test fetch-accounts
        print("Testing fetch-accounts...")
        response = client.get('/api/grokathon/fetch-accounts/', {
            'ids': ids[:10]  # Limit to first 10 for testing
        })
        result = response.json()
        accounts = result.get("accounts", [])
        print(f"✓ Fetched {len(accounts)} accounts")
        
        # Test fetch-posts
        print("Testing fetch-posts...")
        response = client.get('/api/grokathon/fetch-posts/', {
            'ids': ids[:10]  # Limit to first 10 for testing
        })
        result = response.json()
        posts = result.get("posts", [])
        print(f"✓ Fetched {len(posts)} posts")
        
        # Test fetch-ids-handle-topics
        print("Testing fetch-ids-handle-topics...")
        response = client.get('/api/grokathon/fetch-ids-handle-topics/', {
            'handle': '@thomasslabbers',
            'topics': ['Data']
        })
        result = response.json()
        handle_ids = result.get("ids", [])
        print(f"✓ Fetched {len(handle_ids)} IDs from handle")
        
            # Test fetch-topics-and-ranks-ids
        print("Testing fetch-topics-and-ranks-ids...")
        response = client.get('/api/grokathon/fetch-topics-and-ranks-ids/', {
            'ids': ids[:10]
        })
        result = response.json()
        topics = result.get("topics", [])
        ranks = result.get("ranks", [])
        print(f"✓ Fetched topics and ranks")
        
        # Test fetch-topics-ranks-handle
        print("Testing fetch-topics-ranks-handle...")
        response = client.get('/api/grokathon/fetch-topics-ranks-handle/', {
            'handle': '@f1'
        })
        result = response.json()
        topics = result.get("topics", [])
        ranks = result.get("ranks", [])
        print(f"✓ Fetched topics and ranks for handle")
        
        # Test stream-expert-perspective
        if ids:
            print("\nTesting stream-expert-perspective...")
            print("Note: This will stream the response, showing chunks as they arrive...")
            response = client.get('/api/grokathon/stream-expert-perspective/', {
                'input_query': 'Artificial Intelligence',
                'expert_category': 'AI Researchers',
                'ids': ids[:5]  # Test with first 5 IDs
            })
            print(f"✓ Response status: {response.status_code}")
            if response.status_code == 200:
                print("Streaming content (first 500 chars):")
                content = b''.join(response.streaming_content)
                text = content.decode('utf-8')
                print(text[:500] + "..." if len(text) > 500 else text)
                print(f"✓ Total streamed: {len(text)} characters")
        
        return ids, accounts, posts
    
    return ids, [], []


@method_decorator(csrf_exempt, name='dispatch')
class GrokathonViewSet(viewsets.GenericViewSet):
    """Open Grokathon API endpoints - no authentication or CSRF required"""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = None
    filter_backends = [QueryFilter]
    query_filters = []

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchIdsSerializer,
        filter_backends=[QueryFilter],
        query_filters=["input_query"],
        url_path="fetch-ids",
        url_name="fetch-ids",
    )
    def fetch_ids(self, request):
        input_query = request.GET.get("input_query")
        serializer = FetchIdsSerializer(data={"input_query": input_query})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchAccountsSerializer,
        filter_backends=[QueryFilter],
        query_filters=["ids"],
        url_path="fetch-accounts",
        url_name="fetch-accounts",
    )
    def fetch_accounts(self, request):
        ids = request.GET.getlist("ids")
        serializer = FetchAccountsSerializer(data={"ids": ids})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchPostsSerializer,
        filter_backends=[QueryFilter],
        query_filters=["ids"],
        url_path="fetch-posts",
        url_name="fetch-posts",
    )
    def fetch_posts(self, request):
        ids = request.GET.getlist("ids")
        serializer = FetchPostsSerializer(data={"ids": ids})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchGrokathonSizeSerializer,
        filter_backends=[QueryFilter],
        query_filters=["ids"],
        url_path="fetch-grokathon-size",
        url_name="fetch-grokathon-size",
    )
    def fetch_grokathon_size(self, request):
        ids = request.GET.getlist("ids")
        serializer = FetchGrokathonSizeSerializer(data={"ids": ids})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchIdsHandleTopicsSerializer,
        filter_backends=[QueryFilter],
        query_filters=["handle", "topics"],
        url_path="fetch-ids-handle-topics",
        url_name="fetch-ids-handle-topics",
    )
    def fetch_ids_handle_topics(self, request):
        # To get ids outside of the community of the handle
        handle = request.GET.get("handle")
        topics = request.GET.getlist("topics")
        serializer = FetchIdsHandleTopicsSerializer(data={"handle": handle, "topics": topics})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchTopicsAndRanksIdsSerializer,
        filter_backends=[QueryFilter],
        query_filters=["ids"],
        url_path="fetch-topics-and-ranks-ids", 
        url_name="fetch-topics-and-ranks-ids",
    )
    def fetch_topics_and_ranks_ids(self, request):
        # To fetch the top topics (of ids) and the ranks of the ids
        ids = request.GET.getlist("ids")
        serializer = FetchTopicsAndRanksIdsSerializer(data={"ids": ids})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchTopicsRanksHandleSerializer,
        filter_backends=[QueryFilter],
        query_filters=["handle"],
        url_path="fetch-topics-ranks-handle",
        url_name="fetch-topics-ranks-handle",
    )
    def fetch_topics_ranks_handle(self, request):
        # Fetch the ranks of the handle and the top topics the handle is interested in
        handle = request.GET.get("handle")
        serializer = FetchTopicsRanksHandleSerializer(data={"handle": handle})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchExpertCategoriesSerializer,
        filter_backends=[QueryFilter],
        query_filters=["ids"],
        url_path="fetch-expert-categories",
        url_name="fetch-expert-categories",
    )
    def fetch_expert_categories(self, request):
        ids = request.GET.getlist("ids")
        serializer = FetchExpertCategoriesSerializer(data={"ids": ids})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        filter_backends=[QueryFilter],
        query_filters=["input_query", "expert_category", "ids"],
        url_path="stream-expert-perspective",
        url_name="stream-expert-perspective",
    )
    def stream_expert_perspective(self, request):
        """
        Stream the perspective of an expert category on a given query.
        
        Query parameters:
        - input_query: The user's query/topic of interest
        - expert_category: The name of the expert category (e.g., "F1 Drivers", "ML Researchers")
        - ids: List of account IDs belonging to this expert category (comma-separated or multiple)
        
        Returns a streaming text response.
        """
        input_query = request.GET.get("input_query")
        expert_category = request.GET.get("expert_category")
        ids = [int(id_val) for id_val in request.GET.getlist("ids") if id_val]
        
        if not input_query or not expert_category or not ids:
            return Response(
                {"error": "Missing required parameters: input_query, expert_category, and ids"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        def stream_generator():
            """Convert async generator to sync generator for StreamingHttpResponse"""
            async def run_stream():
                async for chunk in get_expert_category_perspective(input_query, expert_category, ids):
                    yield chunk
            
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Run the async generator
                async_gen = run_stream()
                while True:
                    try:
                        chunk = loop.run_until_complete(async_gen.__anext__())
                        # StreamingHttpResponse expects bytes
                        if isinstance(chunk, str):
                            yield chunk.encode('utf-8')
                        else:
                            yield chunk
                    except StopAsyncIteration:
                        break
            finally:
                loop.close()
        
        response = StreamingHttpResponse(
            stream_generator(),
            content_type='text/plain; charset=utf-8'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
        return response

    @action(
        detail=False,
        methods=["get"],
        filter_backends=[QueryFilter],
        query_filters=["input_query", "ids"],
        url_path="stream-expert-overview",
        url_name="stream-expert-overview",
    )
    def stream_expert_overview(self, request):
        """
        Stream an overview of expert views on a given query.
        This is the initial response when the user asks "What are the latest expert views on [topic]?"
        
        Query parameters:
        - input_query: The user's query/topic of interest
        - ids: List of account IDs to analyze (comma-separated or multiple)
        
        Returns a streaming text response.
        """
        input_query = request.GET.get("input_query")
        ids = [int(id_val) for id_val in request.GET.getlist("ids") if id_val]
        
        if not input_query or not ids:
            return Response(
                {"error": "Missing required parameters: input_query and ids"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        def stream_generator():
            """Convert async generator to sync generator for StreamingHttpResponse"""
            async def run_stream():
                async for chunk in get_expert_overview(input_query, ids):
                    yield chunk
            
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Run the async generator
                async_gen = run_stream()
                while True:
                    try:
                        chunk = loop.run_until_complete(async_gen.__anext__())
                        # StreamingHttpResponse expects bytes
                        if isinstance(chunk, str):
                            yield chunk.encode('utf-8')
                        else:
                            yield chunk
                    except StopAsyncIteration:
                        break
            finally:
                loop.close()
        
        response = StreamingHttpResponse(
            stream_generator(),
            content_type='text/plain; charset=utf-8'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
        return response

    @action(
        detail=False,
        methods=["post"],
        url_path="stream-followup",
        url_name="stream-followup",
    )
    def stream_followup(self, request):
        """
        Stream a response to a follow-up question in an ongoing conversation.
        
        POST body (JSON):
        - followup_question: The user's follow-up question
        - conversation_history: List of previous messages [{role: "user"|"assistant", content: "..."}]
        - input_query: The original topic/keyword
        - ids: List of account IDs for context
        - expert_category: Optional expert category name
        
        Returns a streaming text response.
        """
        import json as json_module
        
        data = request.data
        followup_question = data.get("followup_question")
        conversation_history = data.get("conversation_history", [])
        input_query = data.get("input_query")
        ids = data.get("ids", [])
        expert_category = data.get("expert_category")
        
        if not followup_question or not input_query:
            return Response(
                {"error": "Missing required parameters: followup_question and input_query"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert ids to integers if they're strings
        ids = [int(id_val) if isinstance(id_val, str) else id_val for id_val in ids]
        
        def stream_generator():
            """Convert async generator to sync generator for StreamingHttpResponse"""
            async def run_stream():
                async for chunk in get_followup_response(
                    followup_question,
                    conversation_history,
                    input_query,
                    ids,
                    expert_category
                ):
                    yield chunk
            
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Run the async generator
                async_gen = run_stream()
                while True:
                    try:
                        chunk = loop.run_until_complete(async_gen.__anext__())
                        # StreamingHttpResponse expects bytes
                        if isinstance(chunk, str):
                            yield chunk.encode('utf-8')
                        else:
                            yield chunk
                    except StopAsyncIteration:
                        break
            finally:
                loop.close()
        
        response = StreamingHttpResponse(
            stream_generator(),
            content_type='text/plain; charset=utf-8'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
        return response

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=TextToSpeechSerializer,
        filter_backends=[QueryFilter],
        query_filters=["text"],
        url_path="text-to-speech",
        url_name="text-to-speech",
    )
    def text_to_speech(self, request):
        """
        Convert text to speech.
        
        Query parameters (GET) or body (POST):
        - text: The text to convert to speech
        
        Returns an audio file (MP3 format).
        """
        # Support both GET and POST
        if request.method == 'GET':
            text = request.GET.get("text")
        else:
            text = request.data.get("text") or request.GET.get("text")
        
        if not text:
            return Response(
                {"error": "Missing required parameter: text"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TextToSpeechSerializer(data={"text": text})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        audio_content = serializer.instance.get("audio")
        
        if not audio_content:
            return Response(
                {"error": "Failed to generate speech"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Return audio file as response
        response = HttpResponse(audio_content, content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename="speech.mp3"'
        response['Content-Length'] = len(audio_content)
        return response

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=SpeechToTextSerializer,
        filter_backends=[QueryFilter],
        query_filters=["audio"],
        url_path="speech-to-text",
        url_name="speech-to-text",
    )
    def speech_to_text(self, request):
        """
        Convert speech to text.
        
        POST request with multipart/form-data:
        - audio: The audio file to convert to text (file upload)
        
        Returns a text response.
        """
        # File uploads must use POST with multipart/form-data
        if request.method != 'POST':
            return Response(
                {"error": "This endpoint only accepts POST requests with file upload"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        audio_file = request.FILES.get("audio")
        
        if not audio_file:
            return Response(
                {"error": "Missing required file: audio"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SpeechToTextSerializer(data={"audio": audio_file})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="generate-newspaper",
        url_name="generate-newspaper",
    )
    def generate_newspaper(self, request):
        """
        Generate newspaper-style articles from social media posts using Grok.
        
        POST body (JSON):
        - keyword: The topic/keyword for the newspaper edition
        - posts: List of post objects with author, username, text, likes, retweets
        
        Returns JSON with articles.
        """
        # Use request.data for DRF compatibility (handles JSON parsing)
        data = request.data
        
        keyword = data.get("keyword")
        posts = data.get("posts", [])
        
        if not keyword:
            return Response(
                {"error": "Missing required parameter: keyword"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not posts:
            return Response(
                {"error": "Missing required parameter: posts"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = generate_newspaper_articles(keyword, posts)
        return Response(result)