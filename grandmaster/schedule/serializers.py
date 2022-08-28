from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format="%H:%M")
    finish_time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Schedule
        fields = [
            'id',
            'weekday',
            'start_time',
            'finish_time',
            'gym',
            'sport_group',
        ]
        read_only_fields = ['id']
