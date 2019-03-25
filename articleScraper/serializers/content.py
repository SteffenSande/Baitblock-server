# Framework
from rest_framework import serializers

# Models
from articleScraper.models import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        exclude = ('article',)
