from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.reverse import reverse

from chats.models import Chat
from authentication.models import User


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
    special = serializers.SerializerMethodField()
    admitted = serializers.BooleanField(source='is_admitted')
    parents = UserSerializer(many=True)
    children = serializers.SerializerMethodField()
    dm = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    def get_children(self, obj: User):
        if obj.contact_type == User.CONTACT.TRAINER:
            return []
        return UserSerializer(obj.children, many=True, context=self.context).data

    def get_phone_number(self, obj: User):
        # +7 (123) 123-12-12
        raw_phone = obj.phone_number
        if len(raw_phone) == 12:
            return f'{raw_phone[:2]} ({raw_phone[2:5]}) {raw_phone[5:8]}-{raw_phone[8:10]}-{raw_phone[10:12]}'
        return raw_phone

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
            chat.save()
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


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url']

    def to_representation(self, instance):
        return reverse('user-detail', args=[instance.pk])
