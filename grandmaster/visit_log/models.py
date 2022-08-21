from django.db import models
from schedule.models import Schedule
from authentication.models import User


class VisitLog(models.Model):
    # TODO: (3) переделать модель полностью:
    #  1) одно расписание - много посещений -> ForeignKey с расписанием вместо OneToOne
    #  2) можно отмечать присутствующих -> ManyToMany с Users
    #  3) дата отметки: DateField (auto_now)
    day = models.ForeignKey(to=Schedule, related_name='date', on_delete=models.DO_NOTHING, null=True)
    attendance = models.ManyToManyField(to=User)
    date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'visit_log'
