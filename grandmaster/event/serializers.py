import io
import base64

from django.core.files import File
from rest_framework import serializers
from .models import Event


class EventResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'description',
            'address',
            'start_date',
            'end_date',
            'cover',
            'number',
            'members',
            'hidden',
        ]
        read_only_fields = ['id']


class EventSerializer(serializers.ModelSerializer):
    cover = serializers.CharField()

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'description',
            'address',
            'start_date',
            'end_date',
            'cover',
            'number',
            'members',
            'hidden',
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        cover = validated_data.pop('cover', None)
        if cover:
            with io.BytesIO(base64.b64decode(cover)) as stream:
                django_file = File(stream)
                instance.cover.save("some_file_name.png", django_file)
        instance.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        cover = validated_data.pop('cover', None)
        instance = super().create(validated_data)
        if cover:
            with io.BytesIO(base64.b64decode(cover)) as stream:
                django_file = File(stream)
                instance.cover.save("some_file_name.png", django_file)
        instance.save()
        return instance

    def to_representation(self, instance):
        return EventResponseSerializer(instance, context=self.context).data

