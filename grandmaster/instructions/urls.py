from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InstructionViewSet

router = DefaultRouter()
router.register('', InstructionViewSet, basename='instructions')

urlpatterns = [
    path('', include(router.urls)),
]
