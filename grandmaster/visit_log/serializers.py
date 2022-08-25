from rest_framework import serializers

from authentication.admin import User
from schedule.serializers import ScheduleSerializer
from .models import VisitLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name'
        ]
        read_only_fields = [
            'id',
            'full_name'
        ]


class VisitLogSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    attending = UserSerializer(many=True)

    class Meta:
        model = VisitLog
        fields = '__all__'
        read_only_fields = ['id']
