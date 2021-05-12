from rest_framework import serializers
from tweets.models import Area

class areaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"

