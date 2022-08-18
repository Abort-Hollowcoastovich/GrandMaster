from django.db import models

from utils.image_path import PathAndHash
from authentication.models import User


class GymsPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('gyms/' + path)


class Gym(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=256)
    cover = models.ImageField(upload_to=GymsPathAndHash('covers'))
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'gyms'
        ordering = ['order']

    @property
    def trainers(self):
        return [schedule.group.trainer.id for schedule in self.schedules.all()]
