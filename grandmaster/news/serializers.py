import json

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import News, NewsImage


class NewsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image']


class NewsSerializer(serializers.ModelSerializer):
    images = NewsImagesSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'viewed_times',
            'order',
            'hidden',
            'cover',
            'images'
        ]
        read_only_fields = ['id', 'viewed_times', 'created_at']

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        images_data.pop('cover')
        news = News.objects.create(**validated_data)
        for image_data in images_data.values():
            NewsImage.objects.create(news=news, image=image_data)
        return news

    def update(self, instance, validated_data):
        request = self.context.get('view').request
        data = request.data
        print(data)
        title = data.pop('title', None)
        description = data.pop('description', None)
        order = data.pop('order', None)
        hidden = data.pop('hidden', None)
        cover = data.pop('cover', None)
        if title is not None:
            instance.title = title[0]
        if description is not None:
            instance.description = description[0]
        if order is not None:
            instance.order = order[0]
        if hidden is not None:
            instance.hidden = hidden[0].capitalize()
        if cover is not None:
            instance.cover = cover[0]

        # items {'id': new_image_to_change, 'random_str': add_image, 'id': 'leave_image'}
        save_images = []
        for key, value in data.items():
            if isinstance(value, InMemoryUploadedFile):
                if key.isdigit():
                    save_images.append(key)
            else:
                save_images.append(key)
        NewsImage.objects.exclude(id__in=save_images).delete()
        for key, value in data.items():
            if isinstance(value, InMemoryUploadedFile):
                if key.isdigit():
                    try:
                        image = NewsImage.objects.get(id=key)
                        image.image = value
                        image.save()
                    except NewsImage.DoesNotExist:
                        raise NotFound
                else:
                    instance.images.add(NewsImage.objects.create(news=instance, image=value))
        instance.save()
        return instance
