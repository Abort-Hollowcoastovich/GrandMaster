from django.utils.deconstruct import deconstructible

import uuid
import os


@deconstructible
class PathAndHash(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        filename = str(instance) + '_' + uuid.uuid4().hex + '.' + filename.split('.')[-1]
        return os.path.join(self.path, filename)
