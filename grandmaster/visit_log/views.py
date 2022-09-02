import os
import uuid
from datetime import timedelta, datetime

import xlsxwriter as xlsxwriter
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer
from sport_groups.permissions import IsTrainerOrAdminOrModerOnlyPermissions
from .models import VisitLog
from .serializers import VisitLogSerializer
from grandmaster.settings import MEDIA_ROOT, MEDIA_URL


class ScheduleView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
            return VisitLog.objects.all()
        elif User.Group.TRAINER in user:
            return VisitLog.objects.filter(schedule__sport_group__trainer=user)
        return VisitLog.objects.none()

    def get_schedule(self):
        params = self.request.query_params
        gym_id = params.get('gym', None)
        sport_group_id = params.get('sport_group', None)
        if not (gym_id and sport_group_id):
            raise ValidationError('Need both ids in params')
        now_timedate = timezone.now()
        weekday = now_timedate.strftime('%A').lower()
        schedules = Schedule.objects.filter(
            weekday=weekday,
            gym_id=gym_id,
            sport_group_id=sport_group_id,
        )
        if not schedules.exists():
            return None
        return schedules[0]

    def get_object(self, queryset=None):
        schedule = self.get_schedule()
        if schedule is None:
            return None
        date = timezone.now().date()
        visit_logs = VisitLog.objects.filter(
            mark_datetime__day=date.day,
            mark_datetime__month=date.month,
            mark_datetime__year=date.year,
            schedule=schedule,
        )
        if visit_logs.exists():
            return visit_logs[0]
        return None

    def get(self, request: Request):
        schedule = self.get_schedule()
        if schedule is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data='No schedule for this gym with this sport group at this weekday')
        self.check_time(schedule)
        visit_log = self.get_object()
        if visit_log is None:
            return Response({'schedule': ScheduleSerializer(schedule).data, 'attending': []}, status=status.HTTP_200_OK)
        return Response(VisitLogSerializer(visit_log).data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        schedule = self.get_schedule()
        if schedule is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data='No schedule for this gym with this sport group at this weekday')
        self.check_time(schedule)
        data = request.data
        attending = data.get('attending', None)
        if attending is None:
            raise ValidationError('Need attending')
        visit_log = self.get_object()
        if visit_log is None:
            visit_log = VisitLog.objects.create(
                schedule=schedule,
            )
        visit_log.attending.set(attending)
        visit_log.save()
        return Response(VisitLogSerializer(visit_log).data, status=status.HTTP_200_OK)

    def delete(self, request: Request):
        visit_log = self.get_object()
        if visit_log is None:
            raise NotFound
        visit_log.delete()
        return Response("Successful delete", status=status.HTTP_200_OK)

    def check_time(self, schedule, delta=30):
        start_time = datetime.combine(timezone.now().date(), schedule.start_time)
        finish_time = datetime.combine(timezone.now().date(), schedule.finish_time)
        now_time = timezone.now()
        if (now_time < start_time) and ((start_time - now_time) > timedelta(minutes=delta)):
            raise ValidationError('Too early')
        elif (now_time > finish_time) and ((now_time - finish_time) > timedelta(minutes=delta)):
            raise ValidationError('Too late')


@api_view(['GET'])
@permission_classes([IsTrainerOrAdminOrModerOnlyPermissions])
def make_report(request: Request):
    params = request.query_params
    sport_group_id = params.get('sport_group', None)
    start_datetime = params.get('start_datetime', None)
    end_datetime = params.get('end_datetime', None)
    try:
        start_datetime = datetime.fromisoformat(start_datetime)
        end_datetime = datetime.fromisoformat(end_datetime)
    except ValueError:
        raise ValidationError('Invalid isoformat string')
    if not (sport_group_id and start_datetime and end_datetime):
        raise ValidationError('Not all params')
    if not (sport_group_id.isdigit()):
        raise ValidationError('Id must be integer')
    visit_logs = VisitLog.objects.filter(
        schedule__sport_group_id=sport_group_id,
        mark_datetime__gte=start_datetime,
        mark_datetime__lte=end_datetime,
    )
    data = []
    for visit_log in visit_logs:
        date = visit_log.mark_datetime
        sport_group_name = visit_log.schedule.sport_group.name
        trainer_full_name = visit_log.schedule.sport_group.trainer.full_name
        students = visit_log.attending.all()
        for student in students:
            data.append([str(date), student.full_name, sport_group_name, trainer_full_name])
    headers = ['Дата', 'Спортсмен', 'Спортивная группа', 'Тренер']
    filename = get_file_name('report.xlsx')
    filepath = os.path.join(os.path.join(MEDIA_ROOT, 'reports'), filename)
    save_to_file(filepath, data, headers)
    return Response(data={'url': 'https://' + request.get_host() + MEDIA_URL + 'reports/' + filename}, status=200)


def get_file_name(base_name):
    return uuid.uuid4().hex + base_name


def save_to_file(filename, data, header):
    data = [header] + data
    print(data)
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    for row, items in enumerate(data):
        for col, item in enumerate(items):
            worksheet.write(row, col, item)
    workbook.close()
