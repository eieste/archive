import threading
import logging
import requests
from settings import conf
from device.device import Device
log = logging.getLogger("DeviceManager")
log.setLevel(logging.DEBUG)


class DeviceManager:
    READY = False

    def get_endpoint(self):
        return "http://"+conf.FLAT_API_HOST+""+conf.FLAT_API_PORT+"/device/"

    def get_devices(self):
        response = requests.get(self.get_endpoint())
        data = response.json()
        return data["objects"]

    def update_device_list(self, device_list):
        for device in device_list:
            dev = Device.update_or_create(device["id"],
                                            device["description"],
                                            device_type_dict=device["device_type"],
                                            attribute_dict=device["attributes"],
                                            module_names=device["modules"]
                                            )

    def run(self):
        try:
            raw_device_list = self.get_devices()
            self.update_device_list(raw_device_list)
            DeviceManager.READY = True
        except Exception as e:
            log.error("Cant update devicelist")
