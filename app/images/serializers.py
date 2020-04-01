import hashlib
import os

from rest_framework import serializers
from PIL import Image as pi

from images.models import Image


class CreateImageSerializer(serializers.ModelSerializer):
    """Serializer for creating an image."""

    class Meta:
        model = Image
        fields = (
            'code', 'description', 'file_name', 'file_format', 'uploaded_at'
        )
        read_only_fields = ('code', 'file_format')

    def create(self, validated_data):
        return Image.objects.create_image(**validated_data)


class RetrieveUpdateImageSerializer(serializers.ModelSerializer):
    """Serializer for retrieving or updating an image."""

    class Meta:
        model = Image
        fields = (
            'code', 'description', 'file_name', 'file_format', 'uploaded_at'
        )
        read_only_fields = ('code', 'file_name')

    def update(self, instance, validated_data):
        image = Image.objects.get(code=instance.code)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.file_format = validated_data.get(
            'file_format', instance.file_format
        )
        if instance.file_format != image.file_format:
            old_file = pi.open(image.file_name).convert('RGB')
            new_file_name = os.path.splitext(
                str(image.file_name)
            )[0].lower() + instance.file_format
            old_file.save('media/' + new_file_name)
            instance.file_name = new_file_name
        instance.save()
        return instance
