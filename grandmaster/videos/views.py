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

