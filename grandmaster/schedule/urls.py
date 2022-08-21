from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', ScheduleViewSet, basename='schedule')


urlpatterns = [
    path('', include(router.urls)),
    path('find_schedules/', SpecificScheduleView.as_view())
]
