import json
from json import JSONDecodeError

from django.db.models import Count
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from schedule.models import Schedule
from .models import Gym
from authentication.models import User


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class TrainerSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()

    def get_schedules(self, obj):
        schedules = Schedule.objects.filter(sport_group__trainer=obj)
        print(schedules, len(schedules))
        data = []
        grouped = dict()
        for obj in schedules:
            grouped.setdefault(obj.sport_group, []).append(obj)
        for key, values in grouped.items():
            grouped_by_time = dict()
            for value in values:
                grouped_by_time.setdefault((value.start_time, value.finish_time), []).append(value)
            data.append({
                "min_age": key.min_age,
                "max_age": key.max_age,
                "items": [{
                    "start_time": key[0].strftime("%H:%M"),
                    "finish_time": key[1].strftime("%H:%M"),
                    "weekdays": [value.weekday for value in values]
                } for key, values in grouped_by_time.items()]
            })
        return data

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'photo',
            'schedules'
        ]


class GymResponseSerializer(serializers.ModelSerializer):
    trainers = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = '__all__'

    def get_trainers(self, obj):
        trainers = obj.trainers.all()
        return [TrainerSerializer(trainer, context={'request': self.context['request']}).data for trainer in trainers]


class GymSerializer(serializers.ModelSerializer):
    trainers = serializers.CharField()

    class Meta:
        model = Gym
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        trainers = self.get_items(validated_data, 'trainers')
        instance = super().create(validated_data)
        instance.trainers.set(trainers)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        trainers = self.get_items(validated_data, 'trainers')
        instance = super().update(instance, validated_data)
        instance.trainers.set(trainers)
        instance.save()
        return instance

    def get_items(self, validated_data, string):
        try:
            result = json.loads(validated_data.pop(string, '[]'))
        except JSONDecodeError:
            raise ValidationError
        return result

    def to_representation(self, instance):
        return GymResponseSerializer(instance, context=self.context).data
