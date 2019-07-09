# Framework
from rest_framework import serializers

# Models
from articleScraper.models.diff import Diff


class DiffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diff
        exclude = ('article',)
