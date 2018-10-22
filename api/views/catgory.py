from rest_framework import generics

from submission.models import ReportCategory
from submission.serializers import ReportCategorySerializer


class CategoryList(generics.ListCreateAPIView):
    serializer_class = ReportCategorySerializer
    queryset = ReportCategory.objects.all()
