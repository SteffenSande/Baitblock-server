# Framework
from rest_framework import serializers

# Models
from articleScraper.models.child import Child


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
