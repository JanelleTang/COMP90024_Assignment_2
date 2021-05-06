from django.urls import path
from locations.api.views import regionListCreateAPIView

from locations.models import Region
from django.conf.urls import url
from locations.api.views import *
urlpatterns = [
    path("regions/",
        regionListCreateAPIView.as_view(),
        name = "region-list"),
        path("regions/<int:pk>/",
        regionDetailAPIView.as_view(),
        name = "region-detail"),
    url(r'^data.geojson$', RegionGeoJSONAPIView.as_view(model=Region,properties=['name',
                                                                                'sentiment_value',
                                                                                'sentiment_rank',
                                                                                'state',
                                                                                'n_tweets',
                                                                                'city']), name='data'),
    path('tweet/',tweet_test_point)                                                                     
]

