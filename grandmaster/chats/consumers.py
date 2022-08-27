import base64
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile

from authentication.models import User
from chats.models import Message, Chat
from chats.serializers import MessageSerializer
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
        message_json = {
            "id": message.id,
            "author": {
                "id": message.author.id,
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
        message = await self.new_message(text, photo)
        message['image'] = HOST + message['image']
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }, ensure_ascii=False))
