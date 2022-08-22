from django.db import models
from schedule.models import Schedule


class VisitLog(models.Model):
    # TODO: (3) переделать модель полностью:
    #  1) одно расписание - много посещений -> ForeignKey с расписанием вместо OneToOne
    #  2) можно отмечать присутствующих -> ManyToMany с Users
    #  3) дата отметки: DateField (auto_now)
    day = models.OneToOneField(to=Schedule, related_name='date', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'visit_log'
