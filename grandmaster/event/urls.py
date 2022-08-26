from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventMembersView, EventViewSet, make_report

router = DefaultRouter()

router.register(r'', EventViewSet, basename='events')


urlpatterns = [
    path('members/', EventMembersView.as_view()),
    path('reports/', make_report),
    path('', include(router.urls)),
]
