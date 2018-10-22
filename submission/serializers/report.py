from rest_framework import serializers

from submission.models import Report
from submission.serializers.user_report import UserReportSerializer
from .report_category import ReportCategorySerializer


class ReportSerializer(serializers.ModelSerializer):
    category = ReportCategorySerializer()
    reports = UserReportSerializer(many=True)

    class Meta:
        model = Report
        exclude = ('id', 'headline',)
