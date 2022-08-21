from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import SportGroup
from authentication.models import User


class SportsmenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
        ]


class SportGroupSerializer(serializers.ModelSerializer):
    members = SportsmenSerializer(many=True)

    class Meta:
        model = SportGroup
        fields = '__all__'
        read_only_fields = ['id']


class SportsmenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name'
        ]
