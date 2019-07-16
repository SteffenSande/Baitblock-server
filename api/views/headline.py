from rest_framework import generics
from rest_framework.response import Response

from api.views.mixins import MultipleFieldLookupMixin
from headlineScraper.models import Headline
from headlineScraper.serializers.headline import HeadlineSerializer, HeadlineListSerializer


class HeadlineList(generics.ListCreateAPIView):
    queryset = Headline.objects.all()
    serializer_class = HeadlineSerializer

    def list(self, request, pk):
        serializer = HeadlineListSerializer(
            Headline.objects.headlines_on_front_page(pk), many=True)
        return Response(serializer.data)


class HeadlineDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    serializer_class = HeadlineSerializer
    lookup_fields = ('pk', 'headline_id')

    def get(self, request, pk, headline_id):
        try:
            queryset = Headline.objects.get(news_site__id=pk, id=headline_id)
        except Headline.DoesNotExist:
            return Response(status=404)

        serializer = HeadlineSerializer(queryset)
        return Response(serializer.data)
