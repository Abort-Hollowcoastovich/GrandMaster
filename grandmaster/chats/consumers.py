import base64
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile

from grandmaster.settings import HOST
from authentication.models import User
from chats.models import Message, Chat, Room


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
    def new_message(self, text, photo_base64) -> dict:
        message = Message.objects.create(
            chat=self.chat,
            text=text,
            author=self.user,
        )
        if len(photo_base64.strip()) != 0:
            data = ContentFile(base64.b64decode(photo_base64))
            file_name = "photo.png"
            message.image.save(file_name, data, save=True)
        special = None
        if hasattr(message.author, 'special'):
            special = message.author.special.name
        message_json = {
            "id": message.id,
            "author": {
                "id": message.author.id,
                "special": special,
                "full_name": message.author.full_name,
                "me": message.author == self.user,
            },
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

    # Receive message from WebSocket
    async def receive(self, text_data):
        json_data = json.loads(text_data)
        json_message = json_data['message']
        text = json_message['text']
        photo = json_message['photo']
        id_ = json_message['id']
        message = await self.new_message(text, photo)
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
        # print(message, self.user)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }, ensure_ascii=False))
