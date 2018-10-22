from rest_framework import generics
from rest_framework.response import Response

from articleScraper.models import Photographer
from articleScraper.serializers import PhotographerSerializer


class PhotographerList(generics.ListCreateAPIView):
    def list(self, request):
        serializer = PhotographerSerializer(Photographer.objects.all(), many=True)
        return Response(serializer.data)


class PhotographerDetail(generics.RetrieveAPIView):
    serializer_class = PhotographerSerializer

    def get(self, request, pk):
        try:
            queryset = Photographer.objects.get(id=pk)
        except Photographer.DoesNotExist:
            return Response(status=404)

        serializer = PhotographerSerializer(queryset)
        return Response(serializer.data)
