from django.utils import timezone
from datetime import timedelta

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .models import VisitLog
from .serializers import VisitLogSerializer


class VisitLogViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = VisitLogSerializer

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return VisitLog.objects.all()
        elif User.Group.TRAINER in user:
            return VisitLog.objects.filter(schedule__sport_group__trainer=user)
        return VisitLog.objects.none()

    def update(self, request, *args, **kwargs):
        schedule = self.get_object()
        self.check_time(schedule.start_time, schedule.finish_time)
        super().update(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
        # self.check_time()
        # super().create(request, *args, **kwargs)
# TODO: создание по дате и времени
    def check_time(self, start_time, finish_time):
        now_time = timezone.now().time()
        if now_time < start_time and (start_time - now_time) > timedelta(minutes=30):
            raise ValidationError
        elif now_time > finish_time and (now_time - finish_time) > timedelta(minutes=30):
            raise ValidationError


# TODO: добавить эндпоинт для формирования отчета
