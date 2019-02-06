from rest_framework import generics
from rest_framework.response import Response

from api.views.mixins import MultipleFieldLookupMixin
from articleScraper.models import Article, ArticleUrlTemplate
from articleScraper.serializers import ArticleSerializer
from scraper.models import NewsSite
from helpers.utilities import find_headline_id


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        pk = int(self.kwargs.get('pk', "-1"))
        return Article.objects.articles_on_front_page(pk)


class ArticleDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    lookup_fields = ('pk', 'article_id')

    def get(self, request, pk, article_id):
        try:
            queryset = Article.objects.get(
                news_site__id=pk, headline_id=article_id)
        except Article.DoesNotExist:
            return Response(status=404)

        serializer = ArticleSerializer(queryset)
        return Response(serializer.data)


class ArticleSearch(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    serializer_class = ArticleSerializer

    def get(self, request, pk):
        url = self.request.query_params.get('url', None)

        if not url:
            return Response(status=404)

        try:
            site = NewsSite.objects.get(pk=pk)
        except NewsSite.DoesNotExist:
            return Response(status=404)

        url_templates = ArticleUrlTemplate.objects.filter(news_site=site)

        url_id = find_headline_id(url, url_templates)
        if not url_id:
            return Response(status=404)

        try:
            queryset = Article.objects.get(
                news_site__id=pk, headline__url_id=url_id)
        except Article.DoesNotExist:
            return Response(status=404)

        serializer = ArticleSerializer(queryset)
        return Response(serializer.data)
