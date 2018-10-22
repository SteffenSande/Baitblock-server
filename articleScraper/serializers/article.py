from rest_framework import serializers

from articleScraper.models import Article
from .revision import RevisionSerializer


class ArticleSerializer(serializers.ModelSerializer):
    revisions = RevisionSerializer(many=True)
    word_cloud = serializers.SerializerMethodField()
    diffs = serializers.ListField()

    class Meta:
        model = Article
        exclude = ('created', 'modified',)

    def get_word_cloud(self, obj):
        from django.conf import settings
        import os

        from articleScraper.models import Revision

        try:
            revision = obj.revision
        except Revision.DoesNotExist:
            return ""

        wordcloud_folder = os.path.join(settings.MEDIA_URL, settings.WORD_CLOUD_FOLDER.split(settings.MEDIA_URL)[1])
        return os.path.join(wordcloud_folder, os.path.join(obj.file_folder(), revision.filename('png')))
