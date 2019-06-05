from rest_framework import serializers
from articleScraper.models import Article
from articleScraper.serializers.diff import DiffSerializer
from articleScraper.serializers.revision import RevisionSerializer


class ArticleSerializer(serializers.ModelSerializer):
    revisions = RevisionSerializer(many=True)
    # diffs = DiffSerializer(many=True)
    diffs = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = (
            'created',
            'modified',
        )

    def get_diffs(self, obj):
        diffs = map(lambda item: item.diff, list(obj.diff_set.all()))
        return diffs
