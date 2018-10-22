from rest_framework import generics

from submission.models import Limit
from submission.serializers import LimitSerializer


class LimitList(generics.ListCreateAPIView):
    serializer_class = LimitSerializer
    queryset = Limit.objects.all()
