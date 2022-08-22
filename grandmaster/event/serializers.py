import json
from rest_framework import serializers

from .models import Event
from authentication.models import User


class EventMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
        ]


class EventResponseSerializer(serializers.ModelSerializer):
    members = EventMembersSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    members = serializers.CharField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        members = json.loads(validated_data.pop('members', '[]'))
        instance = super().create(validated_data)
        instance.members.set(members)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        members = json.loads(validated_data.pop('members', '[]'))
        instance = super().update(instance, validated_data)
        instance.members.set(members)
        instance.save()
        return instance

    def to_representation(self, instance):
        return EventResponseSerializer(instance, context=self.context).data
