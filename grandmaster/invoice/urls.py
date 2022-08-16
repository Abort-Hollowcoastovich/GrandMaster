from django.urls import path

from .views import webhook_handler, PayAccountsList

urlpatterns = [
    path('yookassa/', webhook_handler),
    path('pay_accounts/', PayAccountsList.as_view())
]
