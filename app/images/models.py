import os

from django.conf import settings
from django.db import models
from hashids import Hashids


FILE_FORMATS = [
    ('.bmp', 'BMP'), ('.gif', 'GIF'), ('.jpeg', 'JPEG'), ('.png', 'PNG')
]


class ImageManager(models.Manager):

    def create_image(self, file_name, **extra_fields):
        """Creates and saves a new image with a unique code and file format."""
        image = Image.objects.create(file_name=file_name, **extra_fields)
        hashids = Hashids(
            salt=settings.SECRET_KEY,
            min_length=10,
            alphabet='abcdefghijkmnopqrstuvwxyz123456789'
        )
        image.code = hashids.encode(image.id)
        image.file_format = os.path.splitext(str(file_name))[1].lower()
        image.save()
        return image


class Image(models.Model):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    file_name = models.ImageField()
    file_format = models.CharField(choices=FILE_FORMATS, max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = ImageManager()
