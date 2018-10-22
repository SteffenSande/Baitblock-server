from rest_framework import generics
from rest_framework.response import Response


from api.views.mixins import MultipleFieldLookupMixin
from articleScraper.models import Journalist
from articleScraper.serializers import JournalistSerializer


class JournalistList(generics.ListCreateAPIView):
    def list(self, request, pk):
        serializer = JournalistSerializer(Journalist.objects.filter(news_site=pk), many=True)
        return Response(serializer.data)


class JournalistDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    serializer_class = JournalistSerializer
    lookup_fields = ('pk', 'journalist_id')

    def get(self, request, pk, journalist_id):
        try:
            queryset = Journalist.objects.get(news_site__id=pk, id=journalist_id)
        except Journalist.DoesNotExist:
            return Response(status=404)

        serializer = JournalistSerializer(queryset)
        return Response(serializer.data)
