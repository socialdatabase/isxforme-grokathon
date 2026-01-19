"""
Utilities for handling async-to-sync streaming in Django views.

This module provides reusable utilities for converting async generators to sync generators
suitable for Django's StreamingHttpResponse, avoiding code duplication across streaming endpoints.
"""

import asyncio
from django.http import StreamingHttpResponse


def async_to_sync_stream_generator(async_gen_func, *args, **kwargs):
    """
    Convert an async generator function to a sync generator for StreamingHttpResponse.

    This function bridges the gap between Django's sync world and async generators
    by creating a new event loop and converting async chunks to sync chunks.

    Args:
        async_gen_func: An async generator function to be called
        *args: Positional arguments to pass to the async generator function
        **kwargs: Keyword arguments to pass to the async generator function

    Yields:
        bytes: UTF-8 encoded chunks from the async generator

    Example:
        >>> async def my_async_gen(query):
        >>>     async for chunk in some_async_source(query):
        >>>         yield chunk
        >>>
        >>> generator = async_to_sync_stream_generator(my_async_gen, "AI research")
        >>> response = StreamingHttpResponse(generator)
    """
    async def run_stream():
        """Wrapper to call the async generator function with its arguments"""
        async for chunk in async_gen_func(*args, **kwargs):
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


def create_streaming_response(generator, content_type='text/plain; charset=utf-8', **extra_headers):
    """
    Create a StreamingHttpResponse with standard streaming headers.

    This function wraps StreamingHttpResponse creation with consistent headers
    that prevent caching and buffering for real-time streaming.

    Args:
        generator: A generator that yields bytes for streaming
        content_type: The content type for the response (default: 'text/plain; charset=utf-8')
        **extra_headers: Additional headers to set on the response (e.g., X-Audio-Sample-Rate='24000')

    Returns:
        StreamingHttpResponse: Configured response ready to stream to the client

    Example:
        >>> def my_generator():
        >>>     for i in range(10):
        >>>         yield f"chunk {i}\n".encode('utf-8')
        >>>
        >>> return create_streaming_response(my_generator())

        >>> # With custom headers:
        >>> return create_streaming_response(
        >>>     audio_generator(),
        >>>     content_type='audio/pcm',
        >>>     **{'X-Audio-Sample-Rate': '24000', 'X-Audio-Channels': '1'}
        >>> )
    """
    response = StreamingHttpResponse(generator, content_type=content_type)

    # Standard headers to prevent caching and buffering
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx

    # Add any extra headers provided
    for header_name, header_value in extra_headers.items():
        response[header_name] = header_value

    return response
