from rest_framework import serializers
from .models import SportGroup
from rest_framework.reverse import reverse
from authentication.models import User


class SportGroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField('get_members', read_only=True)
    trainer = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = SportGroup
        fields = '__all__'
        read_only_fields = ['id']

    def get_members(self, obj):
        request = self.context.get("request")
        return [request.build_absolute_uri(reverse('user-detail', args=[member.pk])) for member in obj.members.all()]

    def create(self, validated_data):
        trainer_id = int(self.context['request'].data.get('trainer'))
        members_ids = [int(i) for i in self.context['request'].data.get('members')]
        trainer = User.objects.get(pk=trainer_id)
        sport_group = SportGroup.objects.create(trainer=trainer, **validated_data)
        for id in members_ids:
            sport_group.members.add(User.objects.get(pk=id))
        return sport_group
