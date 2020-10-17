import network
import logging
from settings import conf
import machine
import ujson
from settings import conf

log = logging.getLogger("wifi")


class WifiManager:

    CONNECTED = False

    def __init__(self, *args, **kwargs):
        self.nic = None
        # super(WifiManager, self).__init__(*args, **kwargs)

    def create_access_point(self):
        self.nic = network.WLAN(network.AP_IF)
        self.nic.active(True)
        self.nic.ifconfig(conf.AP_DHCP_SETTING)
        log.info("Settings: {}".format(ujson.dumps(conf.AP_DHCP_SETTING)))
        self.nic.config(essid=conf.AP_WIFI_SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=conf.AP_WIFI_PASS, **conf.AP_OPTIONS)
        log.info("Wifi: {} as WPA_WPA2_PSK {}".format(conf.AP_WIFI_SSID, ujson.dumps(conf.AP_OPTIONS)))

    @classmethod
    def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)  # create station interface
        wlan.active(True)

        if wlan.isconnected() == True:
            log.info("Already connected to {}".format(ssid))

        wlan.connect(conf.WIFI_SSID, conf.WIFI_PASS)
        while not wlan.isconnected():
            machine.idle()


def start():
    wifi_manager = WifiManager()
    wifi_manager.create_access_point()


def connect():
    WifiManager.connect_to_wifi()
