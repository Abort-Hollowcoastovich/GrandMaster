import json

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
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


def serialize_schedules(sport_group_id: int, gym_id: int, schedules):
    def get_weekday_schedule_or_empty(query_set, weekday: str) -> list:
        items = query_set.filter(weekday=weekday)
        if items.exists():
            weekday = items[0]
            return [weekday.start_time, weekday.finish_time]
        return []

    return {
        'gym': gym_id,
        'sport_group': sport_group_id,
        'days': {
            'monday': get_weekday_schedule_or_empty(schedules, Schedule.WeekDay.MONDAY),
            'tuesday': get_weekday_schedule_or_empty(schedules, Schedule.WeekDay.TUESDAY),
            'wednesday': get_weekday_schedule_or_empty(schedules, Schedule.WeekDay.WEDNESDAY),
            'thursday': get_weekday_schedule_or_empty(schedules, Schedule.WeekDay.THURSDAY),
            'friday': get_weekday_schedule_or_empty(schedules, Schedule.WeekDay.FRIDAY),
            'saturday': get_weekday_schedule_or_empty(schedules, Schedule.WeekDay.SATURDAY),
            'sunday': get_weekday_schedule_or_empty(schedules, Schedule.WeekDay.SUNDAY),
        }
    }


def weekday_to_schedule(weekday: str, gym_id: int, sport_group_id: int, times: list):
    if times:
        return Schedule.objects.create(
            weekday=weekday,
            gym_id=gym_id,
            sport_group_id=sport_group_id,
            start_time=times[0],
            finish_time=times[1]
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
            return Response(data={"status": False, 'details': 'Need both ids'}, status=status.HTTP_404_NOT_FOUND)
        if not gym_id.isdigit() or not sport_group_id.isdigit():
            return Response(data={"status": False, 'details': 'Wrong format'}, status=status.HTTP_404_NOT_FOUND)
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        if not schedules.exists():
            return Response(data={"status": False, 'details': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = serialize_schedules(sport_group_id, gym_id, schedules)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        data = request.data
        gym_id = data.get('gym', None)
        sport_group_id = data.get('sport_group', None)
        if gym_id is None or sport_group_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not (gym_id.isdigit() and sport_group_id.isdigit()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        if schedules.exists():
            return Response(status=status.HTTP_409_CONFLICT)
        days = data.get('days', None)
        if not len(days) == 7:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        schedules = [weekday_to_schedule(Schedule.WeekDay.MONDAY, gym_id, sport_group_id, days['monday']),
                     weekday_to_schedule(Schedule.WeekDay.TUESDAY, gym_id, sport_group_id, days['tuesday']),
                     weekday_to_schedule(Schedule.WeekDay.WEDNESDAY, gym_id, sport_group_id, days['wednesday']),
                     weekday_to_schedule(Schedule.WeekDay.THURSDAY, gym_id, sport_group_id, days['thursday']),
                     weekday_to_schedule(Schedule.WeekDay.FRIDAY, gym_id, sport_group_id, days['friday']),
                     weekday_to_schedule(Schedule.WeekDay.SATURDAY, gym_id, sport_group_id, days['saturday']),
                     weekday_to_schedule(Schedule.WeekDay.SUNDAY, gym_id, sport_group_id, days['sunday'])]
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request: Request):
        def f(weekday, times, schedules, gym_id, sport_group_id):
            items = schedules.filter(weekday=weekday)
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
        data = request.data
        gym_id = data.get('gym', None)
        sport_group_id = data.get('sport_group', None)
        if gym_id is None or sport_group_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not (gym_id.isdigit() and sport_group_id.isdigit()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        if not schedules.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        days = data.get('days', None)
        if not len(days) == 7:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        f(Schedule.WeekDay.MONDAY, days['monday'], schedules, gym_id, sport_group_id)
        f(Schedule.WeekDay.TUESDAY, days['tuesday'], schedules, gym_id, sport_group_id)
        f(Schedule.WeekDay.WEDNESDAY, days['wednesday'], schedules, gym_id, sport_group_id)
        f(Schedule.WeekDay.THURSDAY, days['thursday'], schedules, gym_id, sport_group_id)
        f(Schedule.WeekDay.FRIDAY, days['friday'], schedules, gym_id, sport_group_id)
        f(Schedule.WeekDay.SATURDAY, days['saturday'], schedules, gym_id, sport_group_id)
        f(Schedule.WeekDay.SUNDAY, days['sunday'], schedules, gym_id, sport_group_id)
        schedules = Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        )
        data = serialize_schedules(sport_group_id, gym_id, schedules)
        return Response(data=data, status=status.HTTP_205_RESET_CONTENT)

    def delete(self, request: Request):
        params = request.query_params
        gym_id = params.get('gym', None)
        sport_group_id = params.get('sport_group', None)
        if gym_id is None or sport_group_id is None:
            return Response(data={'details': 'Need both ids', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        if not (gym_id.isdigit() and sport_group_id.isdigit()):
            return Response(data={'details': 'Wrong format', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        Schedule.objects.filter(
            gym_id=gym_id,
            sport_group_id=sport_group_id
        ).delete()
        return Response(data={'details': 'Successful delete', 'status': False}, status=status.HTTP_200_OK)