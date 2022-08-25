import json

from django.core.exceptions import BadRequest
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from authentication.models import User
from .models import Schedule
from .serializers import ScheduleSerializer


# class ScheduleViewSet(ModelViewSet):
#     permission_classes = [DjangoModelPermissions]
#     serializer_class = ScheduleSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['gym', 'sport_group']
#
#     def get_queryset(self):
#         user = self.request.user
#         if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
#             return Schedule.objects.all()
#         elif User.Group.TRAINER in user:
#             return Schedule.objects.filter(sport_group__trainer=user)
#         return Schedule.objects.none()


def serialize_schedules(sport_group_id: int, gym_id: int, schedules):
    days = {}
    for weekday, _ in Schedule.WeekDay.choices:
        days[weekday] = []
        items = schedules.filter(weekday=weekday)
        if items.exists():
            days[weekday] = [items[0].start_time, items[0].finish_time]
    return {
        'gym': gym_id,
        'sport_group': sport_group_id,
        'days': days
    }


def weekday_to_schedule(weekday: str, gym_id: int, sport_group_id: int, days: dict):
    if days[weekday]:
        return Schedule.objects.create(
            weekday=weekday,
            gym_id=gym_id,
            sport_group_id=sport_group_id,
            start_time=days[weekday][0],
            finish_time=days[weekday][1]
        )


class ScheduleView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return Schedule.objects.all()
        elif User.Group.TRAINER in user:
            return Schedule.objects.filter(sport_group__trainer=user)
        return Schedule.objects.none()

    def get(self, request: Request):
        params = request.query_params
        gym_id = params.get('gym', None)
        sport_group_id = params.get('sport_group', None)
        if gym_id is None or sport_group_id is None:
            raise ValidationError("Need both ids")
        if not gym_id.isdigit() or not sport_group_id.isdigit():
            raise ValidationError("Wrong format")
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        if not schedules.exists():
            raise NotFound
        data = serialize_schedules(sport_group_id, gym_id, schedules)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        data = request.data
        gym_id = data.get('gym', None)
        sport_group_id = data.get('sport_group', None)
        if gym_id is None or sport_group_id is None:
            raise ValidationError("Need both ids")
        if not (gym_id.isdigit() and sport_group_id.isdigit()):
            raise ValidationError("Wrong format")
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        if schedules.exists():
            return Response(status=status.HTTP_409_CONFLICT)
        days = data.get('days', None)
        if not len(days) == 7:
            raise ValidationError('Need all weekdays')
        if set(days.keys()) != set([choice for choice, _ in Schedule.WeekDay.choices]):
            raise ValidationError('Wrong weekdays')
        for weekday, times in days.items():
            if len(times) == 2:
                Schedule.objects.create(
                    weekday=weekday,
                    start_time=times[0],
                    finish_time=times[1],
                    gym_id=gym_id,
                    sport_group_id=sport_group_id,
                )
        schedule_objects = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        data = serialize_schedules(sport_group_id, gym_id, schedule_objects)
        return Response(data=data, status=status.HTTP_201_CREATED)

    def put(self, request: Request):
        # VALIDATION START
        data = request.data
        gym_id = data.get('gym', None)
        sport_group_id = data.get('sport_group', None)
        if gym_id is None or sport_group_id is None:
            raise ValidationError("Need both ids")
        if not (gym_id.isdigit() and sport_group_id.isdigit()):
            raise ValidationError("Wrong format")
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        if not schedules.exists():
            raise NotFound
        days = data.get('days', None)
        if not len(days) == 7:
            raise ValidationError('Need all weekdays')
        if set(days.keys()) != set([choice for choice, _ in Schedule.WeekDay.choices]):
            raise ValidationError('Wrong weekdays')
        # VALIDATION END
        print(days)
        for weekday, _ in Schedule.WeekDay.choices:
            times = days[weekday]
            items = Schedule.objects.filter(
                gym_id=gym_id,
                sport_group_id=sport_group_id,
                weekday=weekday
            )
            if items.exists() and not times:
                items.delete()
            elif not items.exists() and times:
                Schedule.objects.create(
                    weekday=weekday,
                    start_time=times[0],
                    finish_time=times[1],
                    gym_id=gym_id,
                    sport_group_id=sport_group_id,
                )
            elif items.exists() and times:
                schedule = schedules[0]
                schedule.start_time = times[0]
                schedule.finish_time = times[1]
                schedule.save()
        schedule_objects = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        data = serialize_schedules(sport_group_id, gym_id, schedule_objects)
        return Response(data=data, status=status.HTTP_205_RESET_CONTENT)

    def delete(self, request: Request):
        params = request.query_params
        gym_id = params.get('gym', None)
        sport_group_id = params.get('sport_group', None)
        if gym_id is None or sport_group_id is None:
            return Response(data={'details': 'Need both ids', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        if not (gym_id.isdigit() and sport_group_id.isdigit()):
            return Response(data={'details': 'Wrong format', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        if not schedules.exists():
            raise NotFound
        schedules.delete()
        return Response(data={'details': 'Successful delete', 'status': True}, status=status.HTTP_200_OK)
