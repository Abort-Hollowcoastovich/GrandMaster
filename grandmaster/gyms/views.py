from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .models import Gym
from .serializers import GymSerializer


class GymViewSet(ModelViewSet):
    serializer_class = GymSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return Gym.objects.all()
        return Gym.objects.filter(hidden=False)


class TrainerGymsList(ListAPIView):
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return Gym.objects.all()
        if User.Group.TRAINER in user:
            return user.gyms
        return Gym.objects.none()
