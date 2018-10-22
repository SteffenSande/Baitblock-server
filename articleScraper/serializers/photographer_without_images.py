from rest_framework import serializers

from articleScraper.models import Photographer


class PhotographerWithoutImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = '__all__'
