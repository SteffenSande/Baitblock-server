# Framework
from rest_framework import serializers

# Models
from headlineScraper.models.diff import Diff
from headlineScraper.serializers.change import ChangeSerializer


class DiffSerializer(serializers.ModelSerializer):
    title_changes = ChangeSerializer(many=True)
    sub_title_changes = ChangeSerializer(many=True)

    class Meta:
        model = Diff
        exclude = ('headline',)
        ordering = ('id',)
