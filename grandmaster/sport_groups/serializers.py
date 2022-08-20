from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import SportGroup
from authentication.models import User


class SportGroupSerializer(serializers.ModelSerializer):
    # members = serializers.SerializerMethodField('get_members', read_only=True)

    class Meta:
        model = SportGroup
        fields = '__all__'
        read_only_fields = ['id']

    # def get_members(self, obj):
    #     request = self.context.get("request")
    #     return [request.build_absolute_uri(reverse('user-detail', args=[member.pk])) for member in obj.members.all()]


class SportsmenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name'
        ]
