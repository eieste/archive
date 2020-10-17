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


class SP3Device:

    STORE = deque(maxlen=5000000)
    DEVICE_LIST = []

    def __init__(self, id, description, mac, ip):
        self._id = id
        self._description = description
        self._mac = mac
        self._ip = ip
        self._created = datetime.now()
        self._last_update = datetime.now()

    def __str__(self):
        return f"{self._id} {self._description}"


    def set_ip(self, new_ip):
        self._last_update = datetime.now()
        self._ip = new_ip

    def set_mac(self, new_mac):
        self._last_update = datetime.now()
        self._mac = new_mac

    def get_ip(self):
        return self._ip

    def get_mac(self):
        return self._mac

    def get_broadlink_device(self):
        return sp2(host=(self.get_ip(), 80), mac=self.get_mac(), devtype=38010)

    def add_datapoint(self, energy):
        datapoint = Datapoint(self, energy)
        SP3Device.STORE.append(datapoint)
        return datapoint

    @staticmethod
    def find_device_by_mac(mac):
        for device in SP3Device.DEVICE_LIST:
            if device.get_mac() == mac:
                return device

    @staticmethod
    def create(id, description, mac, ip):
        device = SP3Device(id, description, mac, ip)
        SP3Device.DEVICE_LIST.append(device)
        return device

    @staticmethod
    def get_or_create_device(id, description, mac, ip):
        device = SP3Device.find_device_by_mac(mac)

        if device is None:
            device = SP3Device.create(id, description, mac, ip)

        device.set_ip(ip)
        device.set_mac(mac)

        return device
