from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.models import User
from chats.models import Chat
from chats.serializers import ChatSerializer, MessageSerializer, MemberSerializer


class ChatListView(generics.ListAPIView, generics.CreateAPIView):
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


class MembersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def get_queryset(self):
        user = self.request.user
        if User.Group.MODERATOR in user:
            return User.objects.filter(contact_type__in=[
                User.CONTACT.MODERATOR,
                User.CONTACT.TRAINER,
                User.CONTACT.SPORTSMAN,
            ])
        elif User.Group.TRAINER in user:
            return User.objects.filter(contact_type__in=[
                User.CONTACT.TRAINER,
                User.CONTACT.SPORTSMAN,
            ])
        return User.objects.none()


# TODO: check chat type
#       check is user has this chat
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_chat(request: Request):
    params = request.query_params
    chat_id = params.get('chat', None)
    if chat_id is None:
        raise NotFound
    chat = Chat.objects.filter(id=chat_id)
    if not chat.exists():
        raise NotFound
    chat = chat[0]
    chat.members.remove(request.user)
    return Response(status=200)
