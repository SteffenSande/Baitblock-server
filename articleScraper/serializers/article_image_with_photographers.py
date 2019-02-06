from rest_framework import serializers

from articleScraper.models import ArticleImage
from .photographer_without_images import PhotographerWithoutImagesSerializer


class ArticleImageWithPhotographersSerializer(serializers.ModelSerializer):
    photographers = PhotographerWithoutImagesSerializer(many=True)

    class Meta:
        model = ArticleImage
        exclude = ('created', 'modified')
