from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', VisitLogViewSet, basename='visit_log')


urlpatterns = [
    path('', include(router.urls)),
]