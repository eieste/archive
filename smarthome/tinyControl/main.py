import logging
from power import main as power
from control.control_parameters import ControlParameters
from settings import conf
import memcache


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("MainLoop")


if __name__ == "__main__":

    log.info("Initialize Cache")
    ControlParameters.cache = memcache.Client(conf.MEMCACHED_HOST)

    log.info("Start Power Module")
    power.start()
