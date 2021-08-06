from rest_framework import serializers

from news.models import NewsPost
from taxonomy.models import Topic, DiveSite


class DiveSiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiveSite
        fields = [
            'pk',
            'display_name',
            'url_name',
            'full_url',
        ]


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'pk',
            'display_name',
            'internal_name'
        ]


class NewsPostSerializer(serializers.HyperlinkedModelSerializer):
    divesite = DiveSiteSerializer(many=False)
    topics = TopicSerializer(many=True)

    class Meta:
        model = NewsPost
        fields = [
            'pk',
            'title',
            'teaser',
            'publish_date',
            'source',
            'divesite',
            'topics',
        ]
