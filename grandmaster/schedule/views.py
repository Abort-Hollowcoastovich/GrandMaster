from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from authentication.models import User
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gym', 'sport_group']

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return Schedule.objects.all()
        elif User.Group.TRAINER in user:
            return Schedule.objects.filter(sport_group__trainer=user)
        return Schedule.objects.none()
