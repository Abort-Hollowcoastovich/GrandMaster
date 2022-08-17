from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=256)
    link = models.URLField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField()

    class Meta:
        db_table = 'videos'
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

