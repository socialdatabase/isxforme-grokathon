from rest_framework import serializers

from api.timeline import (
    fetch_grokathon_ids,
    fetch_accounts, 
    fetch_posts,
    fetch_posts_timeline,
    fetch_grokathon_size, 
    fetch_ids_handle_topics, 
    fetch_topics_and_ranks_ids, 
    fetch_topics_ranks_handle,
    get_accounts_with_ranks,
    fetch_topics,
    infer_topic_in_query,
)
from api.groksignal import (
    extract_expert_categories,
    get_xai_handles_summary,
)
from api.voicethomas import (
    text_to_speech as xai_text_to_speech,
    speech_to_text as xai_speech_to_text,
    get_available_voices,
    AVAILABLE_VOICES,
)
from api.image import (
    fetch_video_from_image,
)

class XaiImageToVideoSerializer(serializers.Serializer):
    image_url = serializers.URLField(write_only=True)
    video_url = serializers.URLField(read_only=True)

    def save(self, **kwargs):
        image_url = self.validated_data.get('image_url')
        video_url = fetch_video_from_image(image_url)
        self.instance = {"video_url": video_url}
        return self.instance


class PublicMetricsSerializer(serializers.Serializer):
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    tweet_count = serializers.IntegerField()
    listed_count = serializers.IntegerField()
    like_count = serializers.IntegerField()
    media_count = serializers.IntegerField()


class AccountSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    url = serializers.URLField(allow_blank=True, allow_null=True)
    profile_image_url = serializers.URLField(allow_blank=True, allow_null=True)
    verified = serializers.BooleanField()
    protected = serializers.BooleanField()
    location = serializers.CharField(allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField()
    pinned_tweet_id = serializers.CharField(allow_blank=True, allow_null=True)
    public_metrics = PublicMetricsSerializer()
    entities = serializers.DictField(required=False, allow_null=True)


class AccountWithRanksSerializer(AccountSerializer):
    ranks = serializers.ListField(child=serializers.CharField(), read_only=True)


class FetchIdsSerializer(serializers.Serializer):
    input_query = serializers.CharField(write_only=True)
    ids = serializers.ListField(child=serializers.CharField(), read_only=True)

    def save(self, **kwargs):
        input_query = self.validated_data.get('input_query')
        ids = fetch_grokathon_ids(input_query)
        self.instance = {"ids": ids}
        return self.instance


class FetchAccountsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    accounts = AccountSerializer(many=True, read_only=True)

    def save(self, **kwargs):
        ids = self.validated_data.get('ids')
        accounts = fetch_accounts(ids)
        self.instance = {"accounts": accounts}
        return self.instance


class PostUrlSerializer(serializers.Serializer):
    start = serializers.IntegerField()
    end = serializers.IntegerField()
    url = serializers.URLField()
    expanded_url = serializers.URLField(allow_blank=True, allow_null=True)
    display_url = serializers.CharField(allow_blank=True, allow_null=True)


class MediaSerializer(serializers.Serializer):
    url = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    type = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    width = serializers.IntegerField(allow_null=True, required=False)
    height = serializers.IntegerField(allow_null=True, required=False)
    preview_image_url = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    start = serializers.IntegerField(allow_null=True, required=False)
    end = serializers.IntegerField(allow_null=True, required=False)


class PostDataSerializer(serializers.Serializer):
    id = serializers.CharField()
    text = serializers.CharField()
    created_at = serializers.DateTimeField()
    account_id = serializers.CharField()
    post_type = serializers.CharField(allow_blank=True, allow_null=True)
    retweet_count = serializers.IntegerField(required=False, allow_null=True)
    reply_count = serializers.IntegerField(required=False, allow_null=True)
    like_count = serializers.IntegerField(required=False, allow_null=True)
    quote_count = serializers.IntegerField(required=False, allow_null=True)
    bookmark_count = serializers.IntegerField(required=False, allow_null=True)
    impression_count = serializers.IntegerField(required=False, allow_null=True)
    urls = PostUrlSerializer(many=True, required=False, allow_null=True)
    media = MediaSerializer(many=True, required=False, allow_null=True, allow_empty=True)


class PostAccountSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    verified = serializers.BooleanField(required=False, allow_null=True)
    profile_image_url = serializers.URLField(allow_blank=True, allow_null=True, required=False)


class PostSerializer(serializers.Serializer):
    post = PostDataSerializer()
    account = PostAccountSerializer()


class FetchPostsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    posts = PostSerializer(many=True, read_only=True)

    def save(self, **kwargs):
        ids = self.validated_data.get('ids')
        posts = fetch_posts(ids)
        self.instance = {"posts": posts}
        return self.instance


class FetchPostsTimelineSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    posts = PostSerializer(many=True, read_only=True)

    def save(self, **kwargs):
        ids = self.validated_data.get('ids')
        posts = fetch_posts_timeline(ids)
        self.instance = {"posts": posts}
        return self.instance
        

class FetchGrokathonSizeSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    size = serializers.CharField(read_only=True)  # External API returns formatted string like '27.9M'

    def save(self, **kwargs):
        ids = self.validated_data.get('ids')
        size = fetch_grokathon_size(ids)
        self.instance = {"size": size}
        return self.instance


class FetchTopicsSerializer(serializers.Serializer):
    topics = serializers.ListField(child=serializers.CharField(), read_only=True)

    def save(self, **kwargs):
        topics, _ = fetch_topics()
        self.instance = {"topics": topics}
        return self.instance


class InferTopicInQuerySerializer(serializers.Serializer):
    input_query = serializers.CharField(write_only=True)
    topic = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        input_query = self.validated_data.get('input_query')
        topic = infer_topic_in_query(input_query)
        self.instance = {"topic": topic}
        return self.instance


class FetchIdsHandleTopicsSerializer(serializers.Serializer):
    handle = serializers.CharField(write_only=True)
    topics = serializers.ListField(child=serializers.CharField(), write_only=True)
    ids = serializers.ListField(child=serializers.CharField(), read_only=True)

    def save(self, **kwargs):
        # To get ids outside of the community of the handle
        handle = self.validated_data.get('handle')
        topics = self.validated_data.get('topics')
        ids = fetch_ids_handle_topics(handle, topics)
        self.instance = {"ids": ids}
        return self.instance


class FetchTopicsAndRanksIdsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    topics = serializers.ListField(child=serializers.CharField(), read_only=True)
    ranks = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField()),
        read_only=True
    )

    def save(self, **kwargs):
        # To fetch the top topics (of ids) and the ranks of the ids
        ids = self.validated_data.get('ids')
        topics, ranks = fetch_topics_and_ranks_ids(ids)
        self.instance = {"topics": topics, "ranks": ranks}
        return self.instance


