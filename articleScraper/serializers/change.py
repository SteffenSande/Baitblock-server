# Framework
from rest_framework import serializers

# Models
from articleScraper.models.change import Change


class ChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change
        exclude = ('diff',)
