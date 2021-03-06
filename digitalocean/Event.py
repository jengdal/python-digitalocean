
from requests.exceptions import ConnectionError
import requests
import time


class Event(object):
    def __init__(self, event_id=""):
        self.id = event_id
        self.client_id = None
        self.api_key = None
        self.event_type_id = None
        self.percentage = None
        self.droplet_id = None
        self.action_status = None
        
    def __call_api(self, path, params=dict()):
        from Droplet import DOException
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)

        max_tries = 10
        while max_tries:
            try:
                r = requests.get("https://api.digitalocean.com/events/%s%s" % ( self.id, path ), params=payload)
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

    def load(self):
        event = self.__call_api("")
        if event:
            event = event.get(u'event')
            self.id = event['id']
            self.event_type_id = event[u'event_type_id']
            self.percentage = event[u'percentage']
            self.droplet_id = event[u'droplet_id']
            self.action_status = event[u'action_status']
