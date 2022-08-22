from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', ScheduleViewSet, basename='visit_log')


urlpatterns = [
    path('', include(router.urls)),
]
