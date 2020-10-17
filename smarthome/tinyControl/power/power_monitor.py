import threading
import logging
from contrib.broadlink import sp2
import time
import requests
import json
from control.control_parameters import ControlParameters
from collections import deque
from settings import conf
import pickle
from device.device import Device, DeviceModule
from device.dm import DeviceManager
from power.models import Datapoint
log = logging.getLogger("BroadlinkPowerMonitor")
log.setLevel(logging.DEBUG)


class PowerMonitor(threading.Thread):

    DATAPOINT_LIST = deque(maxlen=5000000)

    def __init__(self, *args, **kwargs):
        super(PowerMonitor, self).__init__(*args, **kwargs)

    def collect_energy_values(self):

        for device in Device.find_by_module(DeviceModule.SP3):

            broadlink_device = sp2(
                (device.get_attribute("ip_address", flat=True), 80),
                mac=device.get_attribute("mac_address", flat=True),
                devtype=38010
            )

            try:
                broadlink_device.auth()
                energy = broadlink_device.get_energy()
                dp = Datapoint(device, energy)
                PowerMonitor.DATAPOINT_LIST.append(dp)
            except OSError:
                log.error("Device {} is not reachable".format(device))
            except ValueError:
                log.error("Device {} doesnt return a correct Value".format(device))

    def send_device_log(self):
        failed_to_send = []
        FAIL = False

        for dp in list(PowerMonitor.DATAPOINT_LIST):

            if not FAIL:
                try:
                    dp.send()
                except Exception as e:
                    FAIL = True
                    log.exception(e)
                    failed_to_send.append(dp)
            else:
                failed_to_send.append(dp)

        PowerMonitor.DATAPOINT_LIST.clear()
        PowerMonitor.DATAPOINT_LIST.extend(failed_to_send)
        log.debug(f"Store lenght {len(PowerMonitor.DATAPOINT_LIST)}")

    def _get_endpoint(self):
        return "http://"+conf.FLAT_API_HOST+""+conf.FLAT_API_PORT+"/device/?device-type=broadlink-sp3"

    def run(self):
        last_update = -600
        last_collect = -120

        while True:

            if not DeviceManager.READY:
                time.sleep(1)
                continue
                
            if last_collect < time.time() - 60:
                log.info("Collect energy Values")
                self.collect_energy_values()
                last_collect = time.time()

            self.send_device_log()

            time.sleep(10)