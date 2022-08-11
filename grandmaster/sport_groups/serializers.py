from rest_framework import serializers
from .models import SportGroup
from authentication.models import User


class SportGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = SportGroup
        fields = ['pk', 'name', 'min_age', 'max_age', 'trainer', 'members']
        read_only_fields = ['pk']

