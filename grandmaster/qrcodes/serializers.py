from rest_framework import serializers
from rest_framework.request import Request

from authentication.models import User
from chats.models import Chat
from profiles.serializers import UserSerializer


class UserDetailsSerializer(serializers.ModelSerializer):
    documents = serializers.HyperlinkedIdentityField(
        view_name='documents-detail'
    )
    special = serializers.SerializerMethodField()
    admitted = serializers.BooleanField(source='is_admitted')
    parents = UserSerializer(many=True)
    children = UserSerializer(many=True)
    dm = serializers.SerializerMethodField()

    def get_dm(self, obj):
        request: Request = self.context['request']
        user = request.user
        if obj == user:
            return None
        if user.is_anonymous:
            return None
        members = [user.id, obj.id]
        name = f'dm_{user.id}{obj.id}'
        chat = user.chats.filter(name=name)
        if not chat.exists():
            print(f'created dm {str(members)}')
            chat = Chat.objects.create(
                name=name,
                type=Chat.Type.DM,
                owner=None
            )
            chat.members.set(members)
            return chat.id
        else:
            return chat.first().id

    def get_special(self, obj):
        if hasattr(obj, 'special'):
            return obj.special.name
        return None

    class Meta:
        model = User
        fields = [
            'id',
            'special',
            'documents',
            'admitted',
            'photo',
            'gender',
            'first_name',
            'last_name',
            'middle_name',
            'full_name',
            'birth_date',
            'contact_type',
            'phone_number',
            'sport_school',
            'department',
            'trainer_name',
            'training_place',
            'tech_qualification',
            'sport_qualification',
            'weight',
            'height',
            'region',
            'city',
            'address',
            'school',
            'med_certificate_date',
            'insurance_policy_date',
            'father_full_name',
            'father_birth_date',
            'father_phone_number',
            'father_email',
            'mother_full_name',
            'mother_birth_date',
            'mother_phone_number',
            'mother_email',
            'children',
            'parents',
            'dm',
        ]
