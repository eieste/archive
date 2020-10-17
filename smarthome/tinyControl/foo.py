import binascii
import logging
from power.power_monitor import PowerMonitor

from contrib.broadlink import sp2


log = logging.getLogger(__name__)


#34:EA:34:7B:37:DE"
mac = "34:EA:34:7B:37:DE"
devices = [
    sp2(mac=bytearray(b'\xde7{4\xea4'), host=('192.168.69.23', 80), devtype=38010),
]

for dev in devices:
    try:
        print(dev.auth())
        print(dev.mac)
        print(dev.host)
        print(dev.check_power())
        print(dev.get_energy())
        print("-"*10)
    except Exception as e:
        log.exception(e)
    print("-"*100)
