from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['id']


class ScheduleListSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        sport_group = data.get('sport_group', None)
        gym = data.get('gym', None)
        raw_days = data.get('days', None)
        schedules = []
        if raw_days:
            for weekday, times in raw_days.items():
                if len(times) == 2:
                    schedules.append({
                        'weekday': weekday,
                        'start_time': times[0],
                        'finish_time': times[1],
                        'gym': gym,
                        'sport_group': sport_group,
                    })
        return schedules

    def to_representation(self, instance):
        pass