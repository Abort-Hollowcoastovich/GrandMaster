from rest_framework import serializers

from authentication.models import User
from chats.models import Message, Chat
from profiles.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Message
        exclude = [
            'chat',
            'readers'
        ]
        depth = 1


class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    last_message = serializers.SerializerMethodField()
    unreaded_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "name",
            "members",
            "cover",
            "dm",
            "last_message"
        ]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data

    def get_unreaded_count(self, obj):
        request = self.context['request']
        user = request.user

    def get_user_unreaded_count(self, user: User, chat: Chat):
        count = 0
        # chat.messages.filter(readers__)
        # for message in chat.messages.all():
        #     if user not in message.readers.all()
        return count
