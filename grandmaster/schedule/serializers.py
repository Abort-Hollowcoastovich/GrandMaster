from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format="%H:%M")
    finish_time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['id']
