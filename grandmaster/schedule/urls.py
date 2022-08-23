from django.urls import path, include
# from rest_framework.routers import DefaultRouter

from .views import ScheduleView

# router = DefaultRouter()
#
# router.register(r'', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', ScheduleView.as_view()),
]
