from rest_framework import serializers

from submission.models import HeadlineSummary


class HeadlineSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadlineSummary
        fields = ['one_line']