from django.urls import path
from locations.models import *
from django.conf.urls import url
from locations.api.views.views import *
from locations.api.views.tweet_views import *
from locations.api.views.region_views import *

urlpatterns = [
    url(r'^lga_data.geojson$', RegionGeoJSONAPIView.as_view(model=LGA,properties=['name',
                                                                                'display_name',
                                                                                'total_sentiment',
                                                                                'sentiment_rank',
                                                                                'sentiment_value',
                                                                                'state',
                                                                                'city',
                                                                                'n_tweets']), name='data'),
    url(r'^city_data.geojson$', RegionGeoJSONAPIView.as_view(model=City,properties=['name',
                                                                            'total_sentiment',
                                                                            'display_name',
                                                                            'sentiment_rank',
                                                                            'sentiment_value',
                                                                            'state',
                                                                            'n_tweets']), name='data'),
                                                                                
    path('tweet/raw/<int:size>', get_raw_tweet_by_size),
    path('tweet/raw/update/<str:pk>', update_raw_tweet),
    path('tweet/raw/delete/<str:pk>', delete_raw_tweet_by_id),
    path('tweet/raw/create', create_raw_tweet),
    path('tweet/hashtags', tweetHashtags),
    path('location/dates',get_all_dates),
    path('location/dates/<str:pk>',get_city_dates),
    path('location/times',get_all_times),
    path('location/times/<str:pk>',get_city_times),
    path('location/create', create_region),
    path('location/city', get_cities), 
    path('location/lga', get_lgas), 
    path('location/city/<str:pk>', get_city_detail), 
    path('location/city/delete/<str:pk>', delete_city_detail)                                                           
]

