from rest_framework import serializers

from articleScraper.models import Article
from articleScraper.models import Journalist


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('created', 'modified', 'news_site')


class JournalistWithArticlesSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)

    class Meta:
        model = Journalist
        fields = '__all__'
