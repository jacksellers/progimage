import os

from PIL import Image as pi

from wrapper import ImageClient


ic = ImageClient()

# Create an image file
f = open('example-to-be-deleted.jpeg', 'w+')
image = pi.new('RGB', (100, 100))
image.save(f.name)

# Upload it
res = ic.upload(image=f.name, description='example description')

# Get the code
code = res['json']['code']

# Download the image
res = ic.download(code=code)

# Original image
print('\nOriginal image:\n', res)

# Change its description
res = ic.update(code=code, description='example description 2')

# Convert its file format
res = ic.update(code=code, file_format='.png')

# Updated image
print('\nUpdated image:\n', res)

# Delete file
os.remove(f.name)
