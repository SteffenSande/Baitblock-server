from rest_framework import serializers

from articleScraper.models import ArticleUrlTemplate


class ArticleUrlTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleUrlTemplate
        exclude = ('created', 'modified',)