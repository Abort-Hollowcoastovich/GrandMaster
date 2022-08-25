from rest_framework import serializers

from schedule.serializers import ScheduleSerializer
from .models import VisitLog


class VisitLogSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()

    class Meta:
        model = VisitLog
        fields = '__all__'
        read_only_fields = ['id']
