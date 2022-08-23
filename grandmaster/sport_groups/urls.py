from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SportGroupViewSet, SportsmenList, TrainersList


router = DefaultRouter()

router.register('', SportGroupViewSet, basename='sport_groups')


urlpatterns = [
    path('trainers/', TrainersList.as_view()),
    path('sportsmen/', SportsmenList.as_view()),
    path('', include(router.urls)),
]
