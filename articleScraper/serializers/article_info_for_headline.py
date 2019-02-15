from rest_framework import serializers

from articleScraper.models import Article
from .revision import RevisionSerializer


class ArticleInfoForHeadlineSerializer(serializers.ModelSerializer):
    revision = RevisionSerializer()
    published = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ('created', 'modified', 'headline', 'news_site',)

    def get_published(self, obj):
        if obj.category == Article.ARTICLE:
            revisions = obj.revisions
            return revisions[0].timestamp
        return None

    def get_updated(self, obj):
        if obj.category == Article.ARTICLE:
            revisions = obj.revisions
            if len(revisions) > 1:
                return revisions[len(revisions) - 1].timestamp
        return None
