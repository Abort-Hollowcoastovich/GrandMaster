from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from chats.models import Chat

User = get_user_model()


class DocumentsDetailsSerializer(serializers.ModelSerializer):
    other_documents = serializers.SerializerMethodField('get_other_documents')

    class Meta:
        model = User
        fields = [
            'passport_or_birth_certificate',
            'oms_policy',
            'school_ref',
            'insurance_policy',
            'tech_qual_diplo',
            'med_certificate',
            'foreign_passport',
            'inn',
            'diploma',
            'snils',
            'other_documents'
        ]

    def get_other_documents(self, obj):
        request = self.context.get("request")
        return [request.build_absolute_uri(el.image.url) for el in obj.other_documents.all()]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name'
        ]


class UserDetailsSerializer(serializers.ModelSerializer):
    documents = serializers.HyperlinkedIdentityField(
        view_name='documents-detail'
    )
    admitted = serializers.BooleanField(source='is_admitted')
    parents = UserSerializer(many=True)
    children = UserSerializer(many=True)
    dm = serializers.SerializerMethodField()

    def get_dm(self, obj):
        request: Request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return ''
        members = [user.id, obj.id]
        name = f'dm_{user.id}{obj.id}'
        inter_chat = set(user.chats.filter(type=Chat.Type.DM)).intersection(obj.chats.filter(type=Chat.Type.DM))
        if len(inter_chat) > 0:
            chat = inter_chat.pop()
        else:
            chat = Chat.objects.create(
                name=name,
                type=Chat.Type.DM,
                owner=None
            )
            chat.members.set(members)
        return chat.id

    class Meta:
        model = User
        fields = [
            'id',
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


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url']

    def to_representation(self, instance):
        return reverse('user-detail', args=[instance.pk])
