from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    address = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField()
    open = models.BooleanField(default=True)
    number = models.IntegerField()

    class Meta:
        ordering = ['start_date']

    @property
    def is_open(self):
        return self.open

    def __str__(self):
        return self.name
