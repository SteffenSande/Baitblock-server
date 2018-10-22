from rest_framework import serializers

from submission.models import Limit


class LimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limit
        fields = '__all__'
