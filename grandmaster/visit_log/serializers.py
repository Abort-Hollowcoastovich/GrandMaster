from rest_framework import serializers
from .models import VisitLog


class VisitLogSerializer(serializers.ModelSerializer):
    # TODO: (4) Переделать в соответствии с новой моделью
    class Meta:
        model = VisitLog
        fields = ['id', 'day', 'attendance', 'date']
        read_only_fields = ['pk']
