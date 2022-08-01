from django.db import models
from .utils import path_and_hash


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    viewed_times = models.IntegerField(default=0)
    order = models.IntegerField(blank=False)
    hidden = models.BooleanField(default=False)
    cover = models.ImageField(upload_to=path_and_hash('news/covers'))

    class Meta:
        db_table = 'news'
        ordering = ['-order', '-created_at']

    def __str__(self):
        return self.title


class NewsImage(models.Model):
    news = models.ForeignKey(to=News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=path_and_hash('news/images'))

    class Meta:
        db_table = 'news_images'
