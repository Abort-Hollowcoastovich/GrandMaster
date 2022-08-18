from django.urls import path, include
from .views import SportGroupViewSet, SportsmenList
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('', SportGroupViewSet, basename='sport_groups')


urlpatterns = [
    path('sportsmen/', SportsmenList.as_view()),
    path('', include(router.urls)),
]
