# Framework
from rest_framework import serializers

# Models
from articleScraper.models.diff import Diff
from articleScraper.serializers.change import ChangeSerializer


class DiffSerializer(serializers.ModelSerializer):
    changes = ChangeSerializer(many=True)

    class Meta:
        model = Diff
        exclude = ('revision',)
