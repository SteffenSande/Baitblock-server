from rest_framework import serializers

from articleScraper.models import ArticleImage


class ArticleImageWithoutPhotographersSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleImage
        exclude = ('created', 'modified')