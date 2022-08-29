from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q, F
from authentication.models import User
from chats.models import Chat


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
    trainer = models.ForeignKey(to=User, related_name='my_groups',
                                on_delete=models.SET_NULL, blank=True, null=True)
    members = models.ManyToManyField(to=User, related_name='sport_groups', blank=True)
    chat = models.OneToOneField(to=Chat, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'sport_groups'
        constraints = [
            models.CheckConstraint(check=Q(max_age__gte=F('min_age')), name='max_age_gte_min_age')
        ]
        verbose_name = 'Спортивная группа'
        verbose_name_plural = 'Спортивные группы'


@receiver(post_save, sender=SportGroup)
def sport_group_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if created:
        chat = Chat.objects.create(
            name=instance.name,
            type=Chat.Type.AUTO,
            owner=instance.trainer
        )
        members = list(instance.members.all())
        members.append(instance.trainer)
        chat.members.set(members)
        instance.chat = chat
        instance.save()


def members_changed(sender, **kwargs):
    instance = kwargs['instance']
    members = list(instance.members.all())
    members.append(instance.trainer)
    instance.chat.members.set(members)
    instance.save()


m2m_changed.connect(members_changed, sender=SportGroup.members.through)
