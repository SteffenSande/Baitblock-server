from rest_framework import serializers

from articleScraper.models import Revision
from articleScraper.serializers.content import ContentSerializer
from .article_image_with_photographers import ArticleImageWithPhotographersSerializer
from .journalist_without_articles import JournalistWithoutArticlesSerializer


class RevisionSerializer(serializers.ModelSerializer):
    images = ArticleImageWithPhotographersSerializer(many=True)
    journalists = JournalistWithoutArticlesSerializer(many=True)
    contents = ContentSerializer(many=True)

    class Meta:
        model = Revision
        exclude = ('article',)

