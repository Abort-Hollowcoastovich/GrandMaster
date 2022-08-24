from django.utils import timezone
from datetime import timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from schedule.models import Schedule
from .models import VisitLog
from .serializers import VisitLogSerializer


class ScheduleView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return VisitLog.objects.all()
        elif User.Group.TRAINER in user:
            return VisitLog.objects.filter(schedule__sport_group__trainer=user)
        return VisitLog.objects.none()

    # TODO
    # def check_time(self, start_time, finish_time):
    #     now_time = timezone.now().time()
    #     if now_time < start_time and (start_time - now_time) > timedelta(minutes=30):
    #         raise ValidationError
    #     elif now_time > finish_time and (now_time - finish_time) > timedelta(minutes=30):
    #         raise ValidationError

    def get_object(self) -> VisitLog:
        params = self.request.query_params
        gym_id = params.get('gym', None)
        sport_group_id = params.get('sport_group', None)
        if not (gym_id and sport_group_id):
            raise ValidationError
        now_timedate = timezone.now()
        weekday = now_timedate.strftime('%A').lower()
        schedules = Schedule.objects.filter(
            weekday=weekday,
            gym_id=gym_id,
            sport_group_id=sport_group_id,
        )
        print(schedules)
        # TODO
        return None

    def get(self, request: Request):
        visit_log = self.get_object()
        if visit_log is None:
            raise NotFound
        return Response(VisitLogSerializer(visit_log).data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        visit_log = self.get_object()
        if visit_log is not None:
            return Response(status=status.HTTP_409_CONFLICT)
        visit_log = None  # TODO
        return Response(VisitLogSerializer(visit_log).data, status=status.HTTP_201_CREATED)

    def put(self, request: Request):
        visit_log = self.get_object()
        if visit_log is None:
            raise NotFound
        visit_log = None  # TODO
        return Response(VisitLogSerializer(visit_log).data, status=status.HTTP_205_RESET_CONTENT)

# TODO: добавить эндпоинт для формирования отчета
