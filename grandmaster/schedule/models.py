from django.db import models
from django.db.models import Q, F
from sport_groups.models import SportGroup
from gyms.models import Gym
from authentication.models import User


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
    gym = models.ForeignKey(to=Gym, on_delete=models.DO_NOTHING, null=True)
    group = models.ForeignKey(to=SportGroup, related_name='schedule',  on_delete=models.DO_NOTHING, null=True)
    trainer = models.ForeignKey(to=User, related_name='my_schedules', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'schedule'
        constraints = [
            models.CheckConstraint(check=Q(finish_time__gte=F('start_time')), name='finish_time_gte_start_time')
        ]


