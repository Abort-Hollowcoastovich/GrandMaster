from django.urls import path, include
from .views import ScheduleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', ScheduleViewSet, basename='schedule')


urlpatterns = [
    path('', include(router.urls)),
]
