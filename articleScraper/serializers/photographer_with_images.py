from rest_framework import serializers

from articleScraper.models import Photographer
from .article_image_without_photographers import ArticleImageWithoutPhotographersSerializer


class PhotographerWithImagesSerializer(serializers.ModelSerializer):
    images = ArticleImageWithoutPhotographersSerializer(many=True)

    class Meta:
        model = Photographer
        fields = '__all__'
