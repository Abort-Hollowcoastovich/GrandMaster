from django.db import models


class PayAccount(models.Model):
    name = models.CharField(max_length=256)
    account_id = models.CharField(max_length=256)
    secret_key = models.CharField(max_length=256)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
