from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from . import views



urlpatterns = [
    path("", views.index, name="covidstartseite"),
    path("covid_get_plots", views.get_data_by_landkreis, name="covid_get_plots"),
]

urlpatterns += [
    path("impressum", views.impressum, name="impressum"),
    path("datenschutz", views.datenschutz, name="datenschutz"),
    path("cookie_settings", views.cookie_settings, name="cookie_settings"),
]