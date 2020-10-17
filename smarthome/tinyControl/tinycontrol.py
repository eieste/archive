import logging
from power import main as power
from control.control_parameters import ControlParameters
from settings import conf
import memcache
from device.main import start as deviceManager
import time


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("MainLoop")


if __name__ == "__main__":

    log.info("Initialize Cache")
    ControlParameters.cache = memcache.Client(conf.MEMCACHED_HOST)

    log.info("Start Power Module")
    power.start()

    loop_timing = {
        "dm": {
            "last": time.time()-700,
            "delta": 600
        }
    }
    while True:

        if time.time()-loop_timing["dm"]["delta"] > loop_timing["dm"]["last"]:
            deviceManager()
            loop_timing["dm"]["last"] = time.time()

        time.sleep(60)