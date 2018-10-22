from rest_framework import generics
from rest_framework.response import Response

from articleScraper.serializers import ArticleImageSerializer
from articleScraper.models import ArticleImage


class ArticleImageList(generics.ListCreateAPIView):
    def list(self, request):
        serializer = ArticleImageSerializer(ArticleImage.objects.all(), many=True)
        return Response(serializer.data)


class ArticleImageDetail(generics.RetrieveAPIView):
    serializer_class = ArticleImageSerializer

    def get(self, request, pk):
        try:
            queryset = ArticleImage.objects.get(id=pk)
        except ArticleImage.DoesNotExist:
            return Response(status=404)

        serializer = ArticleImageSerializer(queryset)
        return Response(serializer.data)
