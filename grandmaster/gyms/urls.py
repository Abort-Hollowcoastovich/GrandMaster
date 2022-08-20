from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GymViewSet

router = DefaultRouter()
router.register('', GymViewSet, basename='gyms')

urlpatterns = [
    path('', include(router.urls)),
]
