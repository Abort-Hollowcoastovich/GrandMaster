from django.db import models


class Instruction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        db_table = 'instructions'
        ordering = ['order', 'created_at']
        verbose_name = 'Учебный материал'
        verbose_name_plural = 'Учебные материалы'

    def __str__(self):
        return self.title
