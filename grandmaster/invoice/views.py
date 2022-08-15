import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from yookassa.domain.notification import WebhookNotification


@api_view(['POST'])
def webhook_handler(request):
    notification_object = WebhookNotification(json.loads(request.body)).object
    print(notification_object)
    return Response({
        'data': 'Hello, world!',
    }, status=status.HTTP_200_OK)
