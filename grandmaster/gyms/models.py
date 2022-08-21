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
    cover = models.ImageField(upload_to=GymsPathAndHash('covers'), null=True)
    order = models.PositiveIntegerField()
    hidden = models.BooleanField(default=False)
    trainers = models.ManyToManyField(to=User, related_name='gyms', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'gyms'
        ordering = ['order']
