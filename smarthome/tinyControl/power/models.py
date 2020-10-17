from collections import namedtuple, deque
from datetime import datetime
from contrib.broadlink import sp2
from settings import conf
import requests


class Datapoint:

    def __init__(self, device, value, timestamp=None):
        if timestamp is None:
            self._timestamp = datetime.now()
        else:
            self._timestamp = timestamp

        self._device = device
        self._value = value

    def get_device(self):
        return self._device

    def get_value(self):
        return self._value

    def get_timestamp(self):
        return int((datetime.now()-self._timestamp).total_seconds())

    def send(self):
        pass

    def get_endpoint(self):
        return f"http://" + conf.FLAT_API_HOST + "" + conf.FLAT_API_PORT + f"/control/{self._device._id}/sp3/"

    def get_packet(self):
        return {
            "power": self._value,
            "timestamp": self.get_timestamp()
        }

    def send(self):
        response = requests.post(self.get_endpoint(), json=self.get_packet())
        print(response.json())