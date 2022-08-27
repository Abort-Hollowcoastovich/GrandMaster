from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .models import SportGroup
from .permissions import IsTrainerOrAdminOrModerOnlyPermissions
from .serializers import SportGroupSerializer, SportsmenSerializer, TrainerSerializer


class SportGroupViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SportGroupSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return SportGroup.objects.all()
            elif User.Group.TRAINER in user:
                return user.my_groups
            elif user.Group.STUDENT in user:
                return user.sport_groups
        return SportGroup.objects.none()


class SportsmenList(generics.ListAPIView):
    serializer_class = SportsmenSerializer
    permission_classes = [IsTrainerOrAdminOrModerOnlyPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return User.objects.all()
            elif User.Group.TRAINER in user:
                return User.objects.filter(trainer=user)
        return SportGroup.objects.none()


class TrainersList(generics.ListAPIView):
    queryset = User.objects.filter(contact_type=User.CONTACT.TRAINER).all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]