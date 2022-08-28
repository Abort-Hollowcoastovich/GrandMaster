import base64
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile

from authentication.models import User
from chats.models import Message, Chat
from grandmaster.settings import HOST


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'chat_%s' % self.chat_id
        self.user: User = self.scope['user']
        self.chat = await self.get_chat(self.chat_id)
        if self.user.is_anonymous:
            print('anonim')
            return
        if self.chat is None:
            print('no chat')
            return

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def new_message(self, text, photo_base64, author: User) -> dict:
        prefix = None
        if author is None:
            author = self.user
        else:
            if self.user.phone_number == author.father_phone_number:
                prefix = 'Отец'
            elif self.user.phone_number == author.mother_phone_number:
                prefix = 'Мать'
        if hasattr(self.user, 'special'):
            prefix = self.user.special.name
        message = Message.objects.create(
            chat=self.chat,
            text=text,
            author=author,
            prefix=prefix,
        )
        if len(photo_base64.strip()) != 0:
            data = ContentFile(base64.b64decode(photo_base64))
            file_name = "photo.png"
            message.image.save(file_name, data, save=True)
        message_json = {
            "id": message.id,
            "author": {
                "id": message.author.id,
                "full_name": message.author.full_name,
                "me": message.author == self.user,
            },
            "prefix": message.prefix,
            "text": message.text,
            "image": message.image.url if message.image else None,
            "created_at": str(message.created_at),
        }
        return message_json

    @database_sync_to_async
    def get_chat(self, chat_id):
        chat = Chat.objects.filter(id=chat_id)
        if chat.exists():
            return chat[0]
        return None

    @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.filter(id=user_id)
        if user.exists():
            return user.first()
        return None

    # Receive message from WebSocket
    async def receive(self, text_data):
        json_data = json.loads(text_data)
        json_message = json_data['message']
        text = json_message['text']
        photo = json_message['photo']
        id_ = json_message['id']
        author = await self.get_user(id_)
        message = await self.new_message(text, photo, author)
        if message['image'] is not None:
            message['image'] = HOST + message['image']
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    @database_sync_to_async
    def add_message_to_readed(self, id):
        self.user.readed_messages.add(id)
        self.user.save()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        await self.add_message_to_readed(message["id"])
        await self.send(text_data=json.dumps({
            'message': message
        }, ensure_ascii=False))
