from django.db import models

from authentication.admin import User
from utils.image_path import PathAndHash


class ChatPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('chat/' + path)


class Chat(models.Model):
    class Type(models.TextChoices):
        CUSTOM = 'custom'
        AUTO = 'auto'
        DM = 'dm'

    name = models.CharField(max_length=256)
    members = models.ManyToManyField(to=User, related_name='chats', blank=True)
    cover = models.ImageField(upload_to=ChatPathAndHash('covers'), null=True, blank=True)
    type = models.CharField(choices=Type.choices, max_length=256, default='custom')
    owner = models.ForeignKey(to=User, related_name='own_chats', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Room({self.name})"


class Message(models.Model):
    chat = models.ForeignKey(to=Chat, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(to=User, related_name='messages', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=ChatPathAndHash('images'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    readers = models.ManyToManyField(to=User, blank=True, related_name='readed_messages')
    prefix = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'Message({self.chat} {self.author})'


class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    members = models.ManyToManyField(User, related_name="current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name})"
