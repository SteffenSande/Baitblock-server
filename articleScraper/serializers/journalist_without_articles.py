from rest_framework import serializers

from articleScraper.models import Journalist


class JournalistWithoutArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Journalist
        fields = '__all__'
