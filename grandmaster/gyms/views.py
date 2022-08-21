from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.generics import ListAPIView

from .serializers import GymSerializer, TrainerSerializer, GymResponseSerializer
from .models import Gym
from authentication.models import User


class GymViewSet(ModelViewSet):
    serializer_class = GymSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return Gym.objects.all()
        return Gym.objects.filter(hidden=False)


class TrainersList(ListAPIView):
    queryset = User.objects.filter(contact_type=User.CONTACT.TRAINER).all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]
