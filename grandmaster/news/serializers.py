from rest_framework import serializers
from .models import News, NewsImage


class NewsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['image']


class NewsSerializer(serializers.ModelSerializer):
    images = NewsImagesSerializer(many=True, read_only=True)
    
    class Meta:
        model = News
        fields = [
            'pk',
            'title',
            'description',
            'created_at',
            'viewed_times',
            'order',
            'hidden',
            'cover',
            'images'
        ]
        read_only_fields = ['pk', 'viewed_times', 'created_at']

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        images_data.pop('cover')
        news = News.objects.create(**validated_data)
        for image_data in images_data.values():
            NewsImage.objects.create(news=news, image=image_data)
        return news

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        images = self.context.get('view').request.FILES
        images.pop('cover', None)
        for image in images.values():
            instance.images.add(NewsImage.objects.create(news=instance, image=image))
        instance.images.add()
        return instance

