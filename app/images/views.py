from rest_framework import generics

from images.models import Image
from images.serializers import CreateImageSerializer, \
                               RetrieveUpdateImageSerializer


class CreateImageView(generics.CreateAPIView):
    """Create a new image."""
    queryset = Image.objects.all()
    serializer_class = CreateImageSerializer


class RetrieveUpdateImageView(generics.RetrieveUpdateAPIView):
    """Retrieve or update an image."""
    serializer_class = RetrieveUpdateImageSerializer
    lookup_field = 'code'

    def get_queryset(self):
        return Image.objects.filter(code=self.kwargs['code'])
