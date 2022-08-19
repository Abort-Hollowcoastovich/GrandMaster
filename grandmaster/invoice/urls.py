from django.urls import path

from .views import webhook_handler, PayAccountsList, CurrentBillsList, pay_bill

urlpatterns = [
    path('yookassa/', webhook_handler),
    path('pay_accounts/', PayAccountsList.as_view()),
    path('current_bills/', CurrentBillsList.as_view()),
    path('pay_bill/<int:bill_id>/', pay_bill)
]
