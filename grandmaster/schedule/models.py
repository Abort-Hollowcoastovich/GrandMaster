from django.db import models
from django.db.models import Q, F
from sport_groups.models import SportGroup
from gyms.models import Gym


class Schedule(models.Model):
    class WeekDay(models.TextChoices):
        MONDAY = 'monday'
        TUESDAY = 'tuesday'
        WEDNESDAY = 'wednesday'
        THURSDAY = 'thursday'
        FRIDAY = 'friday'
        SATURDAY = 'saturday'
        SUNDAY = 'sunday'

    weekday = models.CharField(choices=WeekDay.choices, max_length=10)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    gym = models.ForeignKey(to=Gym, related_name='schedules', on_delete=models.SET_NULL, null=True, blank=True)
    sport_group = models.ForeignKey(to=SportGroup, related_name='schedules', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'schedules'
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        return f'weekday:{self.weekday} gym_id:{self.gym.id} sport_group_id:{self.sport_group.id}'
