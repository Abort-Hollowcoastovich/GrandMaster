from django.db import models
from .utils import PathAndHash


class Content(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    cover = models.ImageField(upload_to=PathAndHash('content/covers'), null=True)
    number = models.IntegerField(default=0)

    class Meta:
        db_table = 'club_content'

    def __str__(self):
        return self.name
