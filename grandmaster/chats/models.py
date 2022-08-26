from django.db import models

from authentication.admin import User
from utils.image_path import PathAndHash


class ChatCoverPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('users/' + path)


class Chat(models.Model):
    name = models.CharField(max_length=256)
    members = models.ManyToManyField(to=User, related_name='chats')
    cover = models.ImageField(upload_to=ChatCoverPathAndHash('chats/covers'), null=True, blank=True)
    dm = models.BooleanField(default=False)

    def __str__(self):
        return f"Room({self.name})"


class Message(models.Model):
    chat = models.ForeignKey(to=Chat, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(to=User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    readers = models.ManyToManyField(to=User, blank=True)

    def __str__(self):
        return f'Message({self.chat} {self.author})'
