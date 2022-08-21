from django.db import models
from .utils import PathAndHash


class Content(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    cover = models.ImageField(upload_to=PathAndHash('content/covers'), null=True)
    number = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)

    class Meta:
        db_table = 'club_content'

    def __str__(self):
        return self.name
