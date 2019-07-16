from rest_framework import serializers
from articleScraper.models import Article
from articleScraper.serializers.revision import RevisionSerializer


class ArticleSerializer(serializers.ModelSerializer):
    revisions = RevisionSerializer(many=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = (
            'created',
            'modified',
        )

    def get_url(self,obj):
        url = obj.headline.url
        return url
