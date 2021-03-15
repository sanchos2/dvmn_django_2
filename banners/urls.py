from django.urls import path

from banners.views import get_banner_url, get_banners

urlpatterns = [
    path('', get_banners),
    path('<slug:slug>/', get_banner_url),
]
