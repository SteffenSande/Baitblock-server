from rest_framework import serializers

from submission.models import UserReport


class UserReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserReport
        exclude = ('id', 'ip', 'report',)
