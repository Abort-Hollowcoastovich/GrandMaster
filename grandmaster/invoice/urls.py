from django.urls import path

from .views import webhook_handler

urlpatterns = [
    path('yookassa/', webhook_handler),
]
