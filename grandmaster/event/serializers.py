import json
from json import JSONDecodeError

from django.utils import timezone
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


class EventSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    ended = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id',
            'members',
            'name',
            'description',
            'address',
            'start_date',
            'end_date',
            'deadline_date',
            'cover',
            'open',
            'hidden',
            'number',
            'ended',
        ]
        read_only_fields = ['id']

    def get_ended(self, obj):
        now = timezone.now()
        return now > obj.deadline_date

    def update(self, instance, validated_data):
        members = self.get_items(validated_data, 'members')
        instance = super().update(instance, validated_data)
        instance.members.set(members)
        instance.save()
        return instance

    def get_valid_members(self):
        user = self.context['request'].user
        if user.is_anonymous:
            members = User.objects.none()
        elif User.Group.TRAINER in user:
            members = user.students.all()
        elif User.Group.PARENT in user:
            members = user.children.all()
        elif User.Group.MODERATOR in user or User.Group.ADMINISTRATOR in user:
            members = User.objects.all()
        else:
            members = User.objects.filter(id=user.id)
        return members

    def get_members(self, obj):
        valid_members = self.get_valid_members()
        all_members = obj.members.all()
        members = []
        for member in valid_members:
            members.append({
                "id": member.id,
                "full_name": member.full_name,
                "marked": member in all_members,
            })
        return members

    def get_items(self, validated_data, string):
        try:
            result = json.loads(validated_data.pop(string, '[]'))
        except JSONDecodeError:
            raise ValidationError
        return result
