from django.urls import path, include
from .views import EventMembersView, EventViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', EventViewSet, basename='events')


urlpatterns = [
    path('members/', EventMembersView.as_view()),
    path('', include(router.urls)),
]
