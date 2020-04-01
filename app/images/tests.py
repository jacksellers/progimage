import shutil
import os

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image as pi
from tempfile import NamedTemporaryFile

from images.models import Image


CREATE_IMAGE_URL = reverse('images:upload')
TEST_DIR = 'test_media'


class ImagesApiTests(TestCase):
    """Test the images API."""

    def setUp(self):
        self.client = APIClient()

    def create_image(self, file_extension):
        """Helper function to create and return an image."""
        f = open('media/test-to-be-deleted' + file_extension, 'w+')
        image = pi.new('RGB', (100, 100))
        image.save(f.name)
        return f.name

    def create_temporary_image(self, file_extension):
        """Helper function to create and return a temporary image."""
        tmp_file = NamedTemporaryFile(suffix=file_extension)
        image = pi.new('RGB', (100, 100))
        image.save(tmp_file.name)
        return tmp_file

    def get_image_code(self):
        """Helper function to create an image and return its code."""
        file_name = self.create_image('.jpeg')
        image = Image.objects.create_image(
            description='test description',
            file_name=file_name[6:]
        )
        return image.code

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_upload_valid_format(self):
        """Test uploading an image with a valid file format."""
        tmp_file = self.create_temporary_image('.png')
        payload = {
            'description': 'test description',
            'file_name': tmp_file
        }
        res = self.client.post(CREATE_IMAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', res.data)
        self.assertIn('file_name', res.data)
        self.assertIn('file_format', res.data)

    def test_upload_invalid_format(self):
        """Test uploading an image with an invalid file format."""
        tmp_file = self.create_image('.pdf')
        payload = {
            'description': 'test description',
            'file_name': tmp_file
        }
        res = self.client.post(CREATE_IMAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_upload_no_file(self):
        """Test uploading an image with no file."""
        payload = {'description': 'test description'}
        res = self.client.post(CREATE_IMAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_download(self):
        """Test downloading an image."""
        code = self.get_image_code()
        res = self.client.get(
            reverse('images:download', kwargs={'code': code})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('code', res.data)
        self.assertIn('file_name', res.data)
        self.assertIn('file_format', res.data)
    
    def test_update_description(self):
        """Test updating an image's description."""
        code = self.get_image_code()
        payload = {'description': 'test description 2'}
        res = self.client.patch(
            reverse('images:download', kwargs={'code': code}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['description'], 'test description 2')
    
    def test_update_valid_format(self):
        """Test updating an image with a valid format."""
        code = self.get_image_code()
        payload = {'file_format': '.png'}
        res = self.client.patch(
            reverse('images:download', kwargs={'code': code}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['file_format'], '.png')
    
    def test_update_invalid_format(self):
        """Test updating an image with an invalid format."""
        code = self.get_image_code()
        payload = {'file_format': '.pdf'}
        res = self.client.patch(
            reverse('images:download', kwargs={'code': code}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


def tearDownModule():
    print('\nDeleting temporary files...\n')
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
    os.chdir(os.getcwd() + '/media')
    for file in os.listdir(os.getcwd()):
        if os.path.splitext(file)[0] == 'test-to-be-deleted':
            os.remove(file)
