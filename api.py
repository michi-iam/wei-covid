from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


from . models import *
from . serializers import *


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CityViewSet(viewsets.ModelViewSet):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer
    permission_classes = [ReadOnly] 

class RLPCovidDataViewSet(viewsets.ModelViewSet):
    queryset = RLPCovidDataModel.objects.all()
    serializer_class = RLPCovidDataSerializer
    permission_classes = [ReadOnly]




# class CountryViewSet(viewsets.ModelViewSet):
#     queryset = CountryModel.objects.all()
#     serializer_class = CountrySerializer
#     # permission_classes = []

# class WorldCovidDataViewSet(viewsets.ModelViewSet):
#     queryset = WorldCovidDataModel.objects.all()
#     serializer_class = WorldCovidDataSerializer
#     # permission_classes = []