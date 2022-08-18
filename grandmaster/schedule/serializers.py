from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['pk', 'day_of_the_week', 'start_time', 'finish_time', 'gym', 'group']
        read_only_fields = ['pk']
