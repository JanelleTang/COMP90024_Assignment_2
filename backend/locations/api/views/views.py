# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.generics import get_object_or_404
from djgeojson.views import GeoJSONLayerView
# from backend.utils.common import *
# from locations.models import *
# from locations.api.serializers import *

# class regionListCreateAPIView(APIView):
#     def get(self,request):
#         regions = LGA.objects
#         #serializer = RegionSerializer(regions, many=True)
#         #return Response(serializer.data)
#         return json_response(regions)

#     def post(self,request):
#         serializer = RegionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

# class regionDetailAPIView(APIView):
#     def get_object(self,pk):
#         region = get_object_or_404(Region,pk=pk)
#         return region

#     def get(self,request,pk):
#         region = self.get_object(pk)
#         serializer = RegionSerializer(region)
#         return Response(serializer.data)
    
#     def put(self,request,pk):
#         region = self.get_object(pk)
#         serializer = RegionSerializer(region,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk):
#         region = self.get_object(pk)
#         region.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class RegionGeoJSONAPIView(GeoJSONLayerView):
    precision = 4
    geometry_field = 'polygon'
