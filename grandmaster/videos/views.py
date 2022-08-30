import requests
from django.http import HttpResponse
from rest_framework.decorators import api_view

from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Video
from .serializers import VideoSerializer
from authentication.models import User


class VideoViewSet(ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return Video.objects.all()
        return Video.objects.filter(hidden=False)


@api_view(['GET'])
def video_image(request: Request):
    params = request.query_params
    id = params.get('id', None)
    if id is None:
        raise NotFound
    url = f'https://img.youtube.com/vi/{id}/sddefault.jpg'
    response = requests.get(url)
    if response.status_code == 200:
        return HttpResponse(response.content, content_type='image/jpeg')
