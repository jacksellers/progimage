import requests


class ImageClient(object):
    """Interact with the Images API."""

    def __init__(self):
        self.api_url = 'http://127.0.0.1:8000/images/'
    
    def api_call(self, endpoint, method='get', payload=None, files=None):
        """Makes an API call to the server."""
        if files:
            r = requests.request(
                method, self.api_url + endpoint, data=payload, files=files
            )
        else:
            r = requests.request(
                method, self.api_url + endpoint, json=payload
            )
        return {'status': r.status_code, 'json': r.json()}
    
    def upload(self, image, description=None):
        """Upload an image."""
        payload = {'description': description}
        files = {'file_name': open(image, 'rb')}
        return self.api_call(
            endpoint='upload/',
            method='post',
            payload=payload,
            files=files
        )
    
    def download(self, code):
        """Download an image."""
        return self.api_call(
            endpoint='{}/'.format(code),
            method='get'
        )
    
    def update(self, code, description=None, file_format=None):
        """Convert an image or change its description."""
        payload = {}
        for param in ['description', 'file_format']:
            if eval(param) is not None:
                payload[param] = eval(param)
        return self.api_call(
            endpoint='{}/'.format(code),
            method='patch',
            payload=payload
        )
