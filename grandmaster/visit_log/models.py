from django.db import models
from schedule.models import Schedule


class VisitLog(models.Model):
    day = models.OneToOneField(to=Schedule, related_name='date', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'visit_log'
