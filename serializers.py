from rest_framework import serializers
from django.db.models import fields


from .models import *


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CityModel
        fields = '__all__'

class RLPCovidDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RLPCovidDataModel
        fields = '__all__'


# class CountrySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CountryModel
#         fields = '__all__'
# class WorldCovidDataSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = WorldCovidDataModel
#         fields = '__all__'