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
    FetchTopicsSerializer,
    InferTopicInQuerySerializer,
    FetchIdsHandleTopicsSerializer,
    FetchTopicsAndRanksIdsSerializer,
    GetAccountsWithRanksSerializer,
    FetchTopicsRanksHandleSerializer,
    FetchExpertCategoriesSerializer,
    FetchPostsTimelineSerializer,
    XaiTextToSpeechSerializer,
    XaiSpeechToTextSerializer,
    XaiVoicesSerializer,
)
from api.core import QueryFilter
from api.groksignal import get_expert_category_perspective, get_expert_overview, get_followup_response, generate_ai_bio_handle, fetch_account_by_username, get_expert_debate_response
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
        serializer_class=FetchPostsTimelineSerializer,
        filter_backends=[QueryFilter],
        query_filters=["ids"],
        url_path="fetch-posts-timeline",
        url_name="fetch-posts-timeline",
    )
    def fetch_posts_timeline(self, request):
        ids = request.GET.getlist("ids")
        serializer = FetchPostsTimelineSerializer(data={"ids": ids})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=FetchTopicsSerializer,
        filter_backends=[QueryFilter],
        query_filters=[],
        url_path="fetch-topics",
        url_name="fetch-topics",
    )
    def fetch_topics(self, request):
        serializer = FetchTopicsSerializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=InferTopicInQuerySerializer,
        filter_backends=[QueryFilter],
        query_filters=["input_query"],
        url_path="infer-topic-in-query",
        url_name="infer-topic-in-query",
    )
    def infer_topic_in_query(self, request):
        input_query = request.GET.get("input_query")
        serializer = InferTopicInQuerySerializer(data={"input_query": input_query})
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
        serializer_class=GetAccountsWithRanksSerializer,
        filter_backends=[QueryFilter],
        query_filters=["input_query"],
        url_path="get-accounts-with-ranks",
        url_name="get-accounts-with-ranks",
    )
    def get_accounts_with_ranks(self, request):
        input_query = request.GET.get("input_query")
        serializer = GetAccountsWithRanksSerializer(data={"input_query": input_query})
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
        filter_backends=[QueryFilter],
        query_filters=["handle"],
        url_path="fetch-account-handle",
        url_name="fetch-account-handle",
    )
    def fetch_account_handle(self, request):
        """Fetch account details by username/handle"""
        handle = request.GET.get("handle")
        if not handle:
            return Response({"error": "handle parameter required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account = fetch_account_by_username(handle)
            return Response({"account": account})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        query_filters=["handle"],
        url_path="generate-ai-bio-handle",
        url_name="generate-ai-bio-handle",
    )
    def generate_ai_bio_handle(self, request):
        handle = request.GET.get("handle")

        def stream_generator():
            """Convert async generator to sync generator for StreamingHttpResponse"""
            async def run_stream():
                async for chunk in generate_ai_bio_handle(handle):
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
        methods=["post"],
        url_path="stream-debate-response",
        url_name="stream-debate-response",
    )
    def stream_debate_response(self, request):
        """
        Stream an expert's response in a debate context.
        The expert responds based on their posts and what others have said.
        
        POST body (JSON):
        - question: The debate question/topic
        - expert_name: Display name of the expert
        - expert_username: Username of the expert
        - expert_role: Role/category (e.g., "F1 Driver")
        - expert_posts: List of expert's posts [{text, like_count}]
        - conversation_history: Previous responses [{speaker_name, speaker_role, text}]
        - is_first_speaker: Boolean, whether this is the first speaker
        
        Returns a streaming text response.
        """
        data = request.data
        question = data.get("question")
        expert_name = data.get("expert_name")
        expert_username = data.get("expert_username")
        expert_role = data.get("expert_role")
        expert_posts = data.get("expert_posts", [])
        conversation_history = data.get("conversation_history", [])
        is_first_speaker = data.get("is_first_speaker", False)
        
        if not question or not expert_name or not expert_username:
            return Response(
                {"error": "Missing required parameters: question, expert_name, expert_username"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        def stream_generator():
            """Convert async generator to sync generator for StreamingHttpResponse"""
            async def run_stream():
                async for chunk in get_expert_debate_response(
                    question=question,
                    expert_name=expert_name,
                    expert_username=expert_username,
                    expert_role=expert_role or "Expert",
                    expert_posts=expert_posts,
                    conversation_history=conversation_history,
                    is_first_speaker=is_first_speaker
                ):
                    yield chunk
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                async_gen = run_stream()
                while True:
                    try:
                        chunk = loop.run_until_complete(async_gen.__anext__())
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
        response['X-Accel-Buffering'] = 'no'
        return response

    # ==================== xAI Voice API Endpoints ====================
    
    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=XaiTextToSpeechSerializer,
        filter_backends=[QueryFilter],
        query_filters=["text", "voice"],
        url_path="xai-text-to-speech",
        url_name="xai-text-to-speech",
    )
    def xai_text_to_speech(self, request):
        """
        Convert text to speech using xAI's Grok Voice API.
        
        Query parameters (GET) or body (POST):
        - text: The text to convert to speech (required)
        - voice: Voice to use - ara, rex, sal, eve, una, leo (optional, default: ara)
        
        Returns an audio file (WAV format, PCM linear16, 24kHz).
        """
        # Support both GET and POST
        if request.method == 'GET':
            text = request.GET.get("text")
            voice = request.GET.get("voice", "ara")
        else:
            text = request.data.get("text") or request.GET.get("text")
            voice = request.data.get("voice") or request.GET.get("voice", "ara")
        
        if not text:
            return Response(
                {"error": "Missing required parameter: text"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = XaiTextToSpeechSerializer(data={"text": text, "voice": voice})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        audio_content = serializer.instance.get("audio")
        
        if not audio_content:
            return Response(
                {"error": "Failed to generate speech"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Return audio file as response
        response = HttpResponse(audio_content, content_type='audio/wav')
        response['Content-Disposition'] = 'inline; filename="speech.wav"'
        response['Content-Length'] = len(audio_content)
        return response

    @action(
        detail=False,
        methods=["post"],
        serializer_class=XaiSpeechToTextSerializer,
        filter_backends=[QueryFilter],
        query_filters=[],
        url_path="xai-speech-to-text",
        url_name="xai-speech-to-text",
    )
    def xai_speech_to_text(self, request):
        """
        Convert speech to text using xAI's Grok Voice API.
        
        POST request with multipart/form-data:
        - audio: The audio file to convert to text (file upload)
                 Recommended: WAV format, PCM linear16, 16kHz
        
        Returns JSON with transcribed text.
        """
        audio_file = request.FILES.get("audio")
        
        if not audio_file:
            return Response(
                {"error": "Missing required file: audio"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = XaiSpeechToTextSerializer(data={"audio": audio_file})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        serializer_class=XaiVoicesSerializer,
        filter_backends=[QueryFilter],
        query_filters=[],
        url_path="xai-voices",
        url_name="xai-voices",
    )
    def xai_voices(self, request):
        """
        Get the list of available xAI voices for text-to-speech.
        
        Returns JSON with list of voice IDs: ara, rex, sal, eve, una, leo
        """
        serializer = XaiVoicesSerializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post", "get"],
        filter_backends=[QueryFilter],
        query_filters=["text", "voice"],
        url_path="xai-text-to-speech-stream",
        url_name="xai-text-to-speech-stream",
    )
    def xai_text_to_speech_stream(self, request):
        """
        Stream text to speech using xAI's Grok Voice API.
        Returns audio chunks as they're generated for real-time playback.
        
        Query parameters (GET) or body (POST):
        - text: The text to convert to speech (required)
        - voice: Voice to use - ara, rex, sal, eve, una, leo (optional, default: ara)
        
        Returns streaming audio (PCM linear16, 24kHz).
        """
        from api.voicethomas import text_to_speech_stream
        
        # Support both GET and POST
        if request.method == 'GET':
            text = request.GET.get("text")
            voice = request.GET.get("voice", "ara")
        else:
            text = request.data.get("text") or request.GET.get("text")
            voice = request.data.get("voice") or request.GET.get("voice", "ara")
        
        if not text:
            return Response(
                {"error": "Missing required parameter: text"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        def stream_generator():
            """Stream audio chunks from xAI TTS."""
            for chunk in text_to_speech_stream(text, voice_id=voice):
                yield chunk
        
        response = StreamingHttpResponse(
            stream_generator(),
            content_type='audio/pcm'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        response['X-Audio-Sample-Rate'] = '24000'
        response['X-Audio-Channels'] = '1'
        response['X-Audio-Format'] = 'linear16'
        return response

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

    @action(
        detail=False,
        methods=["post"],
        url_path="generate-podcast-script",
        url_name="generate-podcast-script",
    )
    def generate_podcast_script(self, request):
        """
        Generate a podcast-style script from timeline posts using Grok.
        
        POST body (JSON):
        - keyword: The topic/keyword for the podcast
        - posts: List of post objects with author, username, text, likes, retweets
        
        Returns JSON with the podcast script.
        """
        from openai import OpenAI
        from django.conf import settings
        import json as json_module
        
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
        
        # Generate podcast script using Grok
        client = OpenAI(
            api_key=settings.XAI_TOKEN,
            base_url="https://api.x.ai/v1"
        )
        
        prompt = f"""You are a podcast host creating an engaging audio summary of the latest social media discussions about "{keyword}".

Based on these recent posts from experts and thought leaders:
{json_module.dumps(posts, indent=2)}

Create a natural, conversational podcast script that:
1. Opens with a brief, energetic introduction welcoming listeners to the show
2. Summarizes the key themes and discussions happening around "{keyword}"
3. Highlights 2-3 interesting perspectives or insights from specific users (mention them by name)
4. Includes natural transitions between topics
5. Ends with a brief wrap-up and sign-off

IMPORTANT GUIDELINES:
- Write in a conversational, podcast-friendly tone (as if speaking naturally)
- Keep it concise - aim for about 60-90 seconds of speaking time (roughly 150-200 words)
- Don't use hashtags, URLs, or @ symbols - just mention people by their display name
- Add natural pauses with commas and periods
- Don't include stage directions or sound effect notes
- Make it sound like a real person talking, not reading

Start directly with the script text, no meta-commentary."""

        try:
            response = client.chat.completions.create(
                model="grok-4-1-fast-non-reasoning",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            script = response.choices[0].message.content
            
            return Response({"script": script})
            
        except Exception as e:
            return Response(
                {"error": f"Failed to generate podcast script: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )