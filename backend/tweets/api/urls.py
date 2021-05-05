from django.urls import path
from tweets.api.views import areaListCreateAPIView, areaDetailAPIView
# from tweets.api.views import article_detail_api_view, area_list_create_api_view

urlpatterns = [
    path("areas/",
        areaListCreateAPIView.as_view(),
        name = "area-list"),
    path("areas/<int:pk>/",
        areaDetailAPIView.as_view(),
        name = "area-detail")
    # path("areas/",area_list_create_api_view,name = "area-list"),
    # path("areas/<int:pk>/",article_detail_api_view,name = "area-detail")
]