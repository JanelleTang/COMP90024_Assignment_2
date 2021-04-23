from django.shortcuts import render
from rest_framework import viewsets

from .serializers import testSerializer
from .models import testDataPoint

# Create your views here.
class testViewSet(viewsets.ModelViewSet):
    queryset = testDataPoint.objects.all().order_by('unique_id')
    serializer_class = testSerializer
