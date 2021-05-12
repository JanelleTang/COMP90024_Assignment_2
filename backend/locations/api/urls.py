from django.urls import path
from locations.models import Region
from django.conf.urls import url
from locations.api.views.views import *
from locations.api.views.tweet_views import *
from locations.api.views.region_views import *


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
    # path('tweet/raw/',raw_tweets_api_view),
    path('tweet/raw/<int:size>', get_raw_tweet_by_size),
    path('tweet/raw/update/<str:pk>', update_raw_tweet),
    path('tweet/raw/delete/<str:pk>', delete_raw_tweet_by_id),
    path('tweet/raw/create', create_raw_tweet),
    path('location/create', create_region),
    path('location', get_region), 
    path('location/lga/<str:pk>', get_region_detail), 
    path('location/lga/delete/<str:pk>', get_region_detail),                                                                        
]

