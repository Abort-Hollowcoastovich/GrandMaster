from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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

    day_of_the_week = models.CharField(choices=WeekDay.choices)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    gym = models.ForeignKey(to=Gym, related_name='my_groups', on_delete=models.DO_NOTHING, null=True)
    group = models.ManyToManyField(to=SportGroup, related_name='sport_groups', blank=True)

    class Meta:
        db_table = 'schedule'
        constraints = [
            models.CheckConstraint(check=Q(finish_time__gte=F('start_time')), name='finish_time_gte_start_time')
        ]


