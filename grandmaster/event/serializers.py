import json
from json import JSONDecodeError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        members = self.get_items(validated_data, 'members')
        instance = super().create(validated_data)
        instance.members.set(members)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        members = self.get_items(validated_data, 'members')
        instance = super().update(instance, validated_data)
        instance.members.set(members)
        instance.save()
        return instance

    def get_items(self, validated_data, string):
        try:
            result = json.loads(validated_data.pop(string, '[]'))
        except JSONDecodeError:
            raise ValidationError
        return result

    def to_representation(self, instance):
        return EventResponseSerializer(instance, context=self.context).data
