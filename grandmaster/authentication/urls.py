from django.urls import path, include
from .views import *

urlpatterns = [
    path('send_code/', ValidatePhoneSendOTP.as_view()),
    path('validate_code/', ValidateOTP.as_view())
]