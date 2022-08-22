import json
from rest_framework import serializers

from .models import Gym
from authentication.models import User


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'photo'
        ]


class GymResponseSerializer(serializers.ModelSerializer):
    trainers = TrainerSerializer(many=True)

    class Meta:
        model = Gym
        fields = '__all__'


class GymSerializer(serializers.ModelSerializer):
    trainers = serializers.CharField()

    class Meta:
        model = Gym
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        trainers = json.loads(validated_data.pop('trainers', '[]'))
        instance = super().create(validated_data)
        instance.trainers.set(trainers)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        trainers = json.loads(validated_data.pop('trainers', '[]'))
        instance = super().update(instance, validated_data)
        instance.trainers.set(trainers)
        instance.save()
        return instance

    def to_representation(self, instance):
        return GymResponseSerializer(instance, context=self.context).data
