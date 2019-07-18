from rest_framework import serializers

from articleScraper.models import ArticleTemplate


class ArticleTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleTemplate
        fields = '__all__'
