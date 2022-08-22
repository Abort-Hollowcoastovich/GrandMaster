from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user or User.Group.TRAINER in user:
            return Schedule.objects.all()
        elif User.Group.TRAINER in user:
            pass  # TODO: (1) возвращать все расписания, которые относятся к тренеру, после убрать проверку на тренера в верхнем условии
        return Schedule.objects.none()

# TODO (2): добавить поиск нужного расписания согласно фигме:
#  {"gym_id": int, "sport_group_id: int"} -> [schedules_list]

