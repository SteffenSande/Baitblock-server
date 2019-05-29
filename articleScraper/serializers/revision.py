from rest_framework import serializers

from articleScraper.models import Revision
from articleScraper.serializers.content import ContentSerializer
from .article_image_with_photographers import ArticleImageWithPhotographersSerializer
from .journalist_without_articles import JournalistWithoutArticlesSerializer


class RevisionSerializer(serializers.ModelSerializer):
    """
    This is the serializer for the revisons, if it is needed to present this information in the article response from the server
    """

    images = ArticleImageWithPhotographersSerializer(many=True)
    journalists = JournalistWithoutArticlesSerializer(many=True)
    # Uncomment to send content nodes as a part of the response from the server.
    # contents = ContentSerializer(many=True)

    class Meta:
        model = Revision
        exclude = ('article',)

