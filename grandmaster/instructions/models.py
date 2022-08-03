from django.db import models

from utils.image_path import PathAndHash


class InstructionPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('documents/' + path)


class Instruction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document = models.FileField()
    order = models.IntegerField()

    def __str__(self):
        return self.title
