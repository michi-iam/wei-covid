from django.contrib import admin
from . models import RLPCovidDataModel, CityModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# csv import / export in admin-interface
class RLPCovidDataModelResource(resources.ModelResource):
    class Meta:
        model = RLPCovidDataModel

class CityModelResource(resources.ModelResource):
    class Meta:
        model = CityModel

class RLPCovidDataModelAdmin(ImportExportModelAdmin):
    resource_class = RLPCovidDataModelResource
    list_display = ('landkreis', 'date')
    list_filter = ('landkreis', 'date')
    search_fields = ['landkreis']

class CityModelAdmin(ImportExportModelAdmin):
    resource_class = CityModelResource
    list_display = ('name', 'population')
    list_filter = ('name',)
    search_fields = ['name']
    
admin.site.register(RLPCovidDataModel, RLPCovidDataModelAdmin)
admin.site.register(CityModel, CityModelAdmin)



