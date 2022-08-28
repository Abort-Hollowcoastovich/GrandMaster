from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from authentication.models import User
from chats.models import Message, Chat


class MemberSerializer(serializers.ModelSerializer):
    me = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'special',
            'full_name',
            'photo',
            'contact_type',
            'me',
        ]

    def get_me(self, obj):
        request = self.context['request']
        user = request.user
        if user.id == obj.id:
            return True
        return False

    def get_special(self, obj):
        if hasattr(obj, 'special'):
            return obj.special.name
        return None


class MessageSerializer(serializers.ModelSerializer):
    author = MemberSerializer()

    class Meta:
        model = Message
        exclude = [
            'chat',
            'readers'
        ]


class ChatSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    owner = MemberSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unreaded_count = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()
    empty = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "display_name",
            "owner",
            "members",
            "cover",
            "type",
            "last_message",
            "unreaded_count",
            "folder",
            "name",
            "empty",
        ]
        read_only_fields = ["messages", "last_message"]

    def create(self, validated_data):
        request = self.context['request']
        data = request.data
        user = self.get_user()
        members = data.get('members', [])
        chat = Chat.objects.create(
            name=validated_data["name"],
            owner=user
        )
        members.append(self.context['request'].user.id)
        chat.members.set(members)
        return chat

    def get_folder(self, obj: Chat):
        user = self.get_user()
        if obj.type == Chat.Type.DM:
            member = self.get_another_chat_member(obj, user)

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
    def get_empty(self, obj: Chat):
        user = self.get_user()
        if self.get_another_chat_member(obj, user) == user.trainer:
            return False
        folder = self.get_folder(obj)
        is_empty = len(obj.messages.all()) == 0
        if folder == 'none' and is_empty and obj.type == Chat.Type.DM:
            return True
        return False

    def get_user(self):
        child_id = self.context['child_id']
        if self.context['child_id'] is not None:
            return get_object_or_404(User, id=child_id)
        return self.context['request'].user

    def get_display_name(self, obj: Chat):
        try:
            user = self.get_user()
        except Exception:
            return "Ошибка сервера"
        if obj.type == Chat.Type.DM:
            members = obj.members.all()
            if len(obj.members.all()) == 2:
                for member in members:
                    if member != user:
                        if hasattr(member, 'special'):
                            return member.special.name
                        return member.full_name
                return obj.name
            else:
                print('Chat error')
        elif obj.type == Chat.Type.AUTO:
            return obj.name
        elif obj.type == Chat.Type.CUSTOM:
            return obj.name
        return "Без имени"

    def get_last_message(self, obj):
        message = obj.messages.order_by('created_at').last()
        if message:
            json_message = MessageSerializer(message, context=self.context).data
            image = json_message['image']
            text = json_message['text']
            if len(text.strip()) == 0 and len(image.strip()) > 0:
                json_message['text'] = "Изображение"
            return json_message
        return MessageSerializer(message, context=self.context).data

    def get_unreaded_count(self, obj):
        user = self.get_user()
        return self.get_user_unreaded_count(user, obj)

    def get_user_unreaded_count(self, user: User, chat: Chat):
        readed_messages = len(user.readed_messages.filter(chat=chat))
        all_messages = len(Message.objects.filter(chat=chat))
        return all_messages - readed_messages
