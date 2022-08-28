import base64
import qrcode
from qrcode.image.svg import SvgImage
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from authentication.models import User
from qrcodes.serializers import UserDetailsSerializer


class ForPartnersView(APIView):
    permission_classes = [IsAuthenticated]

    # TODO: check if parent
    def get(self, request: Request, *args, **kwargs):
        user = request.user
        params = request.query_params
        child_id = params.get('id', None)
        if child_id is not None:
            user = get_object_or_404(User, id=child_id)
        data = f'https://app.grandmaster.center/?user={user.id}&type=partner'
        img = qrcode.make(data, image_factory=SvgImage).to_string()
        return Response({
            'status': True,
            'details': 'Success',
            'data': base64.standard_b64encode(img),
        },
            status=status.HTTP_200_OK)


class ForEventsView(APIView):
    permission_classes = [IsAuthenticated]

    # TODO: check if parent
    def get(self, request, *args, **kwargs):
        user = request.user
        params = request.query_params
        child_id = params.get('id', None)
        if child_id is not None:
            user = get_object_or_404(User, id=child_id)
        data = f'https://app.grandmaster.center/?user={user.id}&type=event'
        img = qrcode.make(data, image_factory=SvgImage).to_string()
        return Response({
            'status': True,
            'details': 'Success',
            'data': base64.standard_b64encode(img),
        },
            status=status.HTTP_200_OK)


class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
