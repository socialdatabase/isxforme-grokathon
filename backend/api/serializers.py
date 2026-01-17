from rest_framework import serializers

from api.timeline import (
    fetch_grokathon_ids,
    fetch_accounts, 
    fetch_posts,
    fetch_grokathon_size, 
    fetch_ids_handle_topics, 
    fetch_topics_and_ranks_ids, 
    fetch_topics_ranks_handle,
    fetch_topics,
    infer_topic_in_query,
)
from api.groksignal import (
    extract_expert_categories,
    text_to_speech,
    speech_to_text,
)


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
    media = serializers.ListField(required=False, allow_null=True, allow_empty=True)


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
    categories = serializers.DictField(child=serializers.ListField(child=serializers.IntegerField()), read_only=True)

    def save(self, **kwargs):
        ids = self.validated_data.get('ids')
        categories = extract_expert_categories(ids)
        self.instance = {"categories": categories}
        return self.instance


class TextToSpeechSerializer(serializers.Serializer):
    # Double-check if Grok TTS has max_length
    text = serializers.CharField(write_only=True, max_length=20000)
    
    def save(self, **kwargs):
        text = self.validated_data.get('text')
        audio_content = text_to_speech(text)
        self.instance = {"audio": audio_content}
        return self.instance


class SpeechToTextSerializer(serializers.Serializer):
    audio = serializers.FileField(write_only=True)
    text = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        audio = self.validated_data.get('audio')
        text = speech_to_text(audio)
        self.instance = {"text": text}
        return self.instance
