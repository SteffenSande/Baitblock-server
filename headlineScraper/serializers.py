from rest_framework import serializers

from articleScraper.serializers import ArticleInfoForHeadlineSerializer
from headlineScraper.models import HeadlineRevision
from submission.serializers import ReportSerializer
from submission.serializers.headline_summary import HeadlineSummarySerializer
from headlineScraper.models import HeadlineTemplate, Rank, Headline


class HeadlineDiffsSerializer(serializers.Serializer):
    title = serializers.CharField()
    sub_title = serializers.CharField()


class HeadlineRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadlineRevision
        exclude = ('timestamp', 'headline', 'id')


class HeadlineTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadlineTemplate
        exclude = ('created', 'modified', 'id')


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        exclude = ('headline', 'modified',)


class HeadlineSerializer(serializers.ModelSerializer):
    ranks = RankSerializer(many=True, read_only=True)
    revisions = HeadlineRevisionSerializer(many=True)
    summary = HeadlineSummarySerializer()
    reports = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    revision = HeadlineRevisionSerializer()
    diffs = HeadlineDiffsSerializer(many=True)

    class Meta:
        model = Headline
        exclude = ('created',)

    def get_info(self, obj):
        from articleScraper.models import Article
        try:
            info = Article.objects.get(headline=obj)
            return ArticleInfoForHeadlineSerializer(info).data
        except Article.DoesNotExist:
            return None

    def get_reports(self, obj):
        from submission.models import Report
        report = Report.objects.filter(headline=obj)
        return ReportSerializer(report, many=True).data


class HeadlineListSerializer(serializers.ModelSerializer):
    summary = HeadlineSummarySerializer()
    reports = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    revision = HeadlineRevisionSerializer()
    diffs = HeadlineDiffsSerializer(many=True)

    class Meta:
        model = Headline
        exclude = ('created',)

    def get_info(self, obj):
        from articleScraper.models import Article
        try:
            info = Article.objects.get(headline=obj)
            return ArticleInfoForHeadlineSerializer(info).data
        except Article.DoesNotExist:
            return None

    def get_reports(self, obj):
        from submission.models import Report
        report = Report.objects.filter(headline=obj)
        return ReportSerializer(report, many=True).data
