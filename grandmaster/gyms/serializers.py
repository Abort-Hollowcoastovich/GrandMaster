import json
from rest_framework import serializers
from .models import Gym
from authentication.models import User


class GymTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'photo'
        ]


class GymResponseSerializer(serializers.ModelSerializer):
    trainers = GymTrainerSerializer(many=True)
    class Meta:
        model = Gym
        fields = [
            'id',
            'title',
            'description',
            'address',
            'cover',
            'order',
            'trainers',
            'hidden',
        ]


class GymSerializer(serializers.ModelSerializer):
    trainers = serializers.CharField()

    class Meta:
        model = Gym
        fields = [
            'id',
            'title',
            'description',
            'address',
            'cover',
            'order',
            'trainers',
            'hidden',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        trainers_str = validated_data.pop('trainers', None)
        instance = super().create(validated_data)
        if trainers_str:
            trainers = json.loads(trainers_str)
            instance.trainers.add(*trainers)
        instance.save()
        return instance

    def to_representation(self, instance):
        return GymResponseSerializer(instance).data

    def update(self, instance, validated_data):
        trainers_str = validated_data.pop('trainers', None)
        instance = super().update(instance, validated_data)
        if trainers_str:
            trainers = json.loads(trainers_str)
            for trainer_id in trainers:
                if trainer_id not in instance.trainers.all():
                    instance.trainers.add(trainer_id)
            for trainer in instance.trainers.all():
                if trainer.id not in trainers:
                    instance.trainers.remove(trainer)
        instance.save()
        return instance


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
        ]
