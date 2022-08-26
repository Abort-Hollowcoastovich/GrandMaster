from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chats.models import Chat
from chats.serializers import ChatSerializer


class ChatListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return user.chats.all()