class GetAccountsWithRanksSerializer(serializers.Serializer):
    input_query = serializers.CharField(write_only=True)
    accounts = AccountWithRanksSerializer(many=True, read_only=True)

    def save(self, **kwargs):
        input_query = self.validated_data.get('input_query')
        accounts = get_accounts_with_ranks(input_query)
        self.instance = {"accounts": accounts}
        return self.instance


class FetchTopicsRanksHandleSerializer(serializers.Serializer):
    handle = serializers.CharField(write_only=True)
    topics = serializers.ListField(child=serializers.CharField(), read_only=True)
    ranks = serializers.ListField(child=serializers.CharField(), read_only=True)

    def save(self, **kwargs):
        # Fetch the ranks of the handle and the top topics the handle is interested in
        handle = self.validated_data.get('handle')
        topics, ranks = fetch_topics_ranks_handle(handle)
        self.instance = {"topics": topics, "ranks": ranks}
        return self.instance


class FetchExpertCategoriesSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    categories = serializers.DictField(child=serializers.ListField(child=serializers.CharField()), read_only=True)

    def save(self, **kwargs):
        ids = self.validated_data.get('ids')
        categories = extract_expert_categories(ids)
        self.instance = {"categories": categories}
        return self.instance


class XaiTextToSpeechSerializer(serializers.Serializer):
    """
    Serializer for xAI text-to-speech conversion.
    Uses xAI's realtime WebSocket API with Grok voices.
    Available voices: ara, rex, sal, eve, una, leo
    """
    text = serializers.CharField(write_only=True, max_length=20000)
    voice = serializers.ChoiceField(
        choices=[(v, v.title()) for v in AVAILABLE_VOICES],
        default="ara",
        write_only=True,
        required=False
    )
    
    def save(self, **kwargs):
        text = self.validated_data.get('text')
        voice = self.validated_data.get('voice', 'ara')
        audio_content = xai_text_to_speech(text, voice_id=voice, output_format="wav")
        self.instance = {"audio": audio_content}
        return self.instance


class XaiSpeechToTextSerializer(serializers.Serializer):
    """
    Serializer for xAI speech-to-text conversion.
    Uses xAI's realtime WebSocket API for transcription.
    """
    audio = serializers.FileField(write_only=True)
    text = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        audio = self.validated_data.get('audio')
        text = xai_speech_to_text(audio)
        self.instance = {"text": text}
        return self.instance


class XaiVoicesSerializer(serializers.Serializer):
    """Serializer for listing available xAI voices."""
    voices = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )
    
    def save(self, **kwargs):
        self.instance = {"voices": get_available_voices()}
        return self.instance


class XaiHandlesSummarySerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    input_query = serializers.CharField(write_only=True)
    summary = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        ids = self.validated_data.get('ids')
        input_query = self.validated_data.get('input_query')
        summary = get_xai_handles_summary(ids, input_query)
        self.instance = {"summary": summary}
        return self.instance
