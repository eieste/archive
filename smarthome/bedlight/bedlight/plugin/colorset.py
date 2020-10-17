from plugin.baseplugin import BasePlugin
from utils.conf import settings
import logging
import board
import adafruit_ws2801
import struct

log = logging.getLogger("ColorsetPlugin")


class Colorset(BasePlugin):

    topic = "{}led/color".format(settings.MQTT_TOPIC)

    def __init__(self):
        self._led = adafruit_ws2801.WS2801(board.SCLK, board.MOSI, settings.LED_COUNT, brightness=1.0, auto_write=False)

    def on_message(self, topic, payload):
        r,g,b,start,end = struct.unpack("BBBBB", payload)

        for i in range(start, end):
            try:
                self._led[i] = (r,g,b)
            except Exception as e:
                pass
        self._led.show()

leds = adafruit_ws2801.WS2801(board.D2, board.D0, 25)
leds.fill((0x80, 0, 0))
