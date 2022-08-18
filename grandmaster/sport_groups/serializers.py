from rest_framework import serializers
from .models import SportGroup
from rest_framework.reverse import reverse


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

