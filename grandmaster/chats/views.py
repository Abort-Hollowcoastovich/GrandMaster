from django.core.exceptions import BadRequest
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


# todo: change perms
class ChatDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


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
            ]).order_by('last_name').order_by('first_name').order_by('middle_name')
        elif User.Group.TRAINER in user:
            return User.objects.filter(contact_type__in=[
                User.CONTACT.TRAINER,
                User.CONTACT.SPORTSMAN,
            ]).order_by('last_name').order_by('first_name').order_by('middle_name')
        return User.objects.none()


def get_chat(params):
    chat_id = params.get('chat', None)
    if chat_id is None:
        raise NotFound("Need chat id")
    chat = Chat.objects.filter(id=chat_id)
    if not chat.exists():
        raise NotFound("Chat does not exist")
    return chat[0]


def get_member(params):
    member_id = params.get('member', None)
    if member_id is None:
        raise NotFound("Need member id")
    member = User.objects.filter(id=member_id)
    if not member.exists():
        raise NotFound("Member does not exist")
    return member[0]


# TODO: check chat type
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_chat(request: Request):
    params = request.query_params
    chat = get_chat(params)
    if request.user not in chat.members.all():
        raise BadRequest('You are not in this chat')
    chat.members.remove(request.user)
    return Response(status=200)


# TODO: check rights
#       check chat type
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def remove_member(request: Request):
    params = request.query_params
    chat = get_chat(params)
    member = get_member(params)
    if member not in chat.members.all():
        raise BadRequest('User is not in this chat')
    chat.members.remove(member)
    return Response(status=200)
