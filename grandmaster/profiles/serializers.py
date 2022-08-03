from rest_framework import serializers

from .models import Document, UserProfile


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
