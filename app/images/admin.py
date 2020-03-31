from django.contrib import admin

from images.models import Image


class ImageAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'code', 'file_name', 'file_format', 'uploaded_at']

admin.site.register(Image, ImageAdmin)
