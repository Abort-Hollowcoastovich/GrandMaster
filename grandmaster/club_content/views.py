from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Content
from .serializers import ContentSerializer
from authentication.models import User


class ContentViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = ContentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return Content.objects.all()
        return Content.objects.filter(hidden=False)
