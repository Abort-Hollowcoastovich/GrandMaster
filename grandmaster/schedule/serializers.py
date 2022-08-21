from rest_framework import serializers
from .models import Schedule
from authentication.models import User
from sport_groups.models import SportGroup
from gyms.models import Gym


class ScheduleSerializer(serializers.ModelSerializer):
    trainer = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    group = serializers.HyperlinkedRelatedField(view_name='sport_groups-detail', read_only=True)
    gym = serializers.HyperlinkedRelatedField(view_name='gyms-detail', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        trainer_id = int(self.context['request'].data.get('trainer'))
        group_id = int(self.context['request'].data.get('group'))
        gym_id = int(self.context['request'].data.get('group'))
        schedule = Schedule.objects.create(trainer=User.objects.get(pk=trainer_id),
                                           group=SportGroup.objects.get(pk=group_id),
                                           gym=Gym.objects.get(pk=gym_id), **validated_data)
        return schedule
