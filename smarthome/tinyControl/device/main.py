import logging
from device.dm import DeviceManager

log = logging.getLogger("DeviceManager")


def start():
    log.info("Start Device Manager")
    dm = DeviceManager()
    dm.run()


if __name__ == "__main__":
    start()