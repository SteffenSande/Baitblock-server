from rest_framework import serializers

from submission.models import ReportCategory


class ReportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCategory
        fields = '__all__'
