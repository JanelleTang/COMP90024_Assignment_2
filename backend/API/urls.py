from django.urls import include, path
from rest_framework import routers
from . import views
from API.view.tweet import *

router = routers.DefaultRouter()
router.register(r'testDataPoint', views.testViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/tweet/raw/<int:size>', get_raw_tweet_by_size),
    path('api/tweet/raw/update/<str:id>', update_raw_tweet),
    path('api/tweet/raw/delete/<str:id>', delete_raw_tweet_by_id),
    path('api/tweet/raw/create', create_raw_tweet),
]