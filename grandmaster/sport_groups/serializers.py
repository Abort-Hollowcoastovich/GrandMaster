from rest_framework import serializers

from .models import SportGroup
from authentication.models import User


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'photo'
        ]


class SportsmenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
        ]


class SportGroupResponseSerializer(serializers.ModelSerializer):
    members = SportsmenSerializer(many=True)

    class Meta:
        model = SportGroup
        fields = '__all__'


class SportGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportGroup
        fields = '__all__'
        read_only_fields = ['id']

    def to_representation(self, instance):
        return SportGroupResponseSerializer(instance, context=self.context).data
