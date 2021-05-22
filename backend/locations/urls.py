from django.urls import path
from .views import *

urlpatterns = [
    path("update",update_model_instances)
]
