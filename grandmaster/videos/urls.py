from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import VideoViewSet, video_image

router = DefaultRouter()
router.register('', VideoViewSet, basename='videos')

urlpatterns = [
    path('image/', video_image),
    path('', include(router.urls)),
]
