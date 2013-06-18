
from requests.exceptions import ConnectionError
import requests
import time


class Image(object):
    def __init__(self, client_id="", api_key=""):
        self.client_id = client_id
        self.api_key = api_key

        self.name = None
        self.id = None
        self.distribution = None

    def __call_api(self, path, params=None):
        from Droplet import DOException
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        if params:
            payload.update(params)
        max_tries = 10
        while max_tries:
            try:
                r = requests.get("https://api.digitalocean.com/images/%s%s" % (self.id, path), params=payload)
                data = r.json()
            except (ConnectionError, ValueError):
                max_tries -= 1
                if not max_tries:
                    raise
                time.sleep(60)
            else:
                break

        if data['status'] != "OK":
            raise DOException("%s\n%s" % (data["status"], data))
        return data

    def destroy(self):
        """
            Destroy the image
        """
        self.__call_api("/destroy/")

    def transfer(self, region_id):
        """
            Transfer the image
        """
        self.__call_api("/transfer/", {"region_id": region_id})
