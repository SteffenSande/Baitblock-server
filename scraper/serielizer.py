from rest_framework import serializers

from articleScraper.serializers.articleTemplate import ArticleTemplateSerializer
from headlineScraper.serializers import HeadlineTemplateSerializer
from scraper.models import NewsSite


class NewsSiteSerializer(serializers.ModelSerializer):
    headlineTemplate = HeadlineTemplateSerializer()
    articleTemplate = ArticleTemplateSerializer()
    urlTemplates = serializers.SerializerMethodField()
    word_cloud = serializers.SerializerMethodField()

    class Meta:
        model = NewsSite
        exclude = ('created', 'modified', 'is_active',)

    def get_urlTemplates(self, ob):
        from articleScraper.models import ArticleUrlTemplate
        from articleScraper.serializers import ArticleUrlTemplateSerializer

        url_templates = ArticleUrlTemplate.objects.filter(news_site=ob)
        return ArticleUrlTemplateSerializer(url_templates, many=True).data

    def get_word_cloud(self, ob):

        from django.conf import settings

        import os
        path_to_folder = os.path.join(settings.WORD_CLOUD_FOLDER, ob.file_folder())
        relative_path_to_folder = os.path.join(settings.MEDIA_URL, path_to_folder.split(settings.MEDIA_ROOT)[-1][1:])

        return os.path.join(relative_path_to_folder, 'frontpage.png')
