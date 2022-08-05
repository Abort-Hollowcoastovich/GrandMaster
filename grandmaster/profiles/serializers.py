from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Documents, UserProfile


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        exclude = ['id', 'user_profile']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedIdentityField(
        view_name='documents-detail'
    )

    class Meta:
        model = UserProfile
        exclude = ['user', 'url', 'b24_id']


class UserProfileHyperlinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['url']

    def to_representation(self, instance):
        return self.context.get('request').build_absolute_uri(reverse('userprofile-detail', args=[instance.pk]))
