from rest_framework import generics
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from chats.models import Chat
from chats.serializers import ChatSerializer, MessageSerializer


class ChatListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return user.chats.all()


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_chat(self):
        params = self.request.query_params
        chat_id = params.get('chat', None)
        if chat_id is None:
            raise NotFound
        chat = Chat.objects.filter(id=chat_id)
        if not chat.exists():
            raise NotFound
        return chat[0]

    def get_queryset(self):
        chat = self.get_chat()
        user = self.request.user
        if chat not in user.chats.all():
            raise PermissionDenied
        return chat.messages.all().order_by('-created_at')
