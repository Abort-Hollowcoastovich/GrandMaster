from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

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


class UserDetailsSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedIdentityField(
        view_name='documents-detail'
    )
    admitted = serializers.BooleanField(source='is_admitted')

    class Meta:
        model = User
        exclude = [
            'b24_id',
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
            'password',
            'last_login',
            'active',
            'admin',
            'user_permissions',
            'groups',
            'parents',
            'trainer',
        ]


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url']

    def to_representation(self, instance):
        return self.context.get('request').build_absolute_uri(reverse('user-detail', args=[instance.pk]))
