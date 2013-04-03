import requests

class Image(object):
    def __init__(self, client_id="", api_key=""):
        self.client_id = client_id
        self.api_key = api_key

        self.name = None
        self.id = None
        self.distribution = None

    def __call_api(self, path, params=None):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        if params:
            payload.update(params)
        r = requests.get("https://api.digitalocean.com/images/%s%s" % (self.id, path), params=payload)
        data = r.json()
        if data['status'] != "OK":
            return None # Raise?
        return data

    def destroy(self):
        """
            Restore the droplet to an image ( snapshot or backup )
        """
        self.__call_api("/destroy/")
