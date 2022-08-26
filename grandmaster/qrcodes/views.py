import base64
import qrcode
from qrcode.image.svg import SvgImage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated


class ForPartnersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return Response({
                'status': False,
                'details': 'Unauthorized'
            },
                status=status.HTTP_401_UNAUTHORIZED)
        data = f'grandmaster://app.grandmaster.center/?user={user.id}&type=partner'
        img = qrcode.make(data, image_factory=SvgImage).to_string()
        return Response({
            'status': True,
            'details': 'Success',
            'data': base64.standard_b64encode(img),
        },
            status=status.HTTP_200_OK)


class ForEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return Response({
                'status': False,
                'details': 'Unauthorized'
            },
                status=status.HTTP_401_UNAUTHORIZED)
        data = f'grandmaster://app.grandmaster.center/?user={user.id}&type=event'
        img = qrcode.make(data, image_factory=SvgImage).to_string()
        return Response({
            'status': True,
            'details': 'Success',
            'data': base64.standard_b64encode(img),
        },
            status=status.HTTP_200_OK)
