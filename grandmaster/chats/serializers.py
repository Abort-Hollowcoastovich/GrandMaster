from rest_framework import serializers

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
    last_message = serializers.SerializerMethodField()
    unreaded_count = serializers.SerializerMethodField()
    owner = MemberSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = [
            "id",
            "name",
            "owner",
            "members",
            "cover",
            "type",
            "last_message",
            "unreaded_count"
        ]
        read_only_fields = ["messages", "last_message"]

    def create(self, validated_data):
        request = self.context['request']
        data = request.data
        user = request.user
        members = data.get('members', [])
        chat = Chat.objects.create(
            name=validated_data["name"],
            owner=user
        )
        members.append(self.context['request'].user.id)
        chat.members.set(members)
        return chat

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('created_at').last(), context=self.context).data

    def get_unreaded_count(self, obj):
        request = self.context['request']
        user = request.user
        return self.get_user_unreaded_count(user, obj)

    def get_user_unreaded_count(self, user: User, chat: Chat):
        readed_messages = len(user.readed_messages.filter(chat=chat))
        all_messages = len(Message.objects.filter(chat=chat))
        return all_messages - readed_messages
