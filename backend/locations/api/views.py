from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from djgeojson.views import GeoJSONLayerView

from locations.models import Region
from locations.api.serializers import RegionSerializer

class regionListCreateAPIView(APIView):
    def get(self,request):
        regions = Region.objects
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class regionDetailAPIView(APIView):
    def get_object(self,pk):
        region = get_object_or_404(Region,pk=pk)
        return region

    def get(self,request,pk):
        region = self.get_object(pk)
        serializer = RegionSerializer(region)
        return Response(serializer.data)
    
    def put(self,request,pk):
        region = self.get_object(pk)
        serializer = RegionSerializer(region,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        region = self.get_object(pk)
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegionGeoJSONAPIView(GeoJSONLayerView):
    precision = 4
    geometry_field = 'polygon'


import ujson
import logging
import time

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from backend.utils.couchDButil import couch_db
from backend.utils.common import *
logger = logging.getLogger('django.debug')

@require_http_methods(['POST', 'GET'])
def tweet_test_point(request, *args, **kwargs):
    obj = {"success": True}
    return json_response(obj)
