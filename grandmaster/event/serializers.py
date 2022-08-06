from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'description', 'address', 'start_date', 'end_date', 'cover', 'number', 'members']
        read_only_fields = ['pk', 'number']
