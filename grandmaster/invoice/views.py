import json
from yookassa.domain.notification import WebhookNotification

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import PayAccount
from .serializers import PayAccountSerializer

User = get_user_model()


@api_view(['POST'])
def webhook_handler(request):
    try:
        notification_object = WebhookNotification(json.loads(request.body))
        print(notification_object)
        print(notification_object.object)
        print(notification_object.event)
        print(notification_object.type)
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
                context={'request': request}
            ).data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
