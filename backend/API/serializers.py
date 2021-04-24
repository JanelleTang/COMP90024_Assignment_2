from rest_framework import serializers
from .models import testDataPoint

class testSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = testDataPoint
        fields = ('unique_id','attr1','attr2','last_updated')