
# ============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== 

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
