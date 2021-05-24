from django.urls import path
from .views import *

urlpatterns = [
    path("update/city",update_city_instances),
    path("update/lga",update_lga_instances)
]
