from rest_framework import serializers

from chats.models import Message, Chat
from profiles.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Message
        exclude = [
            'chat'
        ]
        depth = 1


class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    last_message = serializers.SerializerMethodField()

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
