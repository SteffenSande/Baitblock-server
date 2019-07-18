from rest_framework import serializers
from headlineScraper.models import HeadlineRevision
from headlineScraper.serializers.diff import DiffSerializer
from headlineScraper.models import HeadlineTemplate, Rank, Headline


class HeadlineRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadlineRevision
        exclude = ('headline',)


class HeadlineTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadlineTemplate
        fields = '__all__'


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        exclude = ('headline',)


class HeadlineSerializer(serializers.ModelSerializer):
    ranks = RankSerializer(many=True, read_only=True)
    revisions = HeadlineRevisionSerializer(many=True)
    diffs = DiffSerializer(many=True)

    class Meta:
        model = Headline
        fields = '__all__'


class HeadlineListSerializer(serializers.ModelSerializer):
    revisions = HeadlineRevisionSerializer(many=True)
    diffs = DiffSerializer(many=True)

    class Meta:
        model = Headline
        fields = '__all__'


