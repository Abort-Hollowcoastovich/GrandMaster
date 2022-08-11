from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q, F
from authentication.models import User


class SportGroup(models.Model):
    name = models.CharField(max_length=100)
    min_age = models.IntegerField(validators=[
        MaxValueValidator(150),
        MinValueValidator(1)
    ])
    max_age = models.IntegerField(validators=[
        MaxValueValidator(150),
        MinValueValidator(1)
    ])
    trainer = models.ForeignKey(to=User, related_name='my_groups', on_delete=models.DO_NOTHING, null=True)
    members = models.ManyToManyField(to=User, related_name='sport_groups', blank=True)

    class Meta:
        db_table = 'sport_groups'
        constraints = [
            models.CheckConstraint(check=Q(max_age__gte=F('min_age')), name='max_age_gte_min_age')
        ]
