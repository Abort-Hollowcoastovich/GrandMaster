from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from sport_groups.models import SportGroup
from authentication.models import User
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleViewSet(ModelViewSet):
    # permission_classes = [DjangoModelPermissions]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user = self.request.user
        # if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
        #     return Schedule.objects.all()
        # elif User.Group.TRAINER in user:
        #     return Schedule.objects.filter(trainer=user.id) # TODO: (1) возвращать все расписания, которые относятся к тренеру, после убрать проверку на тренера в верхнем условии
        return Schedule.objects.none()

# TODO (2): добавить поиск нужного расписания согласно фигме:
#  {"gym_id": int, "sport_group_id: int"} -> [schedules_list]


class SpecificScheduleView(RetrieveAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = ScheduleSerializer(instance=Schedule.objects.filter(group=SportGroup.objects.get(pk=request.data['sport_group']).first()))
        return Response(serializer.data)
