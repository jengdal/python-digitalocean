
from requests.exceptions import ConnectionError
import requests
import time
from digitalocean.Droplet import Droplet, DOException
from digitalocean.Region import Region
from digitalocean.Size import Size
from digitalocean.Image import Image

class Manager(object):
    def __init__(self, client_id="", api_key=""):
        self.client_id = client_id
        self.api_key = api_key

    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        max_tries = 10
        while max_tries:
            try:
                r = requests.get("https://api.digitalocean.com/%s" % path, params=payload)
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

    def get_all_regions(self):
        """
            This function returns a list of Region object.
        """
        data = self.__call_api("/regions/")
        regions = list()
        for jsoned in data['regions']:
            region = Region()
            region.id = jsoned['id']
            region.name = jsoned['name']
            region.client_id = self.client_id
            region.api_key = self.api_key
            regions.append(region)
        return regions

    def get_all_droplets(self):
        """
            This function returns a list of Droplet object.
        """
        data = self.__call_api("/droplets/")
        droplets = list()
        for jsoned in data['droplets']:
            droplet = Droplet()
            droplet.backup_active = jsoned['backups_active']
            droplet.region_id = jsoned['region_id']
            droplet.size_id = jsoned['size_id']
            droplet.image_id = jsoned['image_id']
            droplet.status = jsoned['status']
            droplet.name = jsoned['name']
            droplet.id = jsoned['id']
            droplet.client_id = self.client_id
            droplet.api_key = self.api_key
            droplets.append(droplet)
        return droplets

    def get_all_sizes(self):
        """
            This function returns a list of Size object.
        """
        data = self.__call_api("/sizes/")
        sizes = list()
        for jsoned in data['sizes']:
            size = Size()
            size.id = jsoned['id']
            size.name = jsoned['name']
            size.client_id = self.client_id
            size.api_key = self.api_key
            sizes.append(size)
        return sizes

    def get_all_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.__call_api("/images/")
        images = list()
        for jsoned in data['images']:
            image = Image()
            image.id = jsoned['id']
            image.name = jsoned['name']
            image.distribution = jsoned['distribution']
            image.client_id = self.client_id
            image.api_key = self.api_key
            images.append(image)
        return images

    def get_my_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.__call_api("/images/",{"filter":"my_images"})
        images = list()
        for jsoned in data['images']:
            image = Image()
            image.id = jsoned['id']
            image.name = jsoned['name']
            image.distribution = jsoned['distribution']
            image.client_id = self.client_id
            image.api_key = self.api_key
            images.append(image)
        return images

    def get_global_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.__call_api("/images/",{"filter":"global"})
        images = list()
        for jsoned in data['images']:
            image = Image()
            image.id = jsoned['id']
            image.name = jsoned['name']
            image.distribution = jsoned['distribution']
            image.client_id = self.client_id
            image.api_key = self.api_key
            images.append(image)
        return images

    def get_all_ssh_keys(self):
        data = self.__call_api("/ssh_keys/")
        return data["ssh_keys"]
