from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from tweets.models import Area
from tweets.api.serializers import areaSerializer

"""@api_view(["GET","POST"])
def area_list_create_api_view(request):
    if request.method =="GET":
        areas = Area.objects
        serializer = areaSerializer(areas, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = areaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT","DELETE"])
def article_detail_api_view(request,pk):
    try:
        area = Area.objects.get(pk = pk)
    except Area.DoesNotExist:
        return Response({"error": {
                            "code": 404,
                            "message": "Article not found!"
                            }
        }, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = areaSerializer(area)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = areaSerializer(area,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        area.delete()
        return Response(status=status.HTTP_204_NO_CNTENT)"""

class areaListCreateAPIView(APIView):
    def get(self,request):
        areas = Area.objects
        serializer = areaSerializer(areas, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = areaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class areaDetailAPIView(APIView):
    def get_object(self,pk):
        area = get_object_or_404(Area,pk=pk)
        return area

    def get(self,request,pk):
        area = self.get_object(pk)
        serializer = areaSerializer(area)
        return Response(serializer.data)
    
    def put(self,request,pk):
        area = self.get_object(pk)
        serializer = areaSerializer(area,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Reponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        area = self.get_object(pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)