from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', Hello.as_view()),
]