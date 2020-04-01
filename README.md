# progimage

### Description
REST API for image uploads, downloads and format conversions

### Installation
```
git clone https://github.com/jackwsellers/progimage.git
cd progimage
virtualenv appenv
source appenv/bin/activate
pip install -r requirements.txt
cd app
python manage.py makemigrations images
python manage.py migrate
```

### Testing
Run unit tests:
```
mkdir media
python manage.py test
```
Run the server:
```
python manage.py runserver
```
Visit http://127.0.0.1:8000/admin/ for the admin site

Visit http://127.0.0.1:8000/images/upload/ to upload an image with the browsable API

(replace 'upload' in the above URL with your image code to download it)

### Client
While the server is running, in another console - run:
```
python examples.py
```
This script will use the API wrapper to upload, download and update an example image.
