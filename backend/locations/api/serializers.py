from rest_framework_gis.serializers import GeoFeatureModelSerializer
from locations.models import Region

class RegionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Region
        geo_field = "polygon"
        fields = "__all__"
