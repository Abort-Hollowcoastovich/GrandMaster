from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions

from .models import Video
from .serializers import VideoSerializer
from authentication.models import User


class VideoViewSet(ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return Video.objects.all()
        return Video.objects.filter(hidden=False)

