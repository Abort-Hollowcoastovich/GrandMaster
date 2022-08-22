from django.db import models
from django.db.models import Q, F
from sport_groups.models import SportGroup
from gyms.models import Gym


class Schedule(models.Model):
    class WeekDay(models.TextChoices):
        MONDAY = 'MN'
        TUESDAY = 'TU'
        WEDNESDAY = 'WE'
        THURSDAY = 'TH'
        FRIDAY = 'FR'
        SATURDAY = 'SA'
        SUNDAY = 'SU'

    weekday = models.CharField(choices=WeekDay.choices, max_length=10)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    gym = models.ForeignKey(to=Gym, related_name='schedules', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(to=SportGroup, related_name='schedules', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'schedule'
        constraints = [
            models.CheckConstraint(check=Q(finish_time__gte=F('start_time')), name='finish_time_gte_start_time')
        ]


