from rest_framework import serializers
from .models import VisitLog


class VisitLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitLog
        fields = ['pk', 'day']
        read_only_fields = ['pk']
