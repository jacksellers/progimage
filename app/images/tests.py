import shutil

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image as pi
from tempfile import NamedTemporaryFile

from images.models import Image


CREATE_IMAGE_URL = reverse('images:upload')
TEST_DIR = 'test_media'

def create_temporary_image(file_extension):
    """Helper function to create and return a temporary image."""
    tmp_file = NamedTemporaryFile(suffix=file_extension)
    image = pi.new('RGB', (100, 100))
    image.save(tmp_file.name)
    return tmp_file

def get_image_code():
    """Helper function to create an image and return its code."""
    tmp_file = create_temporary_image('.jpeg')
    image = Image.objects.create_image(
        description='test description',
        file_name=tmp_file.name
    )
    return image.code


class ImagesApiTests(TestCase):
    """Test the images API."""

    def setUp(self):
        self.client = APIClient()

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_upload_valid_format(self):
        """Test uploading an image with a valid file format."""
        tmp_file = create_temporary_image('.png')
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
        tmp_file = create_temporary_image('.pdf')
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
        code = get_image_code()
        res = self.client.get(
            reverse('images:download', kwargs={'code': code})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('code', res.data)
        self.assertIn('file_name', res.data)
        self.assertIn('file_format', res.data)
    
    def test_update_description(self):
        """Test updating an image's description."""
        code = get_image_code()
        payload = {'description': 'test description 2'}
        res = self.client.patch(
            reverse('images:download', kwargs={'code': code}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['description'], 'test description 2')
    
    def test_update_valid_format(self):
        """Test updating an image with a valid format."""
        code = get_image_code()
        payload = {'file_format': '.png'}
        res = self.client.patch(
            reverse('images:download', kwargs={'code': code}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['file_format'], '.png')


def tearDownModule():
    print('\nDeleting temporary files...\n')
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
