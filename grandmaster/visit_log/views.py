from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from sport_groups.models import SportGroup
from schedule.models import Schedule
from .models import VisitLog
from .serializers import VisitLogSerializer


class VisitLogViewSet(ModelViewSet):
    # TODO: (8) добавить в настройки права на модель path: (grandmaster.settings.project)
    permission_classes = [DjangoModelPermissions]
    serializer_class = VisitLogSerializer

    # TODO: (7) Убрать проверку на авторизацию, переделать
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return VisitLog.objects.all()
            elif User.Group.TRAINER in user:
                # TODO: (7) ??? no such field, возвращать только те посещения, которые относятся к тренеру, т.е.
                # VisitLog -> Schedule -> SportGroup -> User (Trainer)
                return user.my_visit_log
        return VisitLog.objects.none()

    # TODo: (5) ????????????
    @action(detail=True, methods=['put'])
    def add_member(self, request, *args, **kwargs):
        try:
            group = VisitLog.objects.get(pk=request.data['pk'])
        except User.DoesNotExist:
            return Response({
                'status': False,
                'details': 'No such user'
            }, status=status.HTTP_404_NOT_FOUND)
        instance = self.get_object()
        instance.group.add(group)
        instance.save()
        serializer = VisitLogSerializer(instance=instance)
        return Response(serializer.data)

    # TODo: (6) ????????????
    @action(detail=True, methods=['put'])
    def remove_member(self, request, *args, **kwargs):
        try:
            group = SportGroup.objects.get(pk=request.data['pk'])
        except User.DoesNotExist:
            return Response({
                'status': False,
                'details': 'No such user'
            }, status=status.HTTP_404_NOT_FOUND)
        instance = self.get_object()
        instance.group.remove(group)
        instance.save()
        serializer = VisitLogSerializer(instance=instance)
        return Response(serializer.data)


# TODO: (9) добавить эндпоинт для формирования отчета