from django.db import models

from authentication.admin import User
from schedule.models import Schedule


class VisitLog(models.Model):
    schedule = models.ForeignKey(to=Schedule, related_name='visit_logs', on_delete=models.SET_NULL, null=True, blank=True)
    attending = models.ManyToManyField(to=User, blank=True)
    mark_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visit_log'
