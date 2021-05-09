from django.urls import include, path
from rest_framework import routers
from . import views
from API.view.tweet import *

router = routers.DefaultRouter()
router.register(r'testDataPoint', views.testViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('tweet/',tweet_test_point)
]