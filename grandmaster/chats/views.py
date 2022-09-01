from django.core.exceptions import BadRequest
from rest_framework import generics, filters
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.models import User
from chats.models import Chat
from chats.serializers import ChatSerializer, MessageSerializer, MemberSerializer
from profiles.models import SpecialContact


class ChatListView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chats = filter(self.is_not_empty, queryset)
        serializer = self.get_serializer(chats, many=True)
        return Response(sorted(serializer.data, key=lambda x: x['display_name']))

    def is_not_empty(self, chat):
        user = self.request.user
        if user.children.all().exists():
            user = self.get_child()
        if self.get_another_chat_member(chat, user) == user.trainer:
            return True
        folder = self.get_folder(chat, user)
        is_empty = len(chat.messages.all()) == 0
        if folder == 'none' and is_empty and chat.type == Chat.Type.DM:
            return False
        return True

    def get_folder(self, obj: Chat, user):
        if obj.type == Chat.Type.DM:
            member = self.get_another_chat_member(obj, user)
            if member is None:
                return 'none'
            if user.contact_type == User.CONTACT.TRAINER:
                if member.trainer == user:
                    return 'students'
                if hasattr(member, 'special'):
                    return 'specialists'
                if member.contact_type == User.CONTACT.TRAINER:
                    return 'trainers'

            elif user.contact_type == User.CONTACT.MODERATOR:
                if member.contact_type == User.CONTACT.TRAINER:
                    return 'trainers'
                if member.contact_type == User.CONTACT.MODERATOR:
                    return 'moderators'
                if member.contact_type == User.CONTACT.SPORTSMAN:
                    return 'students'
                if hasattr(member, 'special'):
                    return 'specialists'

            elif user.contact_type == User.CONTACT.SPORTSMAN:
                if hasattr(member, 'special'):
                    return 'specialists'

        return 'none'

    def get_another_chat_member(self, chat, user) -> User:
        for _member in chat.members.all():
            if _member != user:
                return _member

    def get_queryset(self):
        user = self.request.user
        if user.children.all().exists():
            user = self.get_child()
        self.check_chats_list(user)
        return user.chats.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.query_params
        child_id = params.get('id', None)
        context['child_id'] = child_id
        return context

    def get_child(self):
        params = self.request.query_params
        user = self.request.user
        child_id = params.get('id', None)
        if child_id is None:
            raise NotFound('Parents users need child id')
        child = get_object_or_404(User, id=child_id)
        if child not in user.children.all():
            raise BadRequest('You are not parent of this user')
        return child

    def check_chats_list(self, user):
        if user.contact_type == User.CONTACT.TRAINER:
            students = user.students.all()
            trainers = User.objects.filter(contact_type=User.CONTACT.TRAINER).exclude(pk=self.request.user.pk)
            specialists = [User.objects.get(id=id_['user']) for id_ in SpecialContact.objects.values('user')]
            self.create_dms(students)
            self.create_dms(trainers)
            self.create_dms(specialists)
        elif user.contact_type == User.CONTACT.MODERATOR:
            moderators = User.objects.filter(contact_type=User.CONTACT.MODERATOR)
            trainers = User.objects.filter(contact_type=User.CONTACT.TRAINER).exclude(pk=self.request.user.pk)
            specialists = [User.objects.get(id=id_['user']) for id_ in SpecialContact.objects.values('user')]
            # students = User.objects.filter(contact_type=User.CONTACT.SPORTSMAN) TODO:
            self.create_dms(moderators)
            self.create_dms(trainers)
            self.create_dms(specialists)
            # self.create_dms(students)
        elif user.contact_type == User.CONTACT.SPORTSMAN:
            specialists = [User.objects.get(id=id_['user']) for id_ in SpecialContact.objects.values('user')]
            if user.trainer is not None:
                self.create_dm(user.trainer)
            self.create_dms(specialists)
        elif user.contact_type == User.CONTACT.SPECIALIST:
            moderators = User.objects.filter(contact_type=User.CONTACT.MODERATOR)
            trainers = User.objects.filter(contact_type=User.CONTACT.TRAINER).exclude(pk=self.request.user.pk)
            # students = User.objects.filter(contact_type=User.CONTACT.SPORTSMAN)
            self.create_dms(moderators)
            self.create_dms(trainers)
            # self.create_dms(students)
        elif user.children.exists():
            raise BadRequest('Parent not allowed to own chats')

    def create_dms(self, users):
        for user in users:
            self.create_dm(user)

    def create_dm(self, obj):
        user = self.request.user
        members = [user.id, obj.id]
        name = f'dm_{user.id}{obj.id}'
        reversed_name = f'dm_{obj.id}{user.id}'
        if not user.chats.filter(name=name).exists() and not user.chats.filter(name=reversed_name).exists():
            print(f'created dm {str(members)}')
            chat = Chat.objects.create(
                name=name,
                type=Chat.Type.DM,
                owner=None
            )
            chat.members.set(members)
            chat.save()


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
        return get_object_or_404(Chat, id=chat_id)

    def get_user(self) -> User:
        user = self.request.user
        params = self.request.query_params
        if user.children.all().exists():
            id_ = params.get('id', None)
            if id_ is None:
                raise BadRequest('Need child id')
            child = get_object_or_404(User, id=id_)
            if child not in user.children.all():
                raise BadRequest('It is not your child')
            return child
        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.query_params
        child_id = params.get('id', None)
        context['child_id'] = child_id
        return context

    def get_queryset(self):
        chat = self.get_chat()
        user = self.get_user()
        if chat not in user.chats.all():
            raise PermissionDenied('You are not in this chat')
        messages = chat.messages.all().order_by('-created_at')
        user.readed_messages.add(*messages)
        user.save()
        return messages


class MembersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def get_queryset(self):
        user = self.request.user
        if User.Group.MODERATOR in user:
            return User.objects.filter(contact_type__in=[
                User.CONTACT.MODERATOR,
                User.CONTACT.TRAINER,
                User.CONTACT.SPORTSMAN
            ]).order_by('last_name', 'first_name', 'middle_name')
        elif User.Group.TRAINER in user:
            trainers = list(User.objects.filter(contact_type__in=[
                User.CONTACT.TRAINER,
            ]))
            my_students = list(user.students.all())
            return sorted(my_students + trainers, key=lambda x: x.last_name)
        elif user.contact_type == User.CONTACT.SPECIALIST:
            return User.objects.filter(contact_type__in=[
                User.CONTACT.MODERATOR,
                User.CONTACT.TRAINER,
                User.CONTACT.SPORTSMAN
            ]).order_by('last_name', 'first_name', 'middle_name')
        return User.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.query_params
        child_id = params.get('id', None)
        context['child_id'] = child_id
        return context


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
