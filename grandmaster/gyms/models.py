from django.db import models


class Gym(models.Model):
    b24_id = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    class Meta:
        db_table = 'gyms'
