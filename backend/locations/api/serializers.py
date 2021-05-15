from rest_framework_gis.serializers import GeoFeatureModelSerializer
from locations.models import *

class LGASerializer(GeoFeatureModelSerializer):
    class Meta:
        model = LGA
        geo_field = "polygon"
        fields = "__all__"

class CitySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = City
        geo_field = "polygon"
        fields = "__all__"
