from rest_framework import generics

from newsSite.models import NewsSite
from newsSite.serielizer import NewsSiteSerializer


class SiteList(generics.ListCreateAPIView):
    serializer_class = NewsSiteSerializer
    queryset = NewsSite.objects.active_news_sites()


class SiteDetail(generics.RetrieveAPIView):
    serializer_class = NewsSiteSerializer
    queryset = NewsSite.objects.all()
