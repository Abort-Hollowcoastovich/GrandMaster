from django.db import models

from authentication.models import User


class SpecialContact(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='special')
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name} - {str(self.user)}'

    class Meta:
        verbose_name = 'Спец. контакт'
        verbose_name_plural = 'Спец. контакты'
