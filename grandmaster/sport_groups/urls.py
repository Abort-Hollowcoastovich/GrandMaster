from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', SportGroupViewSet, basename='sport_groups')


urlpatterns = [
    path('', include(router.urls)),
]
