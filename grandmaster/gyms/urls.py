from django.urls import path

from .views import GymListView

urlpatterns = [
    path('', GymListView.as_view()),
]
