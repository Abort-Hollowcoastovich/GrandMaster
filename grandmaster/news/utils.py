import uuid
import os


def path_and_hash(path):
    def wrapper(instance, filename):
        filename = uuid.uuid4().hex + '.' + filename.split('.')[-1]
        return os.path.join(path, filename)
    return wrapper
