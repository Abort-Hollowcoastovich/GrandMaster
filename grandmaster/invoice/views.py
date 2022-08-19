import json
from yookassa.domain.notification import WebhookNotification

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import PayAccount, UserBill
from .serializers import PayAccountSerializer, UserBillSerializer
from .utils import create_payment

User = get_user_model()


@api_view(['POST'])
def webhook_handler(request):
    try:
        notification_object = WebhookNotification(json.loads(request.body))
        print(notification_object)
        print(notification_object.object)
        print(notification_object.event)
        print(notification_object.type)
        print(notification_object.object.id)
        bill = UserBill.objects.get(yookassa_id=notification_object.object.id)
        if notification_object.object.status == 'succeeded':
            print(notification_object.object.status)
            bill.paid_at = timezone.now()
            bill.paid = True
            bill.save()

    except Exception as e:
        print(e)
    return Response({
        'data': 'Hello, world!',
    }, status=status.HTTP_200_OK)


class PayAccountsList(APIView):
    def get(self, request, *args, **kwargs):
        if User.Group.ADMINISTRATOR in request.user:
            return Response(PayAccountSerializer(
                PayAccount.objects.all(),
                context={'request': request},
                many=True
            ).data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CurrentBillsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(
            UserBillSerializer(
                user.bills.all(),
                context={'request': request},
                many=True
            ).data,
        )


# invoices/pay/<int>:id/
# {"bill_id": int} ->
# {"confirmation_url": "https://yoomoney.ru/checkout/payments/v2/contract?orderId=2a919bb7-000f-5000-9000-1cc21f5c9859"}
@api_view(['GET'])
def pay_bill(request, bill_id):
    # TODO: add try
    bill = UserBill.objects.get(id=bill_id)
    payment = create_payment(amount=bill.bill.amount, description=str(bill))
    bill.yookassa_id = payment.id
    bill.save()
    return Response({
        'status': True,
        'detail': 'success',
        'confirmation_url': payment.confirmation.confirmation_url},
        status=status.HTTP_200_OK
    )
